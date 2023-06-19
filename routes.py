from flask import (
    render_template,
    url_for,
    request,
    jsonify,
    send_from_directory,
    Blueprint,
)
from index_builder import IndexBuilder
from config import content_folder_path, content_folder_branch, webhook_secret
from search import search_md_files
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from flask import session
from urllib.parse import urljoin
from repo import pull_changes
import os
import logging
import re
import hashlib
import hmac

markdowner = MarkdownIt().use(tasklists_plugin)
routes = Blueprint("routes", __name__)


@routes.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(routes.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@routes.route("/sidebar")
def sidebar():
    index_builder = IndexBuilder()
    if "email" not in session:
        html_content = index_builder.get_public_index()
    else:
        html_content = index_builder.get_private_index()

    template_name = "sidebar.html"
    return render_template(template_name, content=html_content)


@routes.route("/search")
def search():
    query = request.args.get("query", "")
    if not query:
        return "No query provided", 400

    logged_in = "email" in session
    matching_files = search_md_files(query, content_folder_path, logged_in)
    matching_links_and_excerpts = [
        {
            "link": url_for(
                "routes.view_md", md_path=os.path.splitext(file["path"])[0]
            ),
            "excerpt": markdowner.render(file["excerpt"]),
            "file_name": os.path.splitext(os.path.basename(file["path"]))[0],
        }
        for file in matching_files
    ]
    return render_template("search_results.html", results=matching_links_and_excerpts)


@routes.route("/images/<path:subpath>")
def serve_image(subpath):
    return send_from_directory(content_folder_path, subpath)


@routes.route("/view-folder/", defaults={"folder": ""})
@routes.route("/view-folder/<path:folder>")
def view_folder(folder):
    full_path = os.path.join(content_folder_path, folder)
    if not os.path.isdir(full_path):
        return "Folder not found", 404


@routes.route("/view-md/<path:md_path>")
def view_md(md_path):
    if request.headers.get("X-Requested-With") != "XMLHttpRequest":
        return render_template("base.html")
    if "private" in md_path.split("/")[-1] and "email" not in session:
        return jsonify(status="redirect", url=url_for("auth.login"))

    full_path = os.path.join(content_folder_path, md_path + ".md")
    if not os.path.isfile(full_path) or not full_path.endswith(".md"):
        return "File not found", 404
    md_content = __fetch_markdown_content(full_path)
    html_content = markdowner.render(md_content)
    return render_template("md_page.html", content=html_content, active_folder=md_path)


@routes.route("/repo/<path:path>")
def serve_repo_files(path):
    return send_from_directory(content_folder_path, path)


@routes.route("/")
def index():
    folder = request.args.get("folder", None)
    # Depending on your base.html, you might not need to pass these variables
    # You also might need to pass other variables, depending on your template
    return render_template("base.html", active_folder=folder)


@routes.route("/gh-update", methods=["post"])
def gh_update():
    signature = request.headers.get("X-Hub-Signature")
    if signature is None:
        logging.info("Invalid signature")
        return "Invalid signature", 400

    signature_parts = signature.split("=", 1)
    if len(signature_parts) != 2:
        logging.info("Invalid signature")
        return "Invalid signature", 400

    signature_type, signature_value = signature_parts
    if signature_type != "sha1":
        logging.info("Unsupported signature type")
        return "Unsupported signature type", 400

    secret = webhook_secret
    mac = hmac.new(secret.encode("utf-8"), request.data, hashlib.sha1)
    expected_signature = f"sha1={mac.hexdigest()}"
    if not hmac.compare_digest(signature, expected_signature):
        logging.info("Invalid signature")
        return "Invalid signature", 400

    event_type = request.headers.get("X-GitHub-Event")

    if event_type == "push":
        branch = request.json.get("ref", "").split("/")[-1]
        if branch == content_folder_branch:
            logging.info("Updating content folder from Github...")
            pull_changes(content_folder_path, branch)
            return jsonify({"status": "success", "message": "Repository updated"}), 200
        else:
            logging.info("Branch was not a match, not updating content")
            return jsonify({"status": "skipped", "message": "No update needed"}), 200
    return (
        jsonify(
            {
                "status": "not_processed",
                "message": f"Unexpected event type: {event_type}",
            }
        ),
        200,
    )


def __fetch_markdown_content(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    # Get the real folder path
    real_folder_path = __get_real_folder_path(file_path)
    # Find image paths and prepend the /images/ route and the real folder path to the path
    content = re.sub(
        r'\!\[(.*?)\]\((.*?)(\s"(.*?)")?\)',
        rf"![\1](/images/{real_folder_path}/\2)",
        content,
    )

    # Prepend /view-md/ to all links pointing to .md files but not starting with #
    content = re.sub(
        r"\[(.*?)\]\((?!#)(.*?\.md)\)",
        lambda m: f'[{m.group(1)}]({urljoin("/view-md/", m.group(2))})',
        content,
    )

    return content


def __get_real_folder_path(file_path):
    real_folder_path = os.path.relpath(os.path.dirname(file_path), content_folder_path)
    return real_folder_path.replace(" ", "%20")

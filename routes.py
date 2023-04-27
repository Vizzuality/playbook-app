from flask import render_template, redirect, url_for, session, flash, request, jsonify, send_from_directory, Blueprint
from repo import pull_changes
from index_builder import fetch_markdown_content
from config import local_repo_path
from search import search_md_files
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from flask import session
import os

markdowner = MarkdownIt().use(tasklists_plugin)
routes = Blueprint('routes', __name__)

@routes.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return "No query provided", 400

    logged_in = 'email' in session
    matching_files = search_md_files(query, local_repo_path, logged_in)
    matching_links_and_excerpts = [
        {
            'link': url_for('routes.view_md', md_path=os.path.splitext(file['path'])[0]),
            'excerpt': markdowner.render(file['excerpt']),
            'file_name': os.path.splitext(os.path.basename(file['path']))[0]
        } for file in matching_files
    ]
    return render_template('search_results.html', results=matching_links_and_excerpts)

@routes.route('/images/<path:subpath>')
def serve_image(subpath):
    return send_from_directory(local_repo_path, subpath)

@routes.route('/view-folder/', defaults={'folder': ''})
@routes.route('/view-folder/<path:folder>')
def view_folder(folder):
    full_path = os.path.join(local_repo_path, folder)
    if not os.path.isdir(full_path):
        return "Folder not found", 404

@routes.route('/view-md/<path:md_path>')
def view_md(md_path):
    if "private" in md_path.split("/")[-1] and 'email' not in session:
        return redirect(url_for('auth.login'))

    full_path = os.path.join(local_repo_path, md_path + '.md')
    if not os.path.isfile(full_path) or not full_path.endswith('.md'):
        return "File not found", 404
    md_content = fetch_markdown_content(full_path)
    html_content = markdowner.render(md_content)
    return render_template('md_page.html', content=html_content, active_folder=md_path)



@routes.route('/repo/<path:path>')
def serve_repo_files(path):
    return send_from_directory(local_repo_path, path)

@routes.route('/')
def index():
    folder = request.args.get('folder', None)
    if 'email' not in session:
        with open(os.path.join(local_repo_path, 'public_index.md'), 'r') as file:
            html_content = file.read()
        template_name = 'public_index.html'
    else:
        with open(os.path.join(local_repo_path, 'private_index.md'), 'r') as file:
            html_content = file.read()
        template_name = 'private_index.html'

    return render_template(template_name, content=html_content, active_folder=folder)

@routes.route('/update-repo', methods=['post'])
def update_repo():
    payload = request.get_json()
    print(payload)

    # Verify the webhook payload (optional but recommended)
    # You can use the 'X-Hub-Signature-256' header and a secret to verify the payload
    # Check the GitHub documentation for more information

    if payload.get('ref') == 'refs/heads/master':  # Replace 'main' with your default branch
        pull_changes(local_repo_path)
        return jsonify({'status': 'success', 'message': 'Repository updated'}), 200
    else:
        return jsonify({'status': 'skipped', 'message': 'No update needed'}), 200

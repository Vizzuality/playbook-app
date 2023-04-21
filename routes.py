from flask import render_template, redirect, url_for, session, flash, request, jsonify, send_from_directory, Blueprint
from repo import pull_changes
from index_builder import fetch_markdown_content
from config import local_repo_path
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin

import os
markdowner = MarkdownIt().use(tasklists_plugin)
routes = Blueprint('routes', __name__)

@routes.route('/images/<path:subpath>')
def serve_image(subpath):
    return send_from_directory(local_repo_path, subpath)

@routes.route('/view-md/<path:md_path>')
def view_md(md_path):
    full_path = os.path.join(local_repo_path, md_path)
    if not os.path.isfile(full_path) or not full_path.endswith('.md'):
        return "File not found", 404

    md_content = fetch_markdown_content(full_path)
    html_content = markdowner.render(md_content)
    return render_template('public_page.html', content=html_content)


@routes.route('/repo/<path:path>')
def serve_repo_files(path):
    return send_from_directory(local_repo_path, path)

@routes.route('/')
def index():
    md_content = fetch_markdown_content(os.path.join(local_repo_path, 'public_index.md'))
    html_content = markdowner.render(md_content)
    return render_template('public_index.html', content=html_content)

@routes.route('/public-page')
def public_page():
    md_content = fetch_markdown_content(os.path.join(local_repo_path, 'public_index.md'))
    html_content = markdowner.render(md_content)
    return render_template('public_index.html', content=html_content)

@routes.route('/private-page')
def private_page():
    if 'email' not in session:
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('login'))
    md_content = fetch_markdown_content(os.path.join(local_repo_path, 'private_index.md'))
    html_content = markdowner.render(md_content)
    return render_template('private_index.html', content=html_content)

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

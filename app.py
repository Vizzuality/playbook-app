import os
import subprocess
import git
import requests
import re
from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify, send_from_directory
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urljoin
from collections import defaultdict

load_dotenv()
if os.getenv('OAUTHLIB_INSECURE_TRANSPORT'):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
organization_domain = os.getenv('ORGANIZATION_DOMAIN')
github_repo_url = os.getenv('GITHUB_REPO_URL')
local_repo_path = os.getenv('LOCAL_REPO_PATH')

markdowner = MarkdownIt().use(tasklists_plugin)
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

# Routes

@app.route('/images/<path:subpath>')
def serve_image(subpath):
    return send_from_directory(local_repo_path, subpath)

@app.route('/view-md/<path:md_path>')
def view_md(md_path):
    full_path = os.path.join(local_repo_path, md_path)
    if not os.path.isfile(full_path) or not full_path.endswith('.md'):
        return "File not found", 404

    md_content = fetch_markdown_content(full_path)
    html_content = markdowner.render(md_content)
    return render_template('public_page.html', content=html_content)


@app.route('/repo/<path:path>')
def serve_repo_files(path):
    return send_from_directory(local_repo_path, path)

# Authentication
@app.route('/login')
def login():
    flow = Flow.from_client_config({
        'web': {
            'client_id': client_id,
            'client_secret': client_secret,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [url_for('oauth2callback', _external=True)]
        }},
        ['email', 'openid']
    )

    flow.redirect_uri = url_for('oauth2callback', _external=True)
    print(f'Redirect URI: {flow.redirect_uri}')
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state

    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_config({
        'web': {
            'client_id': client_id,
            'client_secret': client_secret,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [url_for('oauth2callback', _external=True)]
        }},
        scopes=['openid', 'email'],
        state=state
    )

    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(credentials.id_token, google_requests.Request(), client_id)

    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    if id_info['hd'] != organization_domain:
        flash("Unauthorized email domain", "error")
        return redirect(url_for('index'))

        session['email'] = id_info['email']
    flash('Login successful.', 'success')
    session['email'] = id_info['email']
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logout successful.', 'success')
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/public-page')
def public_page():
    md_content = fetch_markdown_content(os.path.join(local_repo_path, 'public_index.md'))
    html_content = markdowner.render(md_content)
    return render_template('public_index.html', content=html_content)

@app.route('/private-page')
def private_page():
    if 'email' not in session:
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('login'))
    md_content = fetch_markdown_content(os.path.join(local_repo_path, 'private_index.md'))
    html_content = markdowner.render(md_content)
    return render_template('private_index.html', content=html_content)

@app.route('/update-repo', methods=['post'])
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

# Public functions

import os
import re
from collections import defaultdict

def humanize(s):
    return re.sub(r'[-_]', ' ', s).title()

def build_menus(local_repo_path):
    public_menu = {}
    private_menu = {}

    for root, dirs, files in os.walk(local_repo_path):
        for file in files:
            if file.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, file), local_repo_path)
                rel_dir = os.path.dirname(rel_path)

                menu_to_update = private_menu if file.startswith("private") else public_menu
                current_level = menu_to_update
                for folder in rel_dir.split(os.sep):
                    current_level = current_level.setdefault(folder, {})

                current_level[file] = rel_path

    return public_menu, private_menu


def save_menus_to_files(public_menu, private_menu, local_repo_path):
    public_index_file = os.path.join(local_repo_path, "public_index.md")
    private_index_file = os.path.join(local_repo_path, "private_index.md")

    def write_nested_list(file, menu, level=0):
        indent = "    " * level
        for item, value in menu.items():
            if isinstance(value, dict):
                file.write(f"{indent}- {humanize(item)}\n")
                write_nested_list(file, value, level + 1)
            else:
                file.write(f"{indent}- [{humanize(item[:-3])}](/view-md/{value})\n")

    with open(public_index_file, "w") as public_file:
        write_nested_list(public_file, public_menu)

    with open(private_index_file, "w") as private_file:
        write_nested_list(private_file, private_menu)


def create_log_directory(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

def log_to_file(log_dir, cmd, output, error):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(os.path.join(log_dir, 'git_commands.log'), 'a') as log_file:
        log_file.write(f"Timestamp: {timestamp}\n")
        log_file.write(f"Command: {cmd}\n")
        log_file.write(f"Output: {output}\n")
        log_file.write(f"Error: {error}\n")
        log_file.write(f"{'-' * 80}\n")

def run_command(cmd, cwd, log_dir):
    process = subprocess.run(cmd, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    log_to_file(log_dir, cmd, process.stdout, process.stderr)
    return process

def pull_changes(local_repo_path):
    git_ssh_command = 'GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no"'
    log_dir = 'logs'  # Change this to the desired path for your log directory
    
    create_log_directory(log_dir)
    
    run_command(f"{git_ssh_command} git fetch origin", local_repo_path, log_dir)
    run_command(f"{git_ssh_command} git reset --hard origin/main", local_repo_path, log_dir)  # Replace 'main' with your default branch
    run_command(f"{git_ssh_command} git clean -fd", local_repo_path, log_dir)
    run_command(f"{git_ssh_command} git status", local_repo_path, log_dir)
    run_command(f"{git_ssh_command} git remote show origin", local_repo_path, log_dir)

    public_menu, private_menu = build_menus(local_repo_path)
    save_menus_to_files(public_menu, private_menu, local_repo_path)

def fetch_markdown_content(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Get the real folder path
    real_folder_path = get_real_folder_path(file_path)
    # Find image paths and prepend the /images/ route and the real folder path to the path
    content = re.sub(r'\!\[(.*?)\]\((.*?)\)', fr'![\1](/images/{real_folder_path}/\2)', content)

    # Prepend /view-md/ to all links pointing to .md files but not starting with #
    content = re.sub(r'\[(.*?)\]\((?!#)(.*?\.md)\)', lambda m: f'[{m.group(1)}]({urljoin("/view-md/", m.group(2))})', content)

    return content



def get_real_folder_path(file_path):
    return os.path.relpath(os.path.dirname(file_path), local_repo_path)


if __name__ == '__main__':
    app.run()


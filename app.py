import os
import subprocess
import git
import requests
from flask import Flask, render_template, redirect, url_for, session, flash, request, jsonify  # Add 'request' here
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests
from markdown_it import MarkdownIt
from mdit_py_plugins.tasklists import tasklists_plugin
from dotenv import load_dotenv
from datetime import datetime

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


@app.route('/private-page')
def private_page():
    if 'email' not in session:
        flash('You need to be logged in to access this page.', 'error')
        return redirect(url_for('login'))

    file_path = 'index.md'
    md_content = fetch_markdown_from_github(file_path)
    html_content = markdowner.render(md_content)
    return render_template('private_page.html', content=html_content)


@app.route('/public-page')
def public_page():
    file_path = 'index.md'
    md_content = fetch_markdown_from_github(file_path)
    html_content = markdowner.render(md_content)
    return render_template('public_page.html', content=html_content)

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


def fetch_markdown_from_github(file_path):
    headers = {'Accept': 'application/vnd.github.VERSION.raw'}
    response = requests.get(f'{github_repo_url}/{file_path}', headers=headers)
    response.raise_for_status()
    return response.text

if __name__ == '__main__':
    app.run()


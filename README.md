# Vizzuality Playbook App

This is a Python 3 Flask application that serves the Vizzuality Playbook pages by pulling the original markdown files stored in a local folder; the playbook folder is updated automatically from the Github Vizzuality Playbook repository.

The app converts the Markdown files to HTML and displays them using a web interface. The app also implements Google Single Sign-On (SSO) for authentication and requires users to log in with their Google accounts.

When a user is not loged in, the app will show puplic pages only.

## Dependencies

The app requires the following external libraries:

- flask
- google
- flask-googlemaps
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client
- markdown-it-py
- mdit-py-plugins
- python-dotenv

## Installation

```bash
git clone https://github.com/vizzuality/playbook-app.git
cd playbook-app
```

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:
```bash
pip install -r requirements.txt
```

Configure the app by creating a .env file in the root directory with the following:
```bash
CLIENT_ID=<your_google_client_id>
CLIENT_SECRET=<your_google_client_secret>
ORGANIZATION_DOMAIN=<your_organization_domain>
LOCAL_REPO_PATH=<local_path_to_clone_your_playbook_repo>
```

Run the application:
```bash
export FLASK_APP=app.py
flask run
```

## License
This project is licensed under the MIT License. See the [License](LICENSE.md) file for details.
# Vizzuality Playbook App

This is a Python 3 Flask application that serves the Vizzuality Playbook pages by pulling the original markdown files
stored in a local folder; the playbook folder is updated automatically from the Github Vizzuality Playbook repository.

The app converts the Markdown files to HTML and displays them using a web interface. The app also implements Google
Single Sign-On (SSO) for authentication and requires users to log in with their Google accounts.

When a user is not loged in, the app will show puplic pages only.

## Dependencies

- Python 3.11 + pip
- Node v18.16 + yarn v1

The Python dependent libraries can be found on `requirements.txt`
The Node dependent libraries can be found on `package.json`

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
GOOGLE_CLIENT_ID=<your_google_client_id>
GOOGLE_CLIENT_SECRET=<your_google_client_secret>
GOOGLE_ORGANIZATION_DOMAIN=<your_organization_domain>
CONTENT_FOLDER_PATH=<local_path_to_clone_your_playbook_repo>
```

Run the application:

```bash
flask run
```

## Configuration

| Variable name              | Description                                                                                               | Default value | Required? |
|----------------------------|-----------------------------------------------------------------------------------------------------------|--------------:|----------:|
| GOOGLE_CLIENT_ID           | Google Client ID for the OAuth integration                                                                |               |       yes |
| GOOGLE_CLIENT_SECRET       | Google Client Secret for the OAuth integration                                                            |               |       yes |
| GOOGLE_ORGANIZATION_DOMAIN | Google organization domain for the OAuth integration                                                      |               |       yes |
| SECRET_KEY                 | A secret key that will be used for securely signing the session cookie                                    |               |       yes |
| CONTENT_FOLDER_PATH        | The path to the local folder that contains the content of the playbook - a folder with several .md files. |               |       yes |
| CONTENT_FOLDER_BRANCH      | Branch to pull when updating the content folder from Github.                                              |               |       yes |
| WEBHOOK_SECRET             | Secret used by Github to authenticate when calling the content update endpoint.                           |               |       yes |

## Tailwind CSS and SCSS Setup

This project uses Tailwind CSS and SCSS for styling. Follow these steps to set up and build the CSS:

1. Install Node.js and Yarn

2. Install the required dependencies:

```
   yarn install
```

3. Build the CSS:

```
   yarn build
```

To watch for changes in your SCSS files and automatically build the CSS, run the following command:

```
   yarn watch
```

## Contributing

We welcome contributions to this project. If you find any issues, have any suggestions, or want to contribute code,
please feel free to open an issue or create a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [License](LICENSE.md) file for details.

[![Deploy](https://github.com/Vizzuality/playbook-app/actions/workflows/deploy.yml/badge.svg?branch=main)](https://github.com/Vizzuality/playbook-app/actions/workflows/deploy.yml)

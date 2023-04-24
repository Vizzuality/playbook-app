import os
from dotenv import load_dotenv

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
organization_domain = os.getenv('ORGANIZATION_DOMAIN')
github_repo_url = os.getenv('GITHUB_REPO_URL')
local_repo_path = os.getenv('LOCAL_REPO_PATH')
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
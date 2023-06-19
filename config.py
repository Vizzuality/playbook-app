import os
from dotenv import load_dotenv

load_dotenv()

google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
google_organization_domain = os.getenv('GOOGLE_ORGANIZATION_DOMAIN')
content_folder_path = os.getenv('CONTENT_FOLDER_PATH')
content_folder_branch = os.getenv('CONTENT_FOLDER_BRANCH')
webhook_secret = os.getenv('WEBHOOK_SECRET')

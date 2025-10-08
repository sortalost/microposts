import os

DEBUG = os.getenv("DEBUG") or "False"
USERNAME = os.getenv("username") or "admin"
PASSWORD = os.getenv("password") or "default"
SECRET_KEY = os.getenv("secret_key") or "secret123"

DATA_FILE = os.getenv("data_file") or "images.json" # where the data and image url will be stored on the other repo
GITHUB_REPO = os.getenv("github_repo")
GITHUB_REPO_BRANCH = os.getenv("github_repo_branch") or "master"
GITHUB_EMAIL = os.getenv("github_email")
GITHUB_USERNAME = os.getenv("github_username")
GITHUB_TOKEN = os.getenv("github_token")
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"

DISPLAY_NAME = os.getenv("display_name") or USERNAME
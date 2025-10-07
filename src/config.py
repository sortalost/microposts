import os

DEBUG = False
USERNAME = os.getenv("username") or "user"
PASSWORD = os.getenv("password") or "pswd"
SECRET_KEY = os.getenv("secret_key") or "secret123"

DATA_FILE = "images.json" # where the data and image url will be stored on the other repo
GITHUB_REPO = os.getenv("github_repo")
GITHUB_REPO_BRANCH = "master"
GITHUB_EMAIL = os.getenv("github_email")
GITHUB_USERNAME = os.getenv("github_username")
GITHUB_TOKEN = os.getenv("github_token")
GITHUB_API_URL = (
    "https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"
)

DISPLAY_NAME = os.getenv("display_name") or USERNAME
import os

DEBUG = os.getenv("DEBUG") or "False"
USERNAME = os.getenv("USERNAME") or "admin"
PASSWORD = os.getenv("PASSWORD") or "default"
SECRET_KEY = os.getenv("SECRET_KEY") or "secret123"

DATA_FILE = os.getenv("DATA_FILE") or "images.json"  # where the data and image URL will be stored on the other repo
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_REPO_BRANCH = os.getenv("GITHUB_REPO_BRANCH") or "master"
GITHUB_EMAIL = os.getenv("GITHUB_EMAIL")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={branch}"

DISPLAY_NAME = os.getenv("DISPLAY_NAME") or USERNAME

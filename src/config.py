import os

SECRET_KEY = os.getenv("secret_key") or "secret123"
DEBUG = True
USERNAME = os.getenv("username") or "maury"
PASSWORD = os.getenv("password") or "123"
DATA_FILE = "images.json" # where the data and image url will be stored on the other github
GITHUB_REPO = "temporary"
GITHUB_EMAIL = "sortalost@cock.li"
GITHUB_USERNAME = "sortalost"
GITHUB_TOKEN = os.getenv("github_token")
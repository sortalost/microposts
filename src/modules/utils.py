import os
import io
import json
import time
from github import Github, InputGitAuthor
from flask import session, flash, jsonify, request, redirect, url_for, current_app
from functools import wraps

class DB:
    def __init__(self, github_token: str, database_repo: str, author: tuple, branch: str = None):
        self.github = Github(github_token)
        self.key = github_token
        self.author = InputGitAuthor(name=author[0], email=author[1])
        self.repo = self.github.get_repo(f"{author[0]}/{database_repo}")
        if branch is None:
            self.branch = self.repo.get_branches()[0].name
        else:
            self.branch = self.repo.get_branch(branch=branch).name

    def save_remote_data(self, content, file_path, *, msg="site-upload", branch=None):
        if branch is None:
            try:
                self.repo.create_file(file_path, msg, str(content))
            except:
                sha = self.repo.get_contents(file_path, ref=self.branch).sha
                self.repo.update_file(file_path, msg, str(content), sha, branch=self.branch)
            return content
        try:
            self.repo.create_file(file_path, msg, str(content), branch=branch)
        except:
            sha = self.repo.get_contents(file_path, ref=branch).sha
            self.repo.update_file(file_path, msg, str(content), sha, branch=branch)
        return content

    def load_remote_data(self, file_path, *, eval_output=False, branch=None):
        if branch is None:
            con = self.repo.get_contents(file_path, ref=self.branch).decoded_content.decode("utf-8")
        else:
            con = self.repo.get_contents(file_path, ref=branch).decoded_content.decode("utf-8")
        if eval_output:
            return eval(con)
        return con

    def upload_to_github(self, file_storage, folder="uploads", branch=None):
        branch = branch or self.branch
        filename = file_storage.filename
        ext = os.path.splitext(filename)[1]
        name = os.path.splitext(filename)[0]
        timestamp = int(time.time())
        # unique_name = f"{name}_{timestamp}{ext}" # never mind the uniqueness
        unique_name = f"{name}{ext}"
        file_path = f"{folder}/{unique_name}"
        file_bytes = file_storage.read()
        msg = f"Upload image: {unique_name}"
        try:
            self.repo.create_file(file_path, msg, file_bytes, branch=branch)
        except Exception:
            sha = self.repo.get_contents(file_path, ref=branch).sha
            self.repo.update_file(file_path, msg, file_bytes, sha, branch=branch)
        user_repo = self.repo.full_name
        raw_url = f"https://raw.githubusercontent.com/{user_repo}/{branch}/{file_path}"
        return {"path": file_path, "url": raw_url, "name": unique_name, "timestamp": timestamp}


def get_db():
    return DB(
        github_token=current_app.config['GITHUB_TOKEN'],
        database_repo=current_app.config['GITHUB_REPO'],
        author=(current_app.config['GITHUB_USERNAME'], current_app.config['GITHUB_EMAIL'])
    )

def get_data():
    db = get_db()
    data = db.load_remote_data(current_app.config['DATA_FILE'], eval_output=True)
    data.sort(key=lambda x: x['display_datetime'][1], reverse=True)
    return data

def save_data(data):
    db = get_db()
    data_json = json.dumps(data, indent=4)
    return db.save_remote_data(data_json, current_app.config['DATA_FILE'])

def upload_image(file_storage):
    db = get_db()
    return db.upload_to_github(file_storage)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in"):
            if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify({"success": False, "message": "Login required"}), 401
            else:
                flash("Please login to access this page.", "error")
                return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def print_debug(string):
    if current_app.debug:
        print(f"[DEBUG] {string}")
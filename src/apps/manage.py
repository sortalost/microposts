import re
import html
import time
import json
import requests
from datetime import datetime
from .modules.utils import login_required, compress, db
from flask import Blueprint, render_template, request

status = Blueprint('status', __name__, url_prefix="/status")

def get_data():
    return db.load_remote_data('.json', eval_output=True)

def update_data(new_data):
    db.push_remote_data(json.dumps(new_data, indent=4), 'status.json')


@status.route("/image", methods=["GET", "POST"])
@login_required
def _image():
    url = None
    default_quality=50
    if request.method == "POST":
        msg = request.form.get('message')
        quality = request.form.get('quality',default_quality)
        file = request.files["file"]
        if file:
            files = {"files[]": (file.filename, file, file.mimetype)}
            r = requests.post(POMF, files=files)
            try:
                res = r.json()
                url = res["files"][0]["url"].replace('pomf2','pomf')
            except Exception:
                url = None
            if url:
                blob = get_blob()
                blob.setdefault("image", {})
                blob["image"][str(int(time.time()))] = url
                status_blob(blob)
    return render_template("status/image.html", url=url, default_quality=default_quality)


@status.route("/status", methods=["GET", "POST"])
@login_required
def _status():
    status = None
    if request.method == "POST":
        status = request.form.get("status")
        if status:
            blob = get_blob()
            blob.setdefault("status", {})
            blob["status"][str(int(time.time()))] = status.strip()
            status_blob(blob)
    return render_template("status/status.html", status=status)


@status.route("/")
def showstatus():
    blob = get_blob()
    terms = get_terms(blob)
    return render_template('status/show.html', terms=terms)


def _get():
    blob = get_blob()
    result = {}
    if "status" in blob and blob["status"]:
        latest_status_time = max(blob["status"].keys(), key=int)
        result["status"] = {
            "data": format_status(blob["status"][latest_status_time]),
            "time": latest_status_time
        }
    if "image" in blob and blob["image"]:
        latest_image_time = max(blob["image"].keys(), key=int)
        result["img"] = {
            "data": blob["image"][latest_image_time],
            "time": latest_image_time
        }
    return result


def format_status(text: str) -> str:
    """Format status lines for greentext, redtext, and quoting."""
    lines = text.splitlines()
    formatted = []
    for line in lines:
        safe_line = html.escape(line)
        if re.match(r"^>>\d+$", line.strip()):
            ts = line.strip()[2:]  # remove >>
            formatted.append(f"<a class='reply' href='#{ts}'>&gt;&gt;{ts}</a>")
        elif line.startswith(">"):
            formatted.append(f"<span class='greentext'>{safe_line}</span>")
        elif line.startswith("<"):
            formatted.append(f"<span class='redtext'>{safe_line}</span>")
        else:
            formatted.append(safe_line)
    return "<br>".join(formatted)


def get_terms(raw_data):
    """
    raw_data: dict loaded from db.load_remote_data('status.json', eval_output=True)
    Returns a list of 'terms' where each term is a dict:
        - ts: timestamp (int)
        - date_str: formatted timestamp string
        - statuses: list of status strings
        - images: list of image URLs
    """
    posts = []
    for ts, status in raw_data.get("status", {}).items():
        posts.append({"ts": int(ts), "type": "status", "content": format_status(status)})
    for ts, img in raw_data.get("image", {}).items():
        posts.append({"ts": int(ts), "type": "image", "content": img})

    posts.sort(key=lambda x: x["ts"])

    terms = []
    for post in posts:
        if not terms:
            terms.append({
                "ts": post["ts"],
                "statuses": [post["content"]] if post["type"] == "status" else [],
                "images": [post["content"]] if post["type"] == "image" else [],
                "date_str": datetime.utcfromtimestamp(post["ts"]).strftime("%Y/%m/%d(%a)%H:%M")
            })
            continue
        last = terms[-1]
        time_diff = abs(post["ts"] - last["ts"]) <= 60*0  # 10 min window
        if time_diff:
            if post["type"] == "status" and last["statuses"]:
                terms.append({
                    "ts": post["ts"],
                    "statuses": [post["content"]],
                    "images": [],
                    "date_str": datetime.utcfromtimestamp(post["ts"]).strftime("%Y/%m/%d(%a)%H:%M")
                })
            else:
                if post["type"] == "status":
                    last["statuses"].append(post["content"])
                else:
                    last["images"].append(post["content"])
        else:
            terms.append({
                "ts": post["ts"],
                "statuses": [post["content"]] if post["type"] == "status" else [],
                "images": [post["content"]] if post["type"] == "image" else [],
                "date_str": datetime.utcfromtimestamp(post["ts"]).strftime("%Y/%m/%d(%a)%H:%M")
            })
    return terms[::-1]  # newest first
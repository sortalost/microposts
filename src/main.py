import requests
import mimetypes
import traceback
from .modules import utils
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, url_for, session, Response, abort, jsonify


app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/")
def index():
    utils.print_debug("fetching")
    uploads = utils.get_data()
    utils.print_debug("fetched")
    utils.print_debug(uploads)
    uploads.sort(key=lambda x: (-x.get("pin", 0), -x["display_datetime"][1]))
    utils.print_debug("sorted")
    return render_template('index.html', uploads=uploads, user=app.config['DISPLAY_NAME'])


@app.route("/new", methods=["GET", "POST"])
@utils.login_required
def new():
    if request.method == "POST":
        file = request.files.get("file")
        desc = request.form.get("description", "")
        date_str = request.form.get("date")
        utils.print_debug(date_str)
        if date_str:
            display_datetime_ts = int(datetime.strptime(date_str, "%Y-%m-%dT%H:%M").timestamp())
        else:
            display_datetime_ts = int(datetime.now().timestamp())
        display_datetime_str = datetime.fromtimestamp(display_datetime_ts).strftime("%Y-%m-%d(%a)%H:%M")
        if not file:
            flash("No file uploaded", "error")
            return redirect(request.url)
        try:
            result = utils.upload_image(file)
            flash("File uploaded successfully!", "success")
            all_images = utils.get_data()
            entry = {
                "name": result['name'],
                "path": result['path'],
                "url": result['url'],
                "display_datetime": [display_datetime_str, display_datetime_ts],
                "uploaded_at": result['timestamp'],
                "description": desc,
                "pin":0
            }
            all_images.append(entry)
            utils.save_data(all_images)
            return redirect(url_for("new"))
        except Exception as e:
            flash(f"Upload failed: {e}", "error")
            return redirect(request.url)
    return render_template("new.html", today=datetime.now().strftime("%Y-%m-%dT%H:%M"))


@app.route("/edit/<filename>", methods=["POST"])
@utils.login_required
def edit(filename):
    new_desc = request.form.get("description", "").strip()
    display_dt_str = request.form.get("display_datetime", "").strip()
    if not new_desc:
        return jsonify({"success": False, "error": "Description cannot be empty"}), 400
    try:
        data = utils.get_data()
        found = False
        display_timestamp = None
        display_datetime_formatted = None
        if display_dt_str:
            dt_obj = datetime.strptime(display_dt_str, "%Y-%m-%dT%H:%M")
            display_timestamp = int(dt_obj.timestamp())
            display_datetime_formatted = dt_obj.strftime("%Y-%m-%d(%a)%H:%M")
        for item in data:
            if item["name"] == filename:
                item["description"] = new_desc
                if display_timestamp:
                    item["display_datetime"] = [display_datetime_formatted, display_timestamp]
                found = True
                break
        if not found:
            return jsonify({"success": False, "error": "File not found"}), 404
        utils.save_data(data)
        flash(f"Edited {filename} successfully!")
        return jsonify({
            "success": True,
            "description": new_desc,
            "display_datetime": display_datetime_formatted
        })
    except Exception as e:
        flash(f"Error occurred while editing {filename}. Check the console/logs.")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/delete/<filename>", methods=["POST"])
@utils.login_required
def delete(filename):
    try:
        utils.delete_post(filename)
        flash(f"Deleted {filename}", 'success')
        return jsonify({"success": True})
    except Exception as e:
        utils.print_debug(e)
        flash(f"Error while deleting {filename}. Check console/logs.", 'error')
        return jsonify({"success": False, "error": str(e)}), 400

    
@app.route("/pin/<filename>", methods=["POST"])
@utils.login_required
def pin(filename):
    data = utils.get_data()
    for item in data:
        if item["name"] == filename:
            item["pin"] = 0 if item.get("pin",0) else 1
            utils.save_data(data)
            return jsonify({"success": True, "pin": item["pin"]})
    return jsonify({"success": False, "error": "File not found"}), 404


@app.route("/images/<path:image_path>")
def proxy_image(image_path):
    headers = {
        "Authorization": f"token {app.config['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3.raw"
    }
    url = app.config['GITHUB_API_URL'].format(
        owner=app.config['GITHUB_USERNAME'],
        repo=app.config['GITHUB_REPO'],
        path=image_path,
        branch=app.config['GITHUB_REPO_BRANCH']
    )
    github_response = requests.get(url, headers=headers)
    if github_response.status_code != 200:
        abort(github_response.status_code)
    content_type, _ = mimetypes.guess_type(image_path)
    if content_type is None:
        content_type = "image/png"
    return Response(github_response.content, content_type=content_type)



@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.errorhandler(404)
def notfound(e):
    return render_template("404.html")


@app.errorhandler(500)
def servererror(e):
    message = "Internal server error. My bad </3"
    if app.debug or session.get('logged_in'):
        message = traceback.format_exc()
    return render_template("500.html", message=message)


@app.errorhandler(Exception)
def other_errors(e):
    code = getattr(e, "code", 500)
    if code in [404, 500]:
        return e
    flash(f"Error: {code}", category='error')
    return render_template("error.html", error=e, code=code), code


@app.route("/login", methods=["GET","POST"])
def login():
    if session.get("logged_in"):
        flash("Already logged in.")
        return redirect(url_for("index"))
    if request.method == "POST":
        if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
            flash("Logged in.", category='success')
            session['logged_in'] = True
            return redirect(url_for("index"))
        else:
            flash('Invalid username or password', category='error')
    return render_template("login.html")


@app.route("/logout")
@utils.login_required
def logout():
    session.clear()
    flash("Logged out.", category='error')
    return redirect(url_for('index'))


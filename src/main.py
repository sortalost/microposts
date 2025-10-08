import requests
import traceback
from .modules import utils
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, url_for, session, Response, abort


app = Flask(__name__)
app.config.from_pyfile("config.py")


@app.route("/")
def index():
    uploads = utils.get_data()
    return render_template('index.html', uploads=uploads, user=app.config['DISPLAY_NAME'])


@app.route("/dashboard")
@utils.login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/dashboard/new", methods=["GET", "POST"])
@utils.login_required
def dashboard_new():
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
                "description": desc
            }
            all_images.append(entry)
            utils.save_data(all_images)
            return redirect(url_for("dashboard_new"))
        except Exception as e:
            flash(f"Upload failed: {e}", "error")
            return redirect(request.url)
    return render_template("dashboard_new.html", today=datetime.now().strftime("%Y-%m-%dT%H:%M"))


@app.route("/dashboard/edit", methods=["GET", "POST"])
@utils.login_required
def dashboard_edit():
    return render_template("dashboard_edit.html")


@app.route("/dashboard/delete/<filename>", methods=["POST"])
@utils.login_required
def dashboard_delete(filename):
    try:
        utils.delete_post(filename)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


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
    if github_response.status_code == 200:
        content_type = github_response.headers.get("Content-Type", image_path.rsplit(".", 1)[-1].lower())
        return Response(github_response.content, content_type=content_type)
    else:
        abort(github_response.status_code)


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
    if app.debug:
        message = traceback.format_exc()
    return render_template("500.html", message=message)


@app.route("/login", methods=["GET","POST"])
def login():
    if session.get("logged_in"):
        flash("Already logged in.")
        return redirect(url_for("index"))
    if request.method == "POST":
        if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
            flash("Logged in.")
            session['logged_in'] = True
            return redirect(url_for("index"))
        else:
            flash('Invalid username or password')
    return render_template("login.html")


@app.route("/logout")
@utils.login_required
def logout():
    session.clear()
    flash("Logged out.")
    return redirect(url_for('index'))


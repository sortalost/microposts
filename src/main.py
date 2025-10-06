from .apps.modules import utils
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, url_for

app = Flask(__name__)

@app.route("/")
def index():
    terms = utils.get_data()
    return render_template('index.html', terms=terms)

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
        date = request.form.get("date") or datetime.now().strftime("%Y-%m-%d")
        if not file:
            flash("No file uploaded", "error")
            return redirect(request.url)
        try:
            utils.db.upload_to_github(file)

            flash("File uploaded successfully!", "success")
            return redirect(url_for("dashboard_new"))
        except Exception as e:
            flash(f"Upload failed: {e}", "error")
            return redirect(request.url)
    return render_template("dashboard_new.html", today=datetime.now().strftime("%Y-%m-%d"))


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.errorhandler(404)
def notfound(e):
    return render_template("404.html")


if __name__=="__main__":
    app.run()
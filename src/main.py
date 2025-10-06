from .apps.modules import utils
from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, url_for

app = Flask(__name__)
USERNAME = "test"
PASSWORD = "123"

@app.route("/")
def index():
    uploads = utils.get_data()
    return render_template('index.html', uploads=data)

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
        if date_str:
            display_datetime_ts = int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())
        else:
            display_datetime_ts = int(datetime.now().timestamp())
        display_datetime_str = datetime.fromtimestamp(display_datetime_ts).strftime("%Y-%m-%d(%a)%H:%M")
        if not file:
            flash("No file uploaded", "error")
            return redirect(request.url)
        try:
            result = utils.db.upload_to_github(file)
            flash("File uploaded successfully!", "success")
            all_images = utils.get_data()
            entry = {
                "name":result['name'],
                "path":result['path'],
                "url":result['url'],
                "display_datetime":[display_datetime_str, display_datetime_ts],
                "uploaded_at":result['timestamp']
            }
            all_images.append(entry)
            utils.save_data(data)
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

@app.route("/login", methods=["GET","POST"])
def login():
    if session.get("logged_in"):
        flash("Already logged in.")
        return redirect(url_for("index"))
    if request.method=="POST":
        if request.form['username']==USERNAME and request.form['password']==PASSWORD:
            flash("Logged in.")
            session['logged_in']==True
            return redirect(url_for("index"))
        else:
            flash('Invalid username or password')
    return render_template("login.html")


if __name__=="__main__":
    app.run(debug=True)
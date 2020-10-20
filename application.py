  
from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

from passlib.hash import pbkdf2_sha256
from io import BytesIO
import os, math, random

from forms_fiels import *
from models import *
from logic import *

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    
    return User.query.get(int(id))

@app.route("/", methods = ['GET', 'POST'])
def main():

    return render_template('main.html')

@app.route("/signup", methods = ['GET', 'POST'])
def signup():

    reg_form = Registration()

    if reg_form.validate_on_submit():
        
        email = reg_form.email.data
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_password = pbkdf2_sha256.hash(password)

        user = User(email = email, username = username, password = hashed_password)
        db.session.add(user)
        db.session.commit() 

        flash("Registered Successfully!!", 'success')

        return redirect(url_for('login'))

    return render_template('signup.html', form = reg_form)

@app.route("/login", methods = ['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.validate_on_submit():

        user_object = User.query.filter_by(username = login_form.username.data).first()
        login_user(user_object)

        flash("Login Successfull!!", 'success')
        return redirect(url_for('index'))

    return render_template("login.html", form = login_form)

@app.route("/logout", methods = ['GET', 'POST'])
def logout():

    if not current_user.is_authenticated:

        flash("Please Login!!", 'danger')
        return redirect(url_for('login'))

    logout_user()
    flash("Logged out successfully!!", 'success')

    return render_template("main.html")

@app.route("/index", methods = ['GET', 'POST'])
#@login_required
def index():

    if not current_user.is_authenticated:

        flash("Please Login!!", 'danger')
        return redirect(url_for('login'))

    up = Uploaddata()
    userid = current_user.get_id()
    user = User.query.filter_by(id = userid).first()
    user_name = user.username

    if up.validate_on_submit():

        userid = current_user.get_id()

        user = User.query.filter_by(id = userid).first()
        user_name = user.username

        ids = userid
        name = up.name.data
        title = up.title.data
        source = up.source.data
        duration = up.duration.data
        year = up.year.data
        files = request.files['data']

        user = User.query.filter_by(id = userid).first()
        TO = user.email

        send_mail_certificate(TO, EMAIL_ADDRESS, EMAIL_PASSWORD, name, title, source, duration, year)

        try:

            loads = Uploads(ids = ids, name = name, title = title, source = source, duration = duration, year = year, data = files.read())
            db.session.add(loads)
            db.session.commit()

            flash("Your certificate was uploaded successfully!!", 'success')
            return render_template("index.html", form = up, username = user_name)

        except:

            flash("Your certificate was not uploaded!!", 'danger')
            return render_template("index.html", form = up, username = user_name)

    return render_template("index.html", form = up, username = user_name)
    
@app.route("/download", methods = ['GET', 'POST'])
def download():

    if not current_user.is_authenticated:

        flash("Please Login!!", 'danger')
        return redirect(url_for('login'))

    download = Download()

    userid = current_user.get_id()
    user = User.query.filter_by(id = userid).first()
    user_name = user.username

    if download.validate_on_submit():

        try:

            userid = current_user.get_id()

            name = download.name.data
            title = download.title.data
            source = download.source.data

            file_data = Uploads.query.filter_by(ids = userid, name = name, title = title, source = source).first()

            flash("Download Successfull!!", 'success')

            return  send_file(BytesIO(file_data.data), attachment_filename = "{}_{}_{}.pdf".format(title, source, name), as_attachment = True)
            
        except:

            flash("Download Unsuccessfull!!", 'danger')
            return render_template("download.html", form = download, username = username)

    return render_template("download.html", form = download, username = user_name)

@app.route("/download/<name>/<title>/<source>")
def download_url(name, title, source):

    if not current_user.is_authenticated:

        flash("Please Login!!", 'danger')
        return redirect(url_for('login'))

    download = Download()

    userid = current_user.get_id()
    all_certs = Uploads.query.filter_by(ids = userid).all()

    user = User.query.filter_by(id = userid).first()
    user_name = user.username

    try:

        file_data = Uploads.query.filter_by(ids = userid, name = name, title = title, source = source).first()

        return  send_file(BytesIO(file_data.data), attachment_filename = "{}_{}_{}.pdf".format(title, source, name), as_attachment = True)
    except:

        flash("Download Unsuccessfull!!", 'danger')

        return render_template("all_certificates.html", certificates = all_certs, username = user_name)

@app.route("/reset", methods = ['GET', 'POST'])
def reset():

    if not current_user.is_authenticated:

        flash("Please Login!!", 'danger')
        return redirect(url_for('login'))

    reset_pass = change_pass()
    userid = current_user.get_id()

    user = User.query.filter_by(id = userid).first()
    user_name = user.username

    if reset_pass.validate_on_submit():

        userid = current_user.get_id()

        password = reset_pass.password.data
        confirm_password = reset_pass.confirm_password.data

        hashed_password = pbkdf2_sha256.hash(confirm_password)

        try:

            db.session.query(User).filter(User.id == userid).update({User.password: hashed_password}, synchronize_session=False)
            db.session.commit()

            user = User.query.filter_by(id = userid).first()

            TO = user.email

            send_mail_danger(TO, EMAIL_ADDRESS, EMAIL_PASSWORD)

            flash("Password Change Successfull!!", "success")
            return redirect(url_for("logout"))

        except:

            flash("Password Change Unsuccessfull!!", "danger")
            return render_template("reset.html", form = reset_pass, username = user_name)

    return render_template("reset.html", form = reset_pass, username = user_name)

@app.route("/forgot", methods = ["GET", "POST"])
def forgot():

    forgot_pass = forgot_password()
    login_form = LoginForm()

    if forgot_pass.validate_on_submit():

        email = forgot_pass.email.data
        TO = email
        
        user_email = User.query.filter_by(email = email).first()
        if (user_email):

            user = User.query.filter_by(email = email).first()

            username = user.username

            string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            password = "" 
            length = len(string) 
            for i in range(10):  
                password += string[math.floor(random.random() * length)] 

            hashed_password = pbkdf2_sha256.hash(password)

            db.session.query(User).filter(User.email == email).update({User.password: hashed_password}, synchronize_session=False)
            db.session.commit()

            send_mail(TO, EMAIL_ADDRESS, EMAIL_PASSWORD, username, password)

            flash("Temporary Password has been sent to your registered email", "success")

            return render_template("login.html", form = login_form)
        else:
            flash("This email is not registered", "danger")
            return render_template("forgot_password.html", form = forgot_pass)

    return render_template("forgot_password.html", form = forgot_pass)

@app.route("/all_certificates", methods = ["GET", "POST"])
def all_certificates():

    # if not current_user.is_authenticated:

    #     flash("Please Login", 'danger')
    #     return redirect(url_for('login'))

    userid = current_user.get_id()

    all_certs = Uploads.query.filter_by(ids = userid).all()

    userid = current_user.get_id()

    user = User.query.filter_by(id = userid).first()
    user_name = user.username

    return render_template("all_certificates.html", certificates = all_certs, username = user_name)
    
if __name__ == "__main__":

    app.run(debug = True)
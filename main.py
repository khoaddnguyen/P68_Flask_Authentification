from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy()
db.init_app(app)


# CREATE TABLE IN DB
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template("index.html")


# Register a new user and add them your database
# take the information they have inputted in register.html form
# and create a new User object with email, name and password to save into the users.db
# Once the user is registered, send them straight to the secrets.html
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        # Hash and salt the password entered by user
        hash_and_salted_pw = generate_password_hash(
            request.form.get("password"),
            method="pbkdf2:sha256",
            salt_length=8
        )

        new_user = User(
            email=request.form.get("email"),
            name=request.form.get("name"),
            password=hash_and_salted_pw
            # password=request.form.get("password")
        )

        db.session.add(new_user)
        db.session.commit()

        return render_template("secrets.html", name=request.form.get("name"))

    return render_template("register.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    return render_template("secrets.html")


@app.route('/logout')
def logout():
    pass


@app.route('/download')
def download():
    return send_from_directory("static", path="files/cheat_sheet.pdf")


if __name__ == "__main__":
    app.run(debug=True)

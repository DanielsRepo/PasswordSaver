from flask import redirect, render_template, url_for, flash
from .forms import SavePasswordForm, LoginForm, RegistrationForm
from . import app, db
from .models import Password
from flask_login import current_user, login_user, logout_user
from .models import User
from collections import namedtuple


@app.route("/", methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    else:
        form = SavePasswordForm()

        if form.validate_on_submit():
            password = Password(service=form.service.data, user=current_user.id)
            password.save_password(form.password.data)

            db.session.add(password)
            db.session.commit()

            return redirect("/")

        password_tuple = namedtuple("password", ["id", "decrypted"])
        passwords = {
            password.service: password_tuple(
                id=password.id,
                decrypted=password.decrypt_password(password.password),
            )
            for password in Password.query.filter_by(user=current_user.id)
        }

        return render_template("index.html", form=form, passwords=passwords)


@app.route("/delete/<int:password_id>", methods=["GET"])
def delete(password_id):
    Password.delete_password(password_id)
    db.session.commit()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("registration.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        else:
            login_user(user)
            return redirect(url_for("index"))

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

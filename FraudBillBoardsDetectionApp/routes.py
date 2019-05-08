from flask import render_template, redirect, url_for
from FraudBillBoardsDetectionApp import fraudBillBoardsDetectionApp
from FraudBillBoardsDetectionApp.forms import LoginForm


@fraudBillBoardsDetectionApp.route("/home")
def home_page():
    return render_template("home.html", title="LandingPage")


@fraudBillBoardsDetectionApp.route("/about_us")
def about_us():
    return "about us"


@fraudBillBoardsDetectionApp.route("/register")
def register():
    return "register"


@fraudBillBoardsDetectionApp.route("/login_user")
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        redirect(url_for("home_page"))
    return render_template("user_login.html", title="LoginPage", form=form)


@fraudBillBoardsDetectionApp.route("/login_admin")
def login_admin():
    return "login admin"

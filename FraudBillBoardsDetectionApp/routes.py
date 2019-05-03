from flask import render_template
from FraudBillBoardsDetectionApp import fraudBillBoardsDetectionApp


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
    return "login user"


@fraudBillBoardsDetectionApp.route("/login_admin")
def login_admin():
    return "login admin"

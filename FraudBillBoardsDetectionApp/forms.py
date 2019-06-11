from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, DateField, IntegerField, FileField
from wtforms.validators import DataRequired


class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("SignIn")


class RegisterForm(FlaskForm):
    email_id = StringField("Email_Id", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    organisation_name = StringField("Organisation_name", validators=[DataRequired()])
    address = StringField("address", validators=[DataRequired()])
    contact_number = IntegerField("Contact_number", validators=[DataRequired()])
    submit = SubmitField("Register")


class AdminLoginForm(FlaskForm):
    admin_username = StringField("Admin_username", validators=[DataRequired()])
    admin_password = PasswordField("Admin_password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("SignIn")


class BuyBillboardForm(FlaskForm):
    start_date = DateField("Start_Date", validators=[DataRequired()])
    end_date = DateField("End_Date", validators=[DataRequired()])
    submit = SubmitField("Submit buy request")


class BillboardSearch(FlaskForm):
    area = StringField("Area", validators=[DataRequired()])
    submit = SubmitField("Search billboards")


class PaymentForm(FlaskForm):
    submit = SubmitField("Pay")


class AddBillboardForm(FlaskForm):
    area = StringField("Billboard_Area", validators=[DataRequired()])
    billboard_dimensions = StringField("Billboard_Dimensions", validators=[DataRequired()])
    cost_per_day = IntegerField("Cost_per_Day", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Add billboard")


class ApproveUserTransactionForm(FlaskForm):
    submit = SubmitField("Approve")


class UploadImageForm(FlaskForm):
    submit = SubmitField("Upload image")



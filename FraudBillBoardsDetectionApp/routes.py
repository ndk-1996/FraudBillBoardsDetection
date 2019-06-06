from flask import render_template, redirect, url_for, session
from FraudBillBoardsDetectionApp import fraudBillBoardsDetectionApp
from FraudBillBoardsDetectionApp.forms import UserLoginForm, RegisterForm, AdminLoginForm, BillboardSearch, BuyBillboardForm, PaymentForm
from FraudBillBoardsDetectionApp.data_access_objects.user_dao import UserDAO
from FraudBillBoardsDetectionApp.data_access_objects.transactions_dao import TransactionsDAO
from FraudBillBoardsDetectionApp.data_access_objects.billboard_dao import BillBoardDAO
from FraudBillBoardsDetectionApp.constants import application_constants
from FraudBillBoardsDetectionApp.find_available_dates import FindAvailableDates
from datetime import date


@fraudBillBoardsDetectionApp.route("/home")
@fraudBillBoardsDetectionApp.route("/<string:user_id>/home")
def home_page(user_id=None):
    return render_template("home.html", title="HomePage", user_id=user_id)


@fraudBillBoardsDetectionApp.route("/about_us")
def about_us():
    return "about us"


@fraudBillBoardsDetectionApp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        insert_query = '''insert into user (email_id, organization_name, address, contact_number, password) values (%s ,%s, %s, %s, %s)'''
        check_user_query = '''select email_id from user where email_id = %s'''
        params_insert_query = (form.email_id.data, form.organisation_name.data, form.address.data, form.contact_number.data, form.password.data)
        params_check_user_query = (form.email_id.data,)
        user_dao = UserDAO()

        if user_dao.is_user_registered(check_user_query, params_check_user_query):
            err_message = 'given user is already registered'
            form.email_id.errors.append(err_message)
            return render_template("user_register.html", title="RegisterPage", form=form)

        user_dao.save_data(insert_query, params_insert_query)
        return redirect(url_for("home_page"))
    return render_template("user_register.html", title="RegisterPage", form=form)


@fraudBillBoardsDetectionApp.route("/login_user", methods=['GET', 'POST'])
def login_user():
    form = UserLoginForm()
    if form.validate_on_submit():
        user_dao = UserDAO()
        check_user_query = '''select email_id, password from user where email_id = %s'''
        params_check_user_query = (form.email_id.data,)
        if user_dao.is_user_registered(check_user_query, params_check_user_query):
            if user_dao.check_for_password_macth(check_user_query, params_check_user_query, form.password.data):
                session[form.username.data] = form.username.data
                return redirect(url_for("user_page", username=form.username.data))
            err_message = "please enter correct credentials"
            form.submit.errors.append(err_message)
            return render_template("user_login.html", title="UserLoginPage", form=form)

        err_message = "please enter correct credentials"
        form.submit.errors.append(err_message)
        return render_template("user_login.html", title="UserLoginPage", form=form)
    return render_template("user_login.html", title="UserLoginPage", form=form)


@fraudBillBoardsDetectionApp.route("/login_admin", methods=['GET', 'POST'])
def login_admin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        if form.admin_username.data == application_constants['admin_username'] and form.admin_password.data == application_constants['admin_password']:
            session[form.admin_username.data] = form.admin_username.data
            return 'logged_in successfully'
        err_message = "please enter correct credentials"
        form.submit.errors.append(err_message)
        return render_template("admin_login.html", title="AdminLoginPage", form=form)
    return render_template("admin_login.html", title="AdminLoginPage", form=form)


@fraudBillBoardsDetectionApp.route("/<string:username>/user_page")
def user_page(username):
    if username in session:
        return render_template("user_page.html", title="UserPage", username=session[username])
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/logout_user")
def logout_user(user_id):
    session.pop(user_id, None)
    return user_id + "logged_out successfully"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/logout_admin")
def logout_admin(user_id):
    session.pop(user_id, None)
    return user_id + "logged_out successfully"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/user_transactions")
def user_transactions(user_id):
    if user_id in session:
        transaction_dao = TransactionsDAO()
        transaction_query = '''select * from transactions t, billboard b where 
        t.billboard_id = b.billboard_id and t.email_id = %s'''
        params_transaction_query = (user_id,)
        transactions_list = transaction_dao.get_transactions(transaction_query, params_transaction_query)
        return render_template("user_transactions.html", title="UserTransactions", transactions_list=transactions_list, user_id=user_id)
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/search_billboards", methods=['GET', 'POST'])
def search_billboards(user_id):
    if user_id in session:
        form = BillboardSearch()
        if form.validate_on_submit():
            billboard_dao = BillBoardDAO()
            billboard_query = '''select * from billboard where area = %s'''
            params_billboard_query = (form.area.data,)
            billboards_list = billboard_dao.get_billboards(billboard_query, params_billboard_query)
            if len(billboards_list) != 0:
                return redirect(url_for("select_billboard", user_id=user_id, area=form.area.data))
            else:
                err_message = "there are no billboards with the given region, please change the region!"
                form.submit.errors.append(err_message)
                return render_template("search_billboard.html", title="SearchBillboard", user_id=user_id, form=form)
        return render_template("search_billboard.html", title="SearchBillboard", user_id=user_id, form=form)
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/<string:area>/select_billboard")
def select_billboard(user_id, area):
    if user_id in session:
        billboard_dao = BillBoardDAO()
        billboard_query = '''select * from billboard where area = %s'''
        params_billboard_query = (area,)
        billboards_list = billboard_dao.get_billboards(billboard_query, params_billboard_query)
        return render_template("select_billboard.html", title="SelectBillboard", user_id=user_id, billboards_list=billboards_list, area=area)
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/<string:area>/<int:billboard_id>/buy_billboard", methods=['GET', 'POST'])
def buy_billboard(user_id, area, billboard_id):
    if user_id in session:
        months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER',
                  'NOVEMBER', 'DECEMBER']
        week = ['mon', 'tue', 'wed', 'thurs', 'fri', 'sat', 'sun']
        form = BuyBillboardForm()
        transactions_dao = TransactionsDAO()
        find_available_dates = FindAvailableDates()
        find_transactions_of_current_year_query = '''select booking_start_date, booking_end_date from transactions where 
        year(booking_start_date) = year(curdate()) and year(booking_end_date) = year(curdate()) and billboard_id = %s'''
        params_find_transactions_of_current_year_query = (billboard_id,)
        blocked_days = transactions_dao.find_transactions_of_current_year(find_transactions_of_current_year_query,
                                                                          params_find_transactions_of_current_year_query)
        calender = find_available_dates.add_blocked_days_to_calender(blocked_days, '-')
        calender_view = find_available_dates.create_calender_view()
        if form.validate_on_submit():
            no_of_days = find_available_dates.find_no_of_days(form.start_date.data, form.end_date.data, '-')
            today = str(date.today())
            insert_new_transaction_query = '''insert into transactions (transaction_id, transaction_date, email_id, 
            booking_start_date, booking_end_date, status, payment_status, billboard_id) values (%s, %s, %s, %s, 
            %s, %s, %s, %s)'''
            new_transaction_id_query = '''select max(transaction_id) from transactions'''
            params_new_transaction_id_query = ()
            transaction_id = transactions_dao.get_new_transaction_id(new_transaction_id_query,
                                                                     params_new_transaction_id_query)
            status = "AWAITING APPROVAL"
            payment_status = "IN PROGRESS"
            params_insert_new_transaction_query = (transaction_id, today, user_id, form.start_date.data,
                                                   form.end_date.data, status, payment_status, billboard_id)
            transactions_dao.insert_new_transaction(insert_new_transaction_query, params_insert_new_transaction_query)
            redirect(url_for("payment_page", user_id=user_id, transactions_id=transaction_id, billboard_id=billboard_id))
        return render_template("buy_billboard.html", title="BuyBillboard", calender_view=calender_view, months=months,
                               user_id=user_id, week=week,)
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/<int:transaction_id>/<int:billboard_id>/payment_page", methods=['GET', 'POST'])
def payment_page(user_id, transaction_id, billboard_id):
    if user_id in session:
        billboard_dao = BillBoardDAO()
        transaction_dao = TransactionsDAO()
        find_available_dates = FindAvailableDates()
        form = PaymentForm()
        billboard_query = '''select * from billboard where billboard_id = %s'''
        params_billboard_query = (billboard_id,)
        billboards_list = billboard_dao.get_billboards(billboard_query, params_billboard_query)
        transaction_dates_query = '''select booking_start_date, booking_end_date 
        from transaction where transaction_id = %s'''
        params_transaction_dates_query = (transaction_id,)
        dates = transaction_dao.find_transacton_dates(transaction_dates_query, params_transaction_dates_query)
        no_of_days = find_available_dates.find_no_of_days(dates[0], dates[1])
        if form.validate_on_submit():
            transaction_dao = TransactionsDAO()
            update_payment_status_query = '''update transactions set payment_status = %s where transaction_id = %s'''
            params_update_payment_status_query = ("SUCCESS", transaction_id)
            transaction_dao.update_payment_status(update_payment_status_query, params_update_payment_status_query)
            return "Payment Done!"
        return render_template("payment_page.html", title="PaymentPage", billboards_list=billboards_list,
                               no_of_days=no_of_days, dates=dates)
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/payment_in_progress_transactions")
def payment_in_progress_transactions(user_id):
    if user_id in session:
        transaction_dao = TransactionsDAO()
        payment_in_progress_transaction_query = '''select * from transactions t, billboard b 
        where t.billboard_id = b.billboard_id and t.email_id = %s and t.payment_status = %s'''
        params_payment_in_progress_transaction_query = (user_id, "IN PROGRESS")
        transactions_list = transaction_dao.get_payment_in_progress_transactions(payment_in_progress_transaction_query,
                                                                                 params_payment_in_progress_transaction_query)
        return render_template("payment_in_progress_transactions.html", title="PaymentInProgressTransactions", transactions_list=transactions_list,
                               user_id=user_id)
    else:
        return "access denied, you must be logged in to access this page"


from flask import render_template, redirect, url_for, session, request
from FraudBillBoardsDetectionApp import fraudBillBoardsDetectionApp
from FraudBillBoardsDetectionApp.forms import UserLoginForm, RegisterForm, AdminLoginForm, BillboardSearch, BuyBillboardForm, PaymentForm, AddBillboardForm, ApproveUserTransactionForm, UploadImageForm
from FraudBillBoardsDetectionApp.data_access_objects.user_dao import UserDAO
from FraudBillBoardsDetectionApp.data_access_objects.transactions_dao import TransactionsDAO
from FraudBillBoardsDetectionApp.data_access_objects.billboard_dao import BillBoardDAO
from FraudBillBoardsDetectionApp.data_access_objects.region_dao import RegionDAO
from FraudBillBoardsDetectionApp.data_access_objects.notifications_dao import NotificationsDAO
from FraudBillBoardsDetectionApp.data_access_objects.images_dao import ImagesDAO
from FraudBillBoardsDetectionApp.constants import application_constants
from FraudBillBoardsDetectionApp.find_available_dates import FindAvailableDates
from datetime import date
from text_detection_and_recognition.text_recognition import start_ocr_job
from FraudBillBoardsDetectionApp import string_matching_kmp
import cv2


@fraudBillBoardsDetectionApp.route("/home")
def home():
    return render_template("home.html", title="HomePage")


@fraudBillBoardsDetectionApp.route("/user_home")
@fraudBillBoardsDetectionApp.route("/<string:user_id>/user_home")
def user_home_page(user_id=None):
    if user_id is not None:
        if user_id in session:
            user_id = user_id
        else:
            user_id = None

    if user_id is None:
        session.clear()

    return render_template("user_home.html", title="UserHomePage", user_id=user_id)


@fraudBillBoardsDetectionApp.route("/admin_home")
@fraudBillBoardsDetectionApp.route("/<string:admin_id>/admin_home")
def admin_home_page(admin_id=None):
    if admin_id is not None:
        if admin_id in session:
            admin_id = admin_id
        else:
            admin_id = None

    if admin_id is None:
        session.clear()

    return render_template("admin_home.html", title="AdminHomePage", admin_id=admin_id)


@fraudBillBoardsDetectionApp.route("/about_us")
def about_us():
    return "about us"


@fraudBillBoardsDetectionApp.route("/register", methods=["GET", "POST"])
@fraudBillBoardsDetectionApp.route("/<string:user_id>/register", methods=['GET', 'POST'])
def register(user_id=None):
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
            if user_id is not None and user_id in session:
                return render_template("user_register.html", title="RegisterPage", form=form, user_id=user_id)
            else:
                return render_template("user_register.html", title="RegisterPage", form=form, user_id=None)

        user_dao.save_data(insert_query, params_insert_query)
        if user_id is None or user_id not in session:
            return redirect(url_for("user_home_page"))
        else:
            return redirect(url_for("user_home_page", user_id=user_id))
    if user_id is not None and user_id in session:
        return render_template("user_register.html", title="RegisterPage", form=form, user_id=user_id)
    else:
        return render_template("user_register.html", title="RegisterPage", form=form, user_id=None)


@fraudBillBoardsDetectionApp.route("/login_user", methods=['GET', 'POST'])
def login_user():
    form = UserLoginForm()
    if form.validate_on_submit():
        user_dao = UserDAO()
        check_user_query = '''select email_id, password from user where email_id = %s'''
        params_check_user_query = (form.username.data,)
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
            return redirect(url_for("admin_page", admin_id=form.admin_username.data))
        err_message = "please enter correct credentials"
        form.submit.errors.append(err_message)
        return render_template("admin_login.html", title="AdminLoginPage", form=form)
    return render_template("admin_login.html", title="AdminLoginPage", form=form)


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/admin_page")
def admin_page(admin_id):
    if admin_id in session:
        return render_template("admin_page.html", title="AdminPage", admin_id=session[admin_id])
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:username>/user_page")
def user_page(username):
    if username in session:
        return render_template("user_page.html", title="UserPage", username=session[username])
    else:
        return "access denied, you must be logged in to access this page"


@fraudBillBoardsDetectionApp.route("/<string:user_id>/logout_user")
def logout_user(user_id):
    session.pop(user_id, None)
    return "<b>" + user_id + "</b>" + " logged_out successfully"


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/logout_admin")
def logout_admin(admin_id):
    session.pop(admin_id, None)
    return "<b>" + admin_id + "</b>" + " logged_out successfully"


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
        region_dao = RegionDAO()
        billboard_regions_query = '''select region from billboard_regions'''
        params_billboard_regions_query = ()
        regions_list = region_dao.get_regions(billboard_regions_query, params_billboard_regions_query)
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
                return render_template("search_billboard.html", title="SearchBillboard", user_id=user_id, regions_list=regions_list, form=form)
        return render_template("search_billboard.html", title="SearchBillboard", user_id=user_id, regions_list=regions_list, form=form)
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
        week = ['mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun']
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
        current_year = application_constants['current_year']
        if form.validate_on_submit():
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
            return redirect(url_for("payment_page", user_id=user_id, transaction_id=transaction_id, billboard_id=billboard_id))
        return render_template("buy_billboard.html", title="BuyBillboard", calender_view=calender_view, months=months,
                               user_id=user_id, week=week, current_year=current_year, form=form)
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
        from transactions where transaction_id = %s'''
        params_transaction_dates_query = (transaction_id,)
        dates = transaction_dao.find_transacton_dates(transaction_dates_query, params_transaction_dates_query)
        no_of_days = find_available_dates.find_no_of_days(dates[0], dates[1], '-')
        if form.validate_on_submit():
            update_payment_status_query = '''update transactions set payment_status = %s where transaction_id = %s'''
            params_update_payment_status_query = ("SUCCESS", transaction_id)
            transaction_dao.update_payment_status(update_payment_status_query, params_update_payment_status_query)
            return "Payment Done!"
        return render_template("payment_page.html", title="PaymentPage", billboards_list=billboards_list,
                               no_of_days=no_of_days, dates=dates, user_id=user_id, form=form)
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


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/add_billboard", methods=['GET', 'POST'])
def add_billboard(admin_id):
    if admin_id in session:
        form = AddBillboardForm()
        region_dao = RegionDAO()
        billboard_regions_query = '''select region from billboard_regions'''
        params_billboard_regions_query = ()
        regions_list = region_dao.get_regions(billboard_regions_query, params_billboard_regions_query)
        if form.validate_on_submit():
            billboard_dao = BillBoardDAO()
            new_billboard_id_query = '''select max(billboard_id) from billboard'''
            params_new_billboard_id_query = ()
            new_billboard_id = billboard_dao.get_new_billboard_id(new_billboard_id_query, params_new_billboard_id_query)
            add_billboard_query = '''insert into billboard (billboard_id, area, 
            billboard_dimensions, cost_per_day, address) values (%s, %s, %s, %s, %s)'''
            params_add_billboard_query = (new_billboard_id, form.area.data, form.billboard_dimensions.data,
                                          form.cost_per_day.data, form.address.data)
            billboard_dao.add_billboard(add_billboard_query, params_add_billboard_query)
            return "new billboard added!"
        return render_template("add_billboard.html", title="AddNewBillboard", admin_id=admin_id, regions_list=regions_list, form=form)
    else:
        return "access denied, you must be logged in as admin to access this page"


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/unapproved_user_transactions")
def unapproved_user_transactions(admin_id):
    if admin_id in session:
        transaction_dao = TransactionsDAO()
        unapproved_transactions_query = '''select * from transactions t, billboard b 
        where t.billboard_id = b.billboard_id and t.status = %s'''
        params_unapproved_transactions_query = ("AWAITING APPROVAL",)
        unapproved_transactions_list = transaction_dao.get_unapproved_transactions(unapproved_transactions_query,
                                                                                   params_unapproved_transactions_query)
        return render_template("unapproved_user_transactions.html", title="UnApprovedUserTransactions", admin_id=admin_id,
                               unapproved_transactions_list=unapproved_transactions_list)
    else:
        return "access denied, you must be logged in as admin to access this page"


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/approved_user_transactions")
def approved_user_transactions(admin_id):
    if admin_id in session:
        transaction_dao = TransactionsDAO()
        approved_transactions_query = '''select * from transactions t, billboard b 
        where t.billboard_id = b.billboard_id and t.status = %s'''
        params_approved_transactions_query = ("APPROVED",)
        approved_transactions_list = transaction_dao.get_approved_transactions(approved_transactions_query,
                                                                                   params_approved_transactions_query)
        return render_template("approved_user_transactions.html", title="ApprovedUserTransactions", admin_id=admin_id,
                               approved_transactions_list=approved_transactions_list)
    else:
        return "access denied, you must be logged in as admin to access this page"


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/<int:billboard_id>/upload_image_and_run_ocr", methods=['GET', 'POST'])
def upload_image_and_run_ocr(admin_id, billboard_id):
    if admin_id in session:
        form = UploadImageForm()
        if form.validate_on_submit():
            transaction_dao = TransactionsDAO()
            notification_dao = NotificationsDAO()
            today = str(date.today())
            image_dao = ImagesDAO()
            new_image_id_query = '''select max(img_id) from images'''
            params_new_image_id_query = ()
            new_imd_id = image_dao.get_new_image_id(new_image_id_query, params_new_image_id_query)
            insert_image_query = '''insert into images (img_id, img_upload_date, img_location, billboard_id) 
            values (%s, %s, %s, %s)'''
            if 'file' not in request.files:
                print("tezt")
                err_msg = 'Please choose the image file'
                return render_template("upload_image_and_run_ocr.html", title="UploadImage", admin_id=admin_id,
                                       billboard_id=billboard_id, form=form, err_msg=err_msg)
            f = request.files['file']
            print(f.filename)
            filename_splitted = f.filename.split('.')
            extension = filename_splitted[1]
            if f.filename == '':
                err_msg = 'Please choose the image file'
                return render_template("upload_image_and_run_ocr.html", title="UploadImage", admin_id=admin_id,
                                       billboard_id=billboard_id, form=form, err_msg=err_msg)
            f.filename = 'image' + str(new_imd_id) + '.' + extension
            print(f.filename)
            f.save(application_constants['upload_folder'] + f.filename)
            args_for_ocr_job = dict()
            args_for_ocr_job["image"] = application_constants['upload_folder'] + f.filename
            image = cv2.imread(args_for_ocr_job["image"])
            (origH, origW) = image.shape[:2]
            origH = (origH // 32) * 32
            origW = (origW // 32) * 32

            print(origW, origH)
            args_for_ocr_job["east"] = application_constants['east_text_detector_location']
            args_for_ocr_job["min_confidence"] = 0.3
            args_for_ocr_job["height"] = origH
            args_for_ocr_job["width"] = origW
            args_for_ocr_job["padding"] = 0.04
            params_insert_image_query = (new_imd_id, today, application_constants['upload_folder'] + f.filename, billboard_id)
            image_dao.save_new_image(insert_image_query, params_insert_image_query)
            new_notification_id_query = '''select max(notification_id) from notifications'''
            params_new_notification_id_query = ()
            new_notification_id = notification_dao.get_new_notification_id(new_notification_id_query, params_new_notification_id_query)
            insert_notification_query = '''insert into notifications (notification_id, img_id, content, ocr_job_finished_or_not, processed_date, ocred_text, expected_organization_name) 
            values (%s, %s, %s, %s, %s, %s, %s)'''
            params_insert_notification_query = (new_notification_id, new_imd_id, None, 'f', today, None, None)
            notification_dao.save_notification(insert_notification_query, params_insert_notification_query)

            text_detected = start_ocr_job(args_for_ocr_job)

            get_organisation_name_query = '''select u.organization_name from user u, transactions t 
            where u.email_id = t.email_id and t.billboard_id = %s and %s between t.booking_start_date and t.booking_end_date'''
            params_get_organisation_name_query = (billboard_id, today)
            organisation_name = transaction_dao.get_organisation_name_for_today_date(get_organisation_name_query, params_get_organisation_name_query)
            print(organisation_name)
            all_text_detected = ''

            for text in text_detected:
                formatted_text = ''
                for i in range(len(text)):
                    ch_ascii = ord(text[i])
                    if (ch_ascii >= ord('a') and ch_ascii <= ord('z')) or (ch_ascii >= ord('A') and ch_ascii <= ord('Z')):
                        formatted_text = formatted_text + text[i]

                all_text_detected = all_text_detected + formatted_text

            found = True
            if organisation_name is not None:
                organisation_name_splitted = str(organisation_name[0]).split(' ')
                for string in organisation_name_splitted:
                    found = string_matching_kmp.KMPSearch(string.lower(), all_text_detected.lower())
                    print(string.lower(), all_text_detected.lower(), found)

            if found is True and organisation_name is not None:
                content = "ocr job ran successfully and the given user has permissions to put up the billboard"
            else:
                content = "ocr job ran successfully and the given user doesn't have permissions to put up the billboard"
            ocred_text = ''
            for text in text_detected:
                ocred_text = ocred_text + text
                ocred_text = ocred_text + ', '
            update_notification_query = '''update notifications 
            set content = %s, ocr_job_finished_or_not = %s, ocred_text = %s, expected_organization_name = %s where notification_id = %s'''
            if organisation_name is not None:
                params_update_notification_query = (content, 't', ocred_text, organisation_name[0], new_notification_id)
            else:
                params_update_notification_query = (content, 't', ocred_text, None, new_notification_id)
            notification_dao.save_notification(update_notification_query, params_update_notification_query)

            return content
        return render_template("upload_image_and_run_ocr.html", title="UploadImage", admin_id=admin_id, billboard_id=billboard_id, form=form)


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/all_notifications")
def all_notifications(admin_id):
    if admin_id in session:
        notification_dao = NotificationsDAO()
        get_notifications_query = '''select * from notifications'''
        params_get_notifications_query = ()
        notifications_list = notification_dao.get_notifications(get_notifications_query, params_get_notifications_query)
        return render_template("all_notifications.html", title="Notifications", admin_id=admin_id, notifications_list=notifications_list)
    else:
        return "access denied, you must be logged in as admin to access this page"


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/<int:transaction_id>/approve_user_transactions", methods=['GET', 'POST'])
def approve_user_transactions(admin_id, transaction_id):
    if admin_id in session:
        form = ApproveUserTransactionForm()
        transaction_dao = TransactionsDAO()
        transaction_query = '''select * from transactions where transaction_id = %s'''
        params_transaction_query = (transaction_id,)
        transaction = transaction_dao.get_transactions(transaction_query, params_transaction_query)
        if form.validate_on_submit():
            update_approval_status_query = '''update transactions set status = %s where transaction_id = %s'''
            params_update_approval_status_query = ("APPROVED", transaction_id)
            transaction_dao.update_approval_status(update_approval_status_query, params_update_approval_status_query)
            return "The transaction with transaction_id = " + str(transaction_id) + " is approved!"
        return render_template("approve_user_transactions.html", title="ApproveUserTransaction", admin_id=admin_id,
                               transaction_id=transaction_id, transaction=transaction, form=form)
    else:
        return "access denied, you must be logged in as admin to access this page"


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/search_billboards_for_ocr", methods=['GET', 'POST'])
def search_billboards_for_ocr(admin_id):
    if admin_id in session:
        form = BillboardSearch()
        region_dao = RegionDAO()
        billboard_regions_query = '''select region from billboard_regions'''
        params_billboard_regions_query = ()
        regions_list = region_dao.get_regions(billboard_regions_query, params_billboard_regions_query)
        if form.validate_on_submit():
            billboard_dao = BillBoardDAO()
            billboard_query = '''select * from billboard where area = %s'''
            params_billboard_query = (form.area.data,)
            billboards_list = billboard_dao.get_billboards(billboard_query, params_billboard_query)
            if len(billboards_list) != 0:
                return redirect(url_for("select_billboard_for_ocr", admin_id=admin_id, area=form.area.data))
            else:
                err_message = "there are no billboards with the given region, please change the region!"
                form.submit.errors.append(err_message)
                return render_template("search_billboards_for_ocr.html", title="SearchBillboard", admin_id=admin_id, regions_list=regions_list, form=form)
        return render_template("search_billboards_for_ocr.html", title="SearchBillboard", admin_id=admin_id, regions_list=regions_list, form=form)
    else:
        return "access denied, you must be logged in as admin to access this page"


@fraudBillBoardsDetectionApp.route("/<string:admin_id>/<string:area>/select_billboard_for_ocr")
def select_billboard_for_ocr(admin_id, area):
    if admin_id in session:
        billboard_dao = BillBoardDAO()
        billboard_query = '''select * from billboard where area = %s'''
        params_billboard_query = (area,)
        billboards_list = billboard_dao.get_billboards(billboard_query, params_billboard_query)
        return render_template("select_billboard_for_ocr.html", title="SelectBillboard", admin_id=admin_id, billboards_list=billboards_list, area=area)
    else:
        return "access denied, you must be logged in as admin to access this page"

import mysql.connector
from FraudBillBoardsDetectionApp.constants import application_constants


class UserDAO(object):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=application_constants['host'],
            user=application_constants['user'],
            passwd=application_constants['passwd'],
            database=application_constants['database']
        )

        self.cursor = self.mydb.cursor()

    def load_data(self, sql_query, values):
        self.cursor.execute(sql_query, values)

    def save_data(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.mydb.commit()

    def is_user_registered(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        cnt = 0
        for user in self.cursor:
            cnt = cnt + 1
            print(user)
        if cnt == 1:
            return True
        else:
            return False

    def check_for_password_macth(self, sql_query, values, password):
        self.cursor.execute(sql_query, values)
        for user in self.cursor:
            if user[1] == password:
                return True
            else:
                return False

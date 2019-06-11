import mysql.connector
from FraudBillBoardsDetectionApp.constants import application_constants


class NotificationsDAO(object):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=application_constants['host'],
            user=application_constants['user'],
            passwd=application_constants['passwd'],
            database=application_constants['database']
        )

        self.cursor = self.mydb.cursor()
        
    def get_new_notification_id(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        max_notification_id = self.cursor.fetchone()
        if max_notification_id[0] is None:
            new_notification_id = 1
        else:
            new_notification_id = int(max_notification_id[0]) + 1

        return new_notification_id

    def get_notifications(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        return self.cursor.fetchall()

    def save_notification(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.mydb.commit()



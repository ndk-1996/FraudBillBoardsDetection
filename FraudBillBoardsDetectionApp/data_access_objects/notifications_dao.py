import mysql.connector


class NotificationsDAO(object):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="753752xl"
        )

        self.cursor = self.mydb.cursor()

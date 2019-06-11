import mysql.connector
from FraudBillBoardsDetectionApp.constants import application_constants


class ImagesDAO(object):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=application_constants['host'],
            user=application_constants['user'],
            passwd=application_constants['passwd'],
            database=application_constants['database']
        )

        self.cursor = self.mydb.cursor()

    def get_new_image_id(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        max_image_id = self.cursor.fetchone()
        if max_image_id[0] is None:
            new_image_id = 1
        else:
            new_image_id = int(max_image_id[0]) + 1

        return new_image_id

    def save_new_image(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.mydb.commit()



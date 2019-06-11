import mysql.connector
from FraudBillBoardsDetectionApp.constants import application_constants


class BillBoardDAO(object):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=application_constants['host'],
            user=application_constants['user'],
            passwd=application_constants['passwd'],
            database=application_constants['database']
        )

        self.cursor = self.mydb.cursor()

    def get_billboards(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        return self.cursor.fetchall()

    def add_billboard(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.mydb.commit()

    def get_new_billboard_id(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        max_billboard_id = self.cursor.fetchone()
        if max_billboard_id[0] is None:
            new_billboard_id = 1
        else:
            new_billboard_id = int(max_billboard_id[0]) + 1

        return new_billboard_id


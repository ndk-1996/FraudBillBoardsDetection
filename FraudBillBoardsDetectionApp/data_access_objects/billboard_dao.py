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


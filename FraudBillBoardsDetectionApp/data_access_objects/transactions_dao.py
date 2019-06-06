import mysql.connector
from FraudBillBoardsDetectionApp.constants import application_constants


class TransactionsDAO(object):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host=application_constants['host'],
            user=application_constants['user'],
            passwd=application_constants['passwd'],
            database=application_constants['database']
        )

        self.cursor = self.mydb.cursor()

    def get_transactions(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        return self.cursor.fetchall()

    def get_new_transaction_id(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        max_transaction_id = self.cursor.fetchone()
        new_transaction_id = int(max_transaction_id[0])
        if new_transaction_id is None:
            new_transaction_id = 1
        else:
            new_transaction_id = new_transaction_id + 1

        return new_transaction_id

    def update_payment_status(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.mydb.commit()

    def find_transactions_of_current_year(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        return self.cursor.fetchall()

    def insert_new_transaction(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.mydb.commit()

    def find_transacton_dates(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        return self.cursor.fetchone()

    def get_payment_in_progress_transactions(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        return self.cursor.fetchall()



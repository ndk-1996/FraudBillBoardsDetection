from flask import Flask


fraudBillBoardsDetectionApp = Flask(__name__)


if __name__ == __main__:
    fraudBillBoardsDetectionApp.run(debug=1)


from FraudBillBoardsDetectionApp import routes
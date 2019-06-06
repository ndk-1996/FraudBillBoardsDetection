from FraudBillBoardsDetectionApp.constants import application_constants

class FindAvailableDates(object):

    def __init__(self):
        self.days_in_each_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.calender = dict()
        self.calender_view = [[[]]]
        for i in range(len(self.days_in_each_month)):
            self.calender[i + 1] = list()
            for j in range(self.days_in_each_month[i]):
                day = (j + 1, 0)
                self.calender[i + 1].append(day)

    def add_blocked_days_to_calender(self, blocked_days, separator):
        for period in blocked_days:
            start_date = period[0]
            end_date = period[1]
            start_date_month = self.get_month_from_date(start_date, separator)
            end_date_month = self.get_month_from_date(end_date, separator)
            start_date_day = self.get_day_from_date(start_date, separator)
            end_date_day = self.get_day_from_date(end_date, separator)

            if start_date_month == end_date_month:
                for days in range(start_date_day - 1, end_date_day):
                    self.calender[start_date_month][days][1] = 1

                return self.calender

            if start_date_month < end_date_month:
                for days in range(start_date_day - 1, self.days_in_each_month[start_date_month - 1]):
                    self.calender[start_date_month][days][1] = 1

                for days in range(0, end_date_day):
                    self.calender[end_date_month][days][1] = 1

                start_date_month = start_date_month + 1
                end_date_month = end_date_month - 1

                if start_date_month <= end_date_month:
                    for months in range(start_date_month - 1, end_date_month):
                        for days in range(self.days_in_each_month[months]):
                            self.calender[months + 1][days][1] = 1

                return self.calender

    def create_calender_view(self):
        first_day = application_constants['first_day_of_the_current_year']
        for curr_month in range(12):
            days_per_week = list()
            j = 0
            for i in range(first_day - 1):
                days_per_week.append((-1, 0))
            for i in range(first_day, 8):
                days_per_week.append(self.calender[curr_month + 1][j])
                j = j + 1
                first_day = first_day + 1
            if first_day == 8:
                self.calender_view[curr_month].append(days_per_week)
                first_day = 1
                days_per_week = list()

            while j < self.days_in_each_month[curr_month]:
                if first_day == 8:
                    self.calender_view[curr_month].append(days_per_week)
                    first_day = 1
                    days_per_week = list()

                days_per_week.append(self.calender[curr_month + 1][j])
                first_day = first_day + 1
                j = j + 1

            for i in range(first_day + 1, 8):
                days_per_week.append((-1, 0))

            self.calender_view[curr_month].append(days_per_week)
            first_day = first_day + 1

        return self.calender_view

    def get_month_from_date(self, date, separator):
        s = date.split(separator)
        month = s[1]
        if month[0] == '0':
            month = int(month[1])
        else:
            month = int(month)

        return month

    def get_day_from_date(self, date, separator):
        s = date.split(separator)
        day = s[2]
        if day[0] == '0':
            day = int(day[1])
        else:
            day = int(day)

        return day

    def find_no_of_days(self, start_date, end_date, separator):
        start_date_month = self.get_month_from_date(start_date, separator)
        end_date_month = self.get_month_from_date(end_date, separator)
        start_date_day = self.get_day_from_date(start_date, separator)
        end_date_day = self.get_day_from_date(end_date, separator)

        if start_date_month == end_date_month:
            no_of_days = end_date_day - start_date_day + 1
            return no_of_days

        if start_date_month < end_date_month:
            no_of_days = self.days_in_each_month[start_date_month - 1] - start_date_day
            no_of_days = no_of_days + end_date_day

            start_date_month = start_date_month + 1
            end_date_month = end_date_month - 1

            if start_date_month <= end_date_month:
                for months in range(start_date_month - 1, end_date_month):
                    no_of_days = no_of_days + self.days_in_each_month[months]

            return no_of_days


if __name__ == '__main__':
    datesObj = FindAvailableDates()


print(datesObj.days_in_each_month)
print(datesObj.calender)


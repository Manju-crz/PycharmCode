from datetime import *

def compare_two_dates(date1, date2):
    y1, m1, d1 = [int(x) for x in str(date(2020, 2, 29)).split('-')]
    y2, m2, d2 = [int(x) for x in str(date.today()).split('-')]
    b1 = date(y1, m1, d1)
    b2 = date(y2, m2, d2)

    month = b1.strftime("%B")
    year = b1.strftime("%Y")
    dt = b1.strftime("%d")
    print("date month and year is: %s , %s and %s " % (dt, month, year))

    if b1 == b2:
        print("Both dates are equal")

    elif b1 > b2:
        print("b1 is greater than b2")

    else:
        print("b2 is greater than b1")


def add_days_to_today(number_of_days):
    b1 = date.today()
    b1 = b1 + timedelta(days=number_of_days)
    return str(b1).split(" ")[0]  # It will return in the form of yyyy/mm/dd


def get_date_monthname_year_values_from_date(my_date=date.today()):
    # It accepts input in the form of yyyy/mm/dd
    print("my_date is ", my_date)
    y1, m1, d1 = [int(x) for x in str(my_date).split('-')]
    b1 = date(y1, m1, d1)
    return b1.strftime("%d"), b1.strftime("%B"), b1.strftime("%Y")


def get_date_of_today():
    return date.today()


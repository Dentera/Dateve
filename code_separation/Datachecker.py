leap_year = False
condition = {31: '1 3 5 7 8 10 12', 30: '4 6 9 11', 28: '2'}


def data_check(year, month, day):
    global leap_year

    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        leap_year = True

    if 0 < month <= 12:
        if str(month) in condition[31] and 0 < day <= 31 and month != 2:
            return True
        elif str(month) in condition[30] and 0 < day <= 30:
            return True
        elif str(month) in condition[28] and (0 < day <= 28 or leap_year is True and 0 < day <= 29):
            return True
        else:
            return False
    else:
        return False

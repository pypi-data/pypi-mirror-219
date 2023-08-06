# coding=utf-8
import gc


def noodows_time(choose):
    def get_month_days(year, month):
        if month > 12 or month <= 0:
            return -1
        if month == 2:
            return 29 if year % 4 == 0 and year % 100 != 0 or year % 400 == 0 else 28
        if month in (4, 6, 9, 11):
            return 30
        else:
            return 31

    if choose == 1:
        import calendar as cal
        import time as t
        print(t.strftime("%Y-%m-%d %H:%M:%S", t.localtime(t.time())))
        year = int(t.strftime("%Y"))
        month = int(t.strftime('%m'))
        print('This month has ' + str(get_month_days(year, month)) + ' days!')
        ca = cal.month(year, month)
        print(str(year) + 'year' + str(month) + "mouth's calendar:")
        print(ca)
        day = int(t.strftime('%d'))
        t = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)[month - 1]
        t += day
        leap = 0
        if year % 4 == 0 or year % 400 == 0: leap = 1
        if leap == 1 and month > 2: t += 1
        if t % 10 == 1:
            print('the %d st day' % t)
        elif t % 10 == 2:
            print('the %d nd day' % t)
        elif t % 10 == 3:
            print('the %d rd day' % t)
        else:
            print('the %d th day' % t)
        print()
        del get_month_days, year, month, ca, day, t, leap
        gc.collect()
    elif choose == 2:
        while 1:
            try:
                year = int(float(input('year:')))
                month = int(float(input('month:')))
                day = int(float(input('day:')))
                if 1 <= month <= 12 and 1 <= day <= 31:
                    t = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)[month - 1]
                break
            except ValueError:
                print("error: input an undefined thing")
        print('This month has ' + str(get_month_days(year, month)) + ' days!')
        t += day
        leap = 0
        if year % 4 == 0 or year % 400 == 0: leap = 1
        if leap == 1 and month > 2: t += 1
        if t % 10 == 1:
            print('the %d st day' % t)
        elif t % 10 == 2:
            print('the %d nd day' % t)
        elif t % 10 == 3:
            print('the %d rd day' % t)
        else:
            print('the %d th day' % t)
        print()
        del get_month_days, year, month, day, t, leap
        gc.collect()
    else:
        print('error')

while 1:
    try:
        year = int(float(input('year:')))
        month = int(float(input('month:')))
        day = int(float(input('day:')))
        if 1 <= month <= 12 and 1 <= day <= 31:
            se = (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334)[month - 1]
        break
    except ValueError:
        print("error: input an undefined thing")

# coding=utf-8
import gc


def calc():
    """

    :return:
    """

    def sqrt(number):
        num0 = number / 2
        num1 = number / 2 + number / (num0 * 2)
        while abs(num1 - num0) > 1e-5:
            num0 = num1
            num1 = num0 / 2 + number / num0 * 2
        del num0, num1
        gc.collect()
        return number

    while 1:
        print('1:x+y, 2:x-y, 3:x*y, 4:x^y, 5:x/y, 6:_/x')
        print('7:2,3,5, 8:x=2*2*3*5, 9:xπ:')
        print('99:exit')
        m = input()
        if m == '1':
            while 1:
                try:
                    num1 = float(input('num1:'))
                    num2 = float(input('num2:'))
                    break
                except ValueError:
                    print('error:input a str')
            print(num1 + num2)
        elif m == '2':
            while 1:
                try:
                    num1 = float(input('num1:'))
                    num2 = float(input('num2:'))
                    break
                except ValueError:
                    print('error:input a str')
            print(num1 - num2)
        elif m == '3':
            while 1:
                try:
                    num1 = float(input('num1:'))
                    num2 = float(input('num2:'))
                    break
                except ValueError:
                    print('error:input a str')
            print(num1 * num2)
        elif m == '4':
            while 1:
                try:
                    num1 = float(input('num1:'))
                    num2 = float(input('num2:'))
                    break
                except ValueError:
                    print('error:input a str')
            print(num1 ** num2)
        elif m == '5':
            while 1:
                try:
                    print('num1/num2')
                    num1 = float(input('num1:'))
                    num2 = float(input('num2(!=0):'))
                    if num2 == 0:
                        print('error:ZeroDivisionError')
                        continue
                    break
                except ValueError:
                    print('error:input a str')
            while 1:
                input_model = input('1:/,2://,3:%')
                if input_model != '1' and input_model != '2' and input_model != '3':
                    print("error: input an undefined thing")
                    continue
                break
            if input_model == '1':
                print(num1 / num2)
            elif input_model == '2':
                print(num1 // num2)
            elif input_model == '3':
                print(num1 % num2)
            del input_model
            gc.collect()
        if m == '1' or m == '2' or m == '3' or m == '4' or m == '5':
            del num1, num2
        elif m == '6':
            while 1:
                try:
                    num = float(input('num:'))
                    if num < 0:
                        print('error:input a num<0')
                    else:
                        break
                except ValueError:
                    print('error:input a str')
            if num == 0:
                print(0)
            else:
                print(sqrt(num))
            del num
        elif m == '7':
            p = 0
            while 1:
                try:
                    print('a<=b')
                    numa = int(float(input('numa:')))
                    numb = int(float(input('numb:')))
                    if numa > numb:
                        print('error:numa>numb')
                    else:
                        break
                except ValueError:
                    print('error:input a str')
            for m in range(numa, numb + 1):
                if m >= 2:
                    for i in range(2, m):
                        if m % i == 0:
                            break
                    else:
                        p += 1
                        print(m)
            print(p)
            del p, numa, numb, m, i
        elif m == '8':
            while 1:
                try:
                    num = int(input('num(>=0,int):'))
                    if num < 0:
                        print('error:input a negative number')
                except ValueError:
                    print('error:input a str')
                else:
                    break
            print('{}='.format(num), end="")
            if num == 0 or num == 1:
                print('{}'.format(num))
            while num != 0 and num != 1:
                for index in range(2, num + 1):
                    if num % index == 0:
                        num //= index
                        if num == 1:
                            print(index)
                        else:  # index 一定是素数
                            print('{} *'.format(index), end=" ")
                        break
            del num, index
        elif m == '9':
            while 1:
                try:
                    num = float(input('num:'))
                    break
                except ValueError:
                    print('error:input a str')
            lists = [2 * 10 ** 24, 2 * 10 ** 24 // 3, 2]
            lists[0] += lists[1]
            while lists[1] > 0:
                lists[1] = lists[1] * lists[2] // (lists[2] * 2 + 1)
                lists[2] += 1
                lists[0] += lists[1]
            lists[0] = lists[0] // (10 ** 15) / (10 ** 9)
            print(num * float('%.20f' % lists[0]))
            del num, lists
        elif m == '99 ':
            break
        else:
            print('error')
        gc.collect()

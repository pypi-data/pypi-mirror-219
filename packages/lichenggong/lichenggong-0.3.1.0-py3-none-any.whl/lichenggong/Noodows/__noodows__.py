# coding=utf-8

import gc
import sys

# 系统包

sys.path.append('../Program_Files/System')

import __bios__
import __calc__
import __logo__
import __user__
import __thanks__
import __n_time__


# 自建包

# import some modules

# 优雅

def __n_start__():
    def __first_choose__():
        with open('first.txt', 'r') as First:
            first = First.readline()
        if first == 'True':
            __user__.__u_first__(0)
            first = 'False'
            with open('first.txt', "w", encoding="utf-8") as First:
                First.write(first)
            del first
            gc.collect()

    def __language__(model, us_en, zn_cn, zn_tw):
        if users_language == 'US_en':
            if model == 'print':
                print(us_en)
            elif model == 'input':
                print(us_en, end='')
                variable = input("")
                return variable
            elif model == '()':
                print(us_en)
                print()
            else:
                print('error: input an undefined thing')

        elif users_language == 'ZN_cn':
            if model == 'print':
                print(zn_cn)
            elif model == 'input':
                print(zn_cn, end='')
                variable = input("")
                return variable
            elif model == '()':
                print(zn_cn)
                print()
            else:
                print('error: input an undefined thing')

        elif users_language == 'Zn_tw':
            if model == 'print':
                print(zn_tw)
            elif model == 'input':
                print(zn_tw, end='')
                variable = input("")
                return variable
            elif model == '()':
                print(zn_tw)
                print()
            else:
                print('error: input an undefined thing')
        else:
            print('error: your language is wrong ')

    __first_choose__()
    __bios__.bios()
    print('hallo,world =) ')
    print()
    __logo__.logo3_0()
    __user__.user()
    with open('.//now//language.txt', 'r') as language:
        users_language = language.readline()
    with open('.//now//power.txt', 'r') as power:
        users_power = power.readline()
    del language, power
    gc.collect()
    while 1:
        __language__('()', '0: Start', '0: 开始菜单', '0: 開始菜單')
        __language__('()', '1: Explorer', '1: 此电脑', '1: 我的電腦')
        __language__('()', '2: Log out', '2: 退出账号', '2: 退出賬號')
        if users_power == 'admin':
            __language__('()', '3: thanks', '3: 致谢名单', '3: 致謝名單')
        __language__('()', '99: Exit', '99：关机', '99：關機')
        choose = __language__('input', 'want?', '你干嘛', '你幹嘛')
        if choose == '0':
            while 1:  # Start menu 需要 while 1!
                __language__('()', '-start-', '-开始菜单-', '-開始菜單-')
                __language__('()', '0: back', '0: 退出', '0: 退出')
                __language__('()', '1: sys software', '1: 汐筒软件', '1: 系統軟件')
                choose = __language__('input', 'want?', '你干嘛', '你幹嘛')
                if choose == '0':
                    print("Good bye!")
                    break
                elif choose == '1':
                    while 1:
                        choose = __language__('input', '1:back,2:continue', '1:返回,2:继续', '1:返回,2:繼續')
                        if choose == '1':
                            print("Good bye!")
                            break
                        elif choose == '2':
                            while 1:
                                __language__('()', '-sys software-', '-汐筒软件-', '-系統軟件-')
                                __language__('()', '0: back', '0: 退出', '0: 退出')
                                __language__('()', '1: calc', '1: 计算器', '1: 計算器')
                                __language__('()', '2: Time', '2: 时间', '2: 時間')
                                if users_power == 'admin':
                                    __language__('()', '3: user change', '3: 用户更改', '3: 用戶更改')
                                choose = __language__('input', 'want?', '你干嘛', '你幹嘛')
                                if choose == '0':
                                    print("Good bye!")
                                    break
                                elif choose == '1':
                                    __calc__.calc()
                                elif choose == '2':
                                    choose = __language__('input', '1:back,2:continue', '1:返回,2:继续',
                                                          '1:返回,2:繼續')
                                    if choose == '1':
                                        print("Good bye!")
                                    elif choose == '2':
                                        __noodows_time__.time(1)
                                    else:
                                        print('error: input an undefined thing')
                                elif choose == '3':
                                    if users_power != 'admin':
                                        print('error: input an undefined thing')
                                    choose = __language__('input', '1:back,2:continue', '1:返回,2:继续',
                                                          '1:返回,2:繼續')
                                    if choose == '1':
                                        print("Good bye!")
                                    elif choose == '2':
                                        with open('.//now//password.txt', 'r') as password:
                                            users_password = password.readline()  # read the Password
                                        while 1:
                                            input_password = __language__('input',
                                                                          'admin,please input your password:',
                                                                          '管理员,请输入密码:',
                                                                          '管理员,請輸入密碼:')
                                            if input_password != users_password:
                                                __language__('print',
                                                             'the password you input is wrong',
                                                             '密码错误',
                                                             '密碼錯誤')
                                            __user__.change()
                                            del users_password, input_password
                                            gc.collect()
                                    else:
                                        print('error')

                        else:
                            print('error: input an undefined thing')
                else:
                    print('error: input an undefined thing')
        elif choose == '1':  # Explorer 需要 while 1!# 施工
            while 1:
                f = input('1:返回,2:繼續')
                if f == '1':
                    print("Good bye!")
                    break
                elif f == '2':
                    print('正在制作')
                else:
                    print('error: input an undefined thing')
        elif choose == '2':
            choose = __language__('input', '1:back,2:continue', '1:返回,2:继续', '1:返回,2:繼續')
            if choose == '1':
                print("Good bye!")
            elif choose == '2':
                __user__.user()
        elif choose == '3':
            if users_power != 'admin':
                print('error: input an undefined thing')
            choose = __language__('input', '1:back,2:continue', '1:返回,2:继续', '1:返回,2:繼續')
            if choose == '1':
                print("Good bye!")
            elif choose == '2':
                __thanks__.thanks()
        elif choose == '99':
            exit(0)
        else:
            print('error: input an undefined thing')
__n_start__()
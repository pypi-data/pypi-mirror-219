# coding=utf-8

# 祖宗之法不可变 切记

import gc
import os
import shutil


def first(__first):
    with open('../Noodows//version//version.txt', 'r') as Version_version:
        version = Version_version.readline()  # read the version
    with open('../Noodows//version//build_version.txt', 'r') as Build_version:
        build_version = Build_version.readline()  # read the version
    print()
    print('您正在使用巨硬产品 noodows yee{0}(测试{1}) 无图像版 (用户创建区)'.format(version, build_version))
    print("You're use noodows yee{0}(build{1}) no Image by Big-hard (setup user)".format(version, build_version))
    print()
    print('设置语言')
    print('Setup language')
    print()
    while 1:
        input_language = input('language(first):      1.English 2.简体中文 3.繁體中文')
        if input_language != '1' and input_language != '2' and input_language != '3':
            print()
            print("error: input an undefined thing")
            continue
        print()
        check_language = input('language(again):      1.English 2.简体中文 3.繁體中文')
        if check_language != '1' and check_language != '2' and check_language != '3':
            print()
            print("error: input an undefined thing")
            print()
            continue
        if check_language == input_language:
            right_language = input_language
            if right_language == '1':
                right_language = 'US_en'
            elif right_language == '2':
                right_language = 'ZN_cn'
            elif right_language == '3':
                right_language = 'ZN_tw'
            break
        print()
        print('您两次输入的语言不一样！')
        print('the first language is not the second one!')
        print()

    # setup language
    def first_language_packager(the_language, model, language_choose):
        # how to use the language

        language_package = [
            'setup a user',
            '创造用户',
            '创造用户',
            'name(first):',
            '名(第一次):',
            '名(初次):',
            'name(again):',
            '名(第二次):',
            '名(再次):',
            'do you want to have  a password?         1.yes 2.no',
            '是否需要密码？         1.是的 2.不需要',
            '是否需要密码？         1.是 2.否',
            'password(first):',
            '密码(第一次):',
            '密码(初次):',
            'password(again):',
            '密码(第二次):',
            '密码(再次):',
            "what's the user's power?         1.admin 2.user 3.visitor",
            '此用户的权限是？         1.管理员 2.用户 3.游客',
            '此用户的权限？         1.管理 2.用户 3.旅者',
            "that's your user,right?         1.yes 2.no",
            '这是否是你的用户？         1.是的 2.不是',
            '此是否是此用户？         1.是 2.否'
        ]
        if the_language == right_language:
            if model == 'print':
                print(language_package[language_choose])
            elif model == 'input':
                print(language_package[language_choose], end='')
            else:
                print('error: input an undefined thing')

    print()
    first_language_packager('US_en', 'print', 0)
    first_language_packager('ZN_cn', 'print', 1)
    first_language_packager('ZN_tw', 'print', 2)
    while 1:
        while 1:
            print()
            input_id = input('ID(1st):')
            print()
            check_id = input('ID(2nd):')
            if check_id == input_id:
                right_id = input_id
                print()
                break
            print()
            print('错误: 您两次输入的ID不一样！')
            print('error: the first ID you input is not the second one!')
        # setup user ID
        while 1:
            first_language_packager('US_en', 'input', 3)
            first_language_packager('ZN_cn', 'input', 4)
            first_language_packager('ZN_tw', 'input', 5)
            input_name = input()
            print()
            first_language_packager('US_en', 'input', 6)
            first_language_packager('ZN_cn', 'input', 7)
            first_language_packager('ZN_tw', 'input', 8)
            check_name = input()
            if check_name == input_name:
                print()
                right_name = input_name
                break
            print()
            print('错误: 您两次输入的名字不一样！')
            print('error: the first name you input is not the second one!')
            print()
        # setup username
        while 1:
            first_language_packager('US_en', 'input', 9)
            first_language_packager('ZN_cn', 'input', 10)
            first_language_packager('ZN_tw', 'input', 11)
            check_password = input()
            if check_password == '1':
                print()
                first_language_packager('US_en', 'input', 12)
                first_language_packager('ZN_cn', 'input', 13)
                first_language_packager('Zn_tw', 'input', 14)
                input_password = input()
                if input_password == 'nothing':
                    print("are you serious?")
                    print("error: input a nul thing")
                    continue
                print()
                first_language_packager('US_en', 'input', 15)
                first_language_packager('ZN_cn', 'input', 16)
                first_language_packager('ZN_tw', 'input', 17)
                check_password = input()
                if check_password == input_password:
                    print()
                    right_password = input_password
                    break
                print()
                print('错误: 您两次输入的密码不一样！')
                print('error: the first password you input is not the second one!')
                print()
            elif check_password == '2':
                print()
                right_password = "nothing"
                break
            else:
                print("error: input an undefined thing")
        # setup user password
        while 1:
            if __first == 0:
                right_power = 'admin'
            else:
                first_language_packager('US_en', 'input', 18)
                first_language_packager('ZN_cn', 'input', 19)
                first_language_packager('ZN_tw', 'input', 20)
                power = input()
                if power == '1':
                    right_power = 'admin'
                elif power == '2':
                    right_power = 'user'
                elif power == '3':
                    right_power = 'visitor'
                else:
                    print()
                    print("error: input an undefined thing")
                    print()
                    continue
            break
        # set up the field of power
        print()
        print('ID:{0}'.format(right_id))
        print('name:{0}'.format(right_name))
        print('password:{0}'.format(right_password))
        print('power:{0}'.format(power))
        print()
        first_language_packager('US_en', 'input', 21)
        first_language_packager('ZN_cn', 'input', 22)
        first_language_packager('ZN_tw', 'input', 23)
        choice = input()
        if choice == "1":
            print()
            print('马上就好')
            print("It'll only take a second")
            print()
            print('0%', end=" ")
            folder = '../User//User' + right_id + '//'
            folder_user_used = folder + 'User_used'
            users_language = folder + 'language.txt'
            users_name = folder + 'name.txt'
            users_password = folder + 'password.txt'
            users_power = folder + 'power.txt'
            print()
            print('10%', end=" ")
            if __first == 0:
                os.makedirs(folder)
                os.makedirs(folder_user_used)
                if __first == 0:
                    os.makedirs('./now')
                    os.makedirs('../User')
                    os.makedirs('../User//UserPE')
                    os.makedirs('../User//UserPE//User_used')
            print()
            print('20%', end=" ")
            with open(users_language, 'w', encoding="utf-8") as Language:
                Language.write(right_language)
            with open('../User//UserPE//language.txt', 'w', encoding="utf-8") as Language:
                Language.write('US_en')
            print()
            print('30%')
            print()
            print('40%', end=" ")
            with open(users_name, 'w', encoding="utf-8") as Name:
                Name.write(right_name)
            with open('../User//UserPE//name.txt', 'w', encoding="utf-8") as Name:
                Name.write('PE')
            print()
            print('50%', end=" ")
            with open(users_password, 'w', encoding="utf-8") as Password:
                Password.write(right_password)
            with open(users_password, 'w', encoding="utf-8") as Password:
                Password.write('nothing')
            print()
            print('60%', end=" ")
            with open(users_power, 'w', encoding="utf-8") as Power:
                Power.write(right_power)
            with open(users_power, 'w', encoding="utf-8") as Power:
                Power.write(right_power)
            print()
            print('100%')
            break
        elif choice == '2':
            print("OK!let's back")
    print()
    print('欢迎使用')
    print('Thank you for your support!')
    del Version_version, version, Build_version, build_version, input_language, check_language, first_language_packager
    del input_id, check_id, input_name, check_name, check_password
    del right_language, right_id, right_name, right_password, power
    del choice, users_language, users_name, users_password, users_power, Language, Name, Password, Power
    gc.collect()


def change():
    """

    """
    with open('../Noodows//version//version.txt', 'r') as Version_version:
        version = Version_version.readline()  # read the version
    with open('../Noodows//version//build_version.txt', 'r') as Build_version:
        build_version = Build_version.readline()  # read the version
    print('您正在使用巨硬产品 noodows yee{0}(测试{1}) 无图像版 (用户更改区)'.format(version, build_version))
    print("You're use noodows yee{0}(build{1}) no Image by Big-hard (setup user)".format(version, build_version))
    print('操作风险,数据至上')
    print("It's dangerous")
    ID = input("change who?         input the ID")
    folder = '../User//User' + ID
    users_language = folder + '//language.txt'
    users_name = folder + '//name.txt'
    users_password = folder + '//password.txt'
    users_power = folder + '//power.txt'
    change_thing = input('change what?         1.ID 2.language 3.name 4.password 5.power')
    if change_thing == '1':
        right_id = input("ID:")
        right_id = '../User//User' + right_id
        os.rename(folder, right_id)
    elif change_thing == '2':
        right_language = input("language :")
        with open(users_language, 'w', encoding="utf-8") as language:
            language.write(right_language)
    elif change_thing == '3':
        right_name = input("name:")
        with open(users_name, 'w', encoding="utf-8") as name:
            name.write(right_name)
    elif change_thing == '4':
        right_password = input("password:")
        with open(users_password, 'w', encoding="utf-8") as password:
            password.write(right_password)
    elif change_thing == '5':
        right_power = input("power:")
        with open(users_power, 'w', encoding="utf-8") as power:
            power.write(right_power)
    else:
        print("error: input an undefined thing")
    del change_thing, ID, right_id, users_language, language, right_language, users_name, name, right_name
    del users_password, password, right_password, users_power, power, right_power
    gc.collect()


def user():
    """

    """
    user_list = []
    for root, dirs, file in os.walk('..//User//'):
        try:
            with open(root + '//name.txt', 'r', encoding="utf-8") as name:
                user_list.append(['ID:' + root.lstrip('..//User//User'), 'name:' + name.readline()])
        except FileNotFoundError:
            pass
    print('users:')
    print()
    while 1:
        try:
            i = 0
            while 1:
                print(user_list[i])
                print()
                i += 1
        except IndexError:
            i = 0
        while 1:
            try:
                input_id = input("your user's ID:")
                if user_list[i][0] != 'ID:' + str(input_id):
                    i += 1
                else:
                    right_id = input_id
                    break
            except IndexError:
                print('error: input an undefined thing')
            except TypeError:
                print('error: input a wrong thing')
        choose = input('1:back,2:continue')
        print()
        if choose == '1':
            print("Good bye!")
            print()
            continue
        elif choose == '2':

            folder = '..//User//User' + right_id + '//'
            folder_user_used = folder + 'User_used'  # 施工
            user_language = folder + 'language.txt'
            user_name = folder + 'name.txt'
            user_password = folder + 'password.txt'
            user_power = folder + 'power.txt'

            with open(user_language, 'r') as language:
                users_language = language.readline()  # read the language
            with open(user_name, 'r') as name:
                users_name = name.readline()  # read the name
            with open(user_password, 'r') as password:
                users_password = password.readline()  # read the password
            with open(user_power, 'r') as power:
                users_power = power.readline()  # read the power

            if users_password != 'nothing':
                input_password = input("your user's password:")
                while input_password != users_password:
                    print()
                    print("error: your inputted password isn't the right password")
                    print()
                    input_password = input("your user's password:")
                print()
                del input_password
            print(users_name + ',hello')
            print()
            shutil.rmtree('.//now//User_used')
            shutil.copytree(folder_user_used, './/now//User_used')
            with open('.//now//language.txt', 'w', encoding="utf-8") as Language:
                Language.write(users_language)
            with open('.//now//name.txt', 'w', encoding="utf-8") as Name:
                Name.write(users_name)
            with open('.//now//password.txt', 'w', encoding="utf-8") as Password:
                Password.write(users_password)
            with open('.//now//power.txt', 'w', encoding="utf-8") as Power:
                Power.write(users_power)
                break
    del user_list, root, dirs, file, name
    del i, input_id, right_id, choose, folder
    del user_language, user_name, user_password, user_power, language, password, power
    del users_language, users_name, users_password, users_power
    del Language, Name, Password, Power
    gc.collect()

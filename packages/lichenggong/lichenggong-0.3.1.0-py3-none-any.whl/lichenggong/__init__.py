def start():
    import platform, sys,os
    if platform.system() == "Windows":
        print('Windows :(')
    elif platform.system() == "Linux":
        print('!!!!Linux!!!!!')
    elif platform.system() == "Cygwin":
        print('!!!Cygwin!!!')
    elif platform.system() == "Darwin":
        print('!!!!!Mac!!!!!!')
    elif platform.system() == "Java":
        print('Java????!!!')
    else:
        print("?!")
    with open(sys.path[-2] + '//Lib//site-packages//lichenggong//Noodows//python.txt', "w", encoding="utf-8") as python:
        python.write(sys.path[-2])
    print('change dir to {0}{1}'.format(sys.path[-2],'//Lib//site-packages//lichenggong//Noodows'))
    os.chdir(sys.path[-2] + '//Lib//site-packages//lichenggong//Noodows')
    print(os.getcwd())
    sys.path.append('./')
    import __noodows__
    __noodows__.__n_start__()
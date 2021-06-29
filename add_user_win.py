import os
import subprocess
import time
import stdiomask
print('Данное программное обеспечение разработано Кириченко А.В. для компании КМФ')
print('В целях автоматизации инсталляции ПО на планшеты')
os.system('chcp 65001') # Корректно отображение текста
os.system('tzutil /s "Central Asia Standard Time"') # часовой пояс +6 Астана
os.system('netsh advfirewall set allprofiles state off') # Отключить брэндмаур windows
os.system('powercfg /SETACVALUEINDEX SCHEME_CURRENT '
          '7516b95f-f776-4464-8c53-06167f40cc99 3c0bc021-c8a8-4e07-a973-6b14cbcb2b7e 180')
os.system('powercfg /SETDCVALUEINDEX SCHEME_CURRENT '
          '7516b95f-f776-4464-8c53-06167f40cc99 3c0bc021-c8a8-4e07-a973-6b14cbcb2b7e 180')
os.system('powercfg -change -standby-timeout-dc 3')
os.system('powercfg -change -standby-timeout-ac 3')
def user_pass(): # Изменение пароля
    restart = input('Смена пароля Y-да, N-нет: ')
    while restart != 'Y' and restart != 'y' and restart != 'N' and restart != 'n':
        restart = input('Нужно выбрать только Y-да, N-нет: ')
    else:
        if restart == 'Y' or restart == 'y':
            user = input('Имя пользователя: ')
            c = 0
            while c == 0:
                password = stdiomask.getpass('Пароль: ',)
                password2 = stdiomask.getpass('Повторите Пароль: ')
                if password == password2:
                    c = 1
                else:
                    print('Пароли не совпадают повторите.')
            os.system('net user "{}" "{}"'.format(user, password))
            return 'Пароль изменен: {}'.format(user)

def add_user(): # Добовление пользователя
    restart = input('Хотите добавить пользователя Y-да, N-нет: ')
    while restart != 'Y' and restart != 'y' and restart != 'N' and restart != 'n':
        restart = input('Нужно выбрать только Y-да, N-нет: ')
    else:
        if restart == 'Y' or restart == 'y':
            user = input('Имя пользователя: ')
            c = 0
            while c == 0:
                password = stdiomask.getpass('Пароль: ',)
                password2 = stdiomask.getpass('Повторите Пароль: ')
                if password == password2:
                    c = 1
                else:
                    print('Пароли не совпадают повторите.')
            os.system('net user "{}" "{}" /add'.format(user, password))
            return 'Создан пользователь: {}'.format(user)


def name_pc(): # Коретировка имени
    restart = input('Хотите изменить имя ПК Y-да, N-нет: ')
    while restart != 'Y' and restart != 'y' and restart != 'N' and restart != 'n':
        restart = input('Нужно выбрать только Y-да, N-нет: ')
    else:
        if restart == 'Y' or restart == 'y':
            name = input('Имя ПК: ')
            subprocess.call(['powershell.exe', "Rename-Computer -NewName {}".format(name)])
            return reboot()

def bit_os(): # Определение разрядности ситстемы
    text = os.popen('systeminfo').read()
    nom = text.find('-based PC')
    if text[nom - 2:nom] == '64':
        os_64()
    elif text[nom - 2:nom] == '86':
        os_32()
    else:
        return 'OS не определил'

def sech(): #Проверка каталога на соответствие
    path = 'C:\plan_install'
    spisok = ['7z920-x64.msi', 'ChromeStandaloneSetup.exe', 'ChromeStandaloneSetup64.exe',
              'appsetup.exe', 'chngpsw.sql', 'FortiClient 6.0.7', 'Keyboard Mouse Test V 0.4(portable)',
              'KZLocale_1.2.1.7', 'LibreOffice_6.0.1_Win_x64.msi', 'LibreOffice_6.0.1_Win_x86.msi', 'LM', 'Asbuka',
              'off-USB.bat', 'on-USB.bat', 'update ERPOR.sql', 'Мобильный эксперт.lnk']

    def sverka(sverka):
        result = list(set(sverka) - set(os.listdir(path)))
        if not result:
            restart = input('Продолжит инсталяцию Y-да, N-нет: ')
            while restart != 'Y' and restart != 'y' and restart != 'N' and restart != 'n':
                restart = input('Нужно выбрать только Y-да, N-нет: ')
            else:
                if restart == 'Y' or restart == 'y':
                    bit_os()
        else:
            print('У вас нет файлов: {}'.format(result))
            restart = input('Хотите продолжить Y-да, N-нет: ')
            while restart != 'Y' and restart != 'y' and restart != 'N' and restart != 'n':
                restart = input('Нужно выбрать только Y-да, N-нет: ')
            else:
                if restart == 'Y' or restart == 'y':
                    bit_os()

    if os.path.exists(path):
        if os.path.isdir(path):
            print('Папка plan_install есть')
            sverka(spisok)
    else:
        print('Папка plan_install не найдена')
        stop()

def os_64():
    os.system('"C:\plan_install\LM\LiteManager Pro - Server.msi" /quiet')
    os.system('regedit.exe /S "C:\plan_install\LM\pass.reg"')
    os.system('"C:\plan_install\KZLocale_1.2.1.7\KZLocale.exe"')
    os.system('"C:\plan_install\ChromeStandaloneSetup64.exe"')
    os.system('"C:\plan_install\FortiClient 6.0.7\FortiClientSetup_6.0.7_x64.exe" /quiet')
    os.system('"C:\plan_install\off-USB.bat"')
    os.system('"C:\plan_install\LibreOffice_6.0.1_Win_x64.msi"')

def os_32():
    os.system('"C:\plan_install\LM\LiteManager Pro - Server.msi" /quiet')
    os.system('regedit.exe /S "C:\plan_install\LM\pass32.reg"')
    os.system('"C:\plan_install\KZLocale_1.2.1.7\KZLocale.exe"')
    os.system('"C:\plan_install\ChromeStandaloneSetup.exe"')
    os.system('"C:\plan_install\FortiClient 6.0.7\FortiClientSetup_6.0.7_x86.exe" /quiet')
    os.system('"C:\plan_install\off-USB.bat"')
    os.system('"C:\plan_install\LibreOffice_6.0.1_Win_x86.msi"')

def stop():
    restart = input('Хотите прервать установку Y-да, N-нет: ')
    while restart != 'Y' and restart != 'y' and restart != 'N' and restart != 'n':
        restart = input('Нужно выбрать только Y-да, N-нет: ')
    else:
        if restart == 'Y' or restart == 'y':
            raise SystemExit
        elso: bit_os()


def reboot():
    restart = input('Хотите перезагрузить Компьютер Y-да, N-нет: ')
    n = 0
    while restart != 'Y' and restart != 'y' and restart != 'N' and restart != 'n':
        restart = input('Нужно выбрать только Y-да, N-нет: ')
    else:
        if restart == 'Y' or restart == 'y':
            os.system('shutdown -r -f -t 0')
        else:
            raise SystemExit


user_pass()
time.sleep(1)
sech()
time.sleep(1)
add_user()
time.sleep(1)
name_pc()



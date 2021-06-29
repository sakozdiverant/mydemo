import paramiko

def slovar_to():
    spisok = open('./TO.csv', 'r')
    res = {}    
    for i in spisok.readlines():
        i = i.split(';')
        res[f'{i[0]} {i[1]}'] = i[2].split()
    return res

def reboot_TO(ip):
    port = 22
    username = 'username'
    password = 'password'
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(ip, port, username, password)
    try:
        comanda = s.invoke_shell()
        comanda.send('sudo reboot\n')
        comanda.send('1\n')
        return 'Перезагрузка прошла успешно'
    except Exception as e:
        error_log = str(e)
        return error_log + '\n'


import os
import hashlib
from getpass import getpass

clear_command = input('your terminals cls command: ')
os.system(clear_command)
print('welcome to insider')
print('type help for help')
print('standard password is `123` but you can change it')
user = "simon"
host = "esp1814"
wp = "/"
column_width = 30
superuser = False

def password():
    h = hashlib.new('sha256')
    h.update(getpass().encode())
    with open("password.txt", "r") as file_pass:
        readpass = file_pass.readline()
    return readpass == h.hexdigest()

while True:
    cmd = input('[' + user + '§' + host + ']:' + wp + '$ ')
    if cmd == 'ls':
        try:
            files = os.listdir(wp)
            print(" ")
            for index, file in enumerate(files):
                print(f"{file:<{column_width}}", end=" | " if (index + 1) % 3 and index + 1 != len(files) else "\n")
            print(" ")
        except:
            print('file is not a directory, or an unexpected error occurred')

    if cmd.startswith('cd '):
        target = cmd.split(" ",1)[1]
        wp = target

    if cmd.startswith('cdu '):
        target = cmd.split(" ",1)[1]
        wp = wp + target

    if cmd == 'pwd':
        print(wp)

    if cmd == 'help':
        print(' ')
        print('Commands available:')
        print('ls                     | lists all files inside working directory')
        print('cd {directory}         | change working directory')
        print('pwd                    | print out current working directory')
        print('dispw {column width}   | edit the column width used for various commands like `ls`')
        print('clear                  | clears the terminal')
        print('su                     | enable super user [PASSWORD PROMPT]')
        print('exsu                   | exit super user')
        print('chsu                   | check wether you are super user or not')
        print('host {new host}        | change the host [SUPER COMMAND]')
        print('user {new user}        | change the username')
        print('pass {new pass}        | change the password [SUPER COMMAND] [PASSWORD PROMPT]')
        print(' ')

    if cmd == 'clear':
        os.system(clear_command)

    if cmd.startswith('dispw'):
        column_width = cmd.split(" ",1)[1]

    if cmd.startswith('su'):
        if password():
            print('super user enabled')
            superuser = True
        else:
            print('incorrect password, check if its correct or if the password is incorrectly hashed')

    if cmd == 'exsu':
        print('super user disabled')
        superuser = False
    
    if cmd == 'chsu':
        print(superuser)

    if cmd == 'pass':
        if superuser:
            if password():
                new_pass = getpass('new pass: ')
                h = hashlib.new('sha256')
                h.update(new_pass.encode())
                new_pass = h.hexdigest()
                with open("password.txt", "w") as file_pass:  # Open file in write mode
                    file_pass.write(new_pass)
            else:
                print('incorrect password, check if its correct or if the password is incorrectly hashed')
        else:
            print('requires superuser')
    
    if cmd.startswith('user '):
        user = cmd.split(" ",1)[1]

    if cmd.startswith('host '):
        if superuser:
            host = cmd.split(" ",1)[1]
        else:
            print('requires superuser')

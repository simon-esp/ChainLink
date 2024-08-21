import os
import hashlib

clear_command = input('your terminals cls command: ')
os.system(clear_command)
user = "simon"
host = "insider"
wp = "/"
column_width = 30
superuser = False

def password():
    h = hashlib.new('sha256')
    h.update(input('Pass:').encode())
    with open("password.txt", "r") as file_pass:
        readpass = file_pass.readline()
    return readpass == h.hexdigest()

while True:
    cmd = input('{' + user + '$' + host + '} ')
    if cmd == 'ls':
        files = os.listdir(wp)
        print(" ")
        for index, file in enumerate(files):
            print(f"{file:<{column_width}}", end=" | " if (index + 1) % 3 and index + 1 != len(files) else "\n")
        print(" ")

    if cmd.startswith('cd '):
        target = cmd.split(" ",1)[1]
        wp = target

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
        accepted = password()
        if accepted:
            print('super user enabled')
            superuser = True

    if cmd == 'exsu':
        print('super user disabled')
        superuser = False
    
    if cmd == 'chsu':
        print(superuser)

    if cmd == 'pass':
        if superuser:
            if password():
                new_pass = input('new pass: ')
                with open("password.txt", "w") as file_pass:  # Open file in write mode
                    file_pass.write(new_pass)

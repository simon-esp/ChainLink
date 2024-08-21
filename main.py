import os

os.system('cls')
user = "simon"
host = "insider"
wp = "/"
column_width = 30
superuser = False

def password():
    prompt = input('Pass:')
    file_pass = open(r"/insider/password.txt", "Access_Mode")
    readpass = file_pass.readline()
    file_pass.close()
    return readpass == prompt

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
        os.system('cls')

    if cmd.startswith('dispw'):
        column_width = cmd.split(" ",1)[1]

    if cmd.startswith('su'):
        if password:
            print('super user enabled')
            superuser = True

    if cmd == 'exsu':
        print('super user disabled')
        superuser = False
    
    if cmd == 'chsu':
        print(superuser)

import os
import hashlib
from getpass import getpass
from termcolor import colored, cprint
import interpreter

#clear_command = input(colored('your terminals cls command: ', 'green'))
clear_command = 'cls' if os.name == 'nt' else 'clear'
os.system(clear_command)
print(colored('welcome to chainlink', 'green'))
print(colored('type help for help', 'green'))
print(colored('standard password is `123` but you can change it', 'green'))
with open("data.txt", "r") as f:
    data = f.read()
    data = data.split("|",1)
    user = data[0]
    host = data[1]
wd = "c:\\"
superuser = False

def password():
    h = hashlib.new('sha256')
    h.update(getpass().encode())
    with open("password.txt", "r") as file_pass:
        readpass = file_pass.readline()
    return readpass == h.hexdigest()

while True:
    cmd_text = colored('[' + user + '§' + host + ']:' + colored(wd, attrs=['underline']) + colored('$ ', 'magenta', attrs=['bold']), 'magenta', attrs=['bold'])
    cmd = input(cmd_text)

    history = True
    if cmd == 'ls':
        try:
            files = os.listdir(wd)
            column_width = len(max(files, key=len)) if files else 0
            print(" ")
            for index, file in enumerate(files):
                print(colored(f"{file:<{column_width}}", 'cyan'), end=colored(" | ", 'yellow') if (index + 1) % 3 != 0 and index + 1 != len(files) else "\n")
            print(" ")
        except:
            print('file is not a directory, or an unexpected error occurred')

    elif cmd.startswith('cd '):
        target = cmd.split(" ",1)[1]
        wd = target

    elif cmd.startswith('cdu '):
        target = cmd.split(" ", 1)[1]
        wd = os.path.join(wd, target)


    elif cmd == 'pwd':
        print(wd)

    elif cmd == 'help':
        print(' ')
        print(colored('Commands available:', 'cyan'))
        print(colored('ls                     | lists all files inside working directory', 'cyan'))
        print(colored('cd {directory}         | change working directory', 'cyan'))
        print(colored('cdu {directory}        | add a path to your already existing working directory', 'cyan'))
        print(colored('cdd                    | go back 1 directory', 'cyan'))
        print(colored('pwd                    | print out current working directory', 'cyan'))
        print(colored('clr                    | clears the terminal', 'cyan'))
        print(colored('su                     | enable super user [PASSWORD PROMPT]', 'cyan'))
        print(colored('exsu                   | exit super user', 'cyan'))
        print(colored('chsu                   | check wether you are super user or not', 'cyan'))
        print(colored('host {new host}        | change the host [SUPER COMMAND]', 'cyan'))
        print(colored('user {new user}        | change the username', 'cyan'))
        print(colored('pass {new pass}        | change the password [SUPER COMMAND] [PASSWORD PROMPT]', 'cyan'))
        print(colored('bcmd                   | gives a prompt to run in the systems terminal', 'cyan'))
        print(colored('cat {file}             | print the contents of a the file, has to be under your working directory', 'cyan'))
        print(colored('cdtos                  | cd to os, changes directory to os folder', 'cyan'))
        print(colored('echo {text}            | echo text to the terminal, useful in assembly i guess', 'cyan'))
        print(colored('copy {file}            | copy a file to the os folder, with a `!` in front', 'cyan'))
        print(' ')

    elif cmd == 'clr':
        os.system(clear_command)

    elif cmd.startswith('su'):
        if password():
            print('super user enabled')
            superuser = True
        else:
            print('incorrect password, check if its correct or if the password is incorrectly hashed')

    elif cmd == 'exsu':
        print('super user disabled')
        superuser = False
    
    elif cmd == 'chsu':
        print(superuser)

    elif cmd == 'pass':
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
    
    elif cmd.startswith('user '):
        user = cmd.split(" ",1)[1]
        with open("data.txt", "w") as f:  # Open file in write mode
            f.write(user + '|' + host)

    elif cmd.startswith('host '):
        if superuser:
            host = cmd.split(" ",1)[1]
            with open("data.txt", "w") as f:  # Open file in write mode
                f.write(user + '|' + host)
        else:
            print('requires superuser')

    elif cmd == 'bcmd':
        os.system(input('your command: '))

    elif cmd.startswith('cat'):
        try:
            with open(os.path.join(wd, cmd.split(" ",1)[1]), 'r') as f: # The with keyword automatically closes the file when you are done
                print (f.read())
        except Exception as e:
            print(f"Error: {e}")
    
    elif cmd.startswith('clss'):
        try:
            interpreter.clss(os.path.join(wd, cmd.split(" ",1)[1]))
        except:
            print("something did a little oopsie")

    elif cmd.startswith('ev'):
        try:
            print(interpreter.eval(cmd.split(" ",1)[1]))
        except:
            print("something did a little oopsie")

    elif cmd.startswith('raw'):
            try:
                interpreter.raw_clss(cmd.split(" ",1)[1])
            except:
                print("something did a little oopsie")

    elif cmd == 'cdd':
        wd = os.path.dirname(os.path.normpath(wd))
        if wd == '':
            wd = '\\'

    elif cmd == 'sl':
        print('🚂')
    
    elif cmd.startswith('copy '):
        split = cmd.split(" ")
        try:
            print(split)
            full_path = os.path.join(wd, split[1])
            print(f"Trying to open file: {full_path}")  # Debugging line
            with open(full_path, 'r') as f:
                    content = f.read()
            print('finding path..')
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, '!' + split[1])
            print('creating file..')
            with open(file_path, 'a') as f:
                f.write(content)
            print(f"File copied to {file_path}")
        except FileNotFoundError as e:
            print(f"{full_path} does not exist, {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif cmd.startswith('echo '):
        # Remove 'echo ' from the beginning and print the rest of the command
        print(" ".join(cmd.split(" ")[1:]))

    elif cmd == 'cdtos':
        wd = os.path.dirname(os.path.abspath(__file__))

    else:
        history = False
    if history:
        with open('history.txt', 'a') as file:
            file.write('\n' + cmd)

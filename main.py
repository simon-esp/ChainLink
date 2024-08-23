import os
import hashlib
from getpass import getpass
from cryptography.fernet import Fernet

clear_command = input('your terminals cls command: ')
os.system(clear_command)
print('welcome to insider')
print('type help for help')
print('standard password is `123` but you can change it')
with open("data.txt", "r") as f:
    data = f.read()
    data = data.split("|",1)
    user = data[0]
    host = data[1]
wp = "/"
column_width = 30
superuser = False

def password():
    h = hashlib.new('sha256')
    h.update(getpass().encode())
    with open("password.txt", "r") as file_pass:
        readpass = file_pass.readline()
    return readpass == h.hexdigest()

def custom_encrypt_decrypt(key: bytes, text: str, operation: str) -> str:
    """
    Encrypts or decrypts text using the provided key.

    :param key: The encryption key (32-byte, URL-safe base64-encoded).
    :param text: The text to encrypt or decrypt.
    :param operation: Specify "encrypt" to encrypt the text or "decrypt" to decrypt it.
    :return: The encrypted or decrypted text.
    """
    cipher = Fernet(key)

    if operation == "encrypt":
        encrypted_text = cipher.encrypt(text.encode())
        return encrypted_text.decode()
    elif operation == "decrypt":
        decrypted_text = cipher.decrypt(text.encode())
        return decrypted_text.decode()
    else:
        raise ValueError("Invalid operation. Choose either 'encrypt' or 'decrypt'.")

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
        print('cdu {directory}        | add a path to your already existing working directory')
        print('cdd                    | go back 1 directory')
        print('pwd                    | print out current working directory')
        print('dispw {column width}   | edit the column width used for various commands like `ls`')
        print('clr                    | clears the terminal')
        print('su                     | enable super user [PASSWORD PROMPT]')
        print('exsu                   | exit super user')
        print('chsu                   | check wether you are super user or not')
        print('host {new host}        | change the host [SUPER COMMAND]')
        print('user {new user}        | change the username')
        print('pass {new pass}        | change the password [SUPER COMMAND] [PASSWORD PROMPT]')
        print('bcmd                   | gives a prompt to run in the systems terminal')
        print('cat {file}             | print the contents of a the file, has to be under your working directory')
        print(' ')

    if cmd == 'clr':
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
        with open("data.txt", "w") as f:  # Open file in write mode
            f.write(user + '|' + host)

    if cmd.startswith('host '):
        if superuser:
            host = cmd.split(" ",1)[1]
            with open("data.txt", "w") as f:  # Open file in write mode
                f.write(user + '|' + host)
        else:
            print('requires superuser')

    if cmd == 'bcmd':
        os.system(input('your command: '))

    if cmd.startswith('cat'):
        with open(wp + cmd.split(" ",1)[1], 'r') as f: # The with keyword automatically closes the file when you are done
            print (f.read())

    if cmd == 'cdd':
        dir_split = wp.split("/")
        dir_fuse = ''
        for i in range(len(dir_split) - 2):
            dir_fuse = dir_fuse + '/' + dir_split[i+1]
        wp = dir_fuse
        if wp == '':
            wp = '/'

    if cmd == 'sl':
        print('🚂')
    
    if cmd.startswith('copy '):
        split = cmd.split(" ")
        arg = split[1]
        if arg.startswith('-'):
            arg = arg.split("-")[1]
            if arg == 's':
                try:
                    full_path = wp + split[2]
                    print(f"Trying to open file: {full_path}")  # Debugging line
                    with open(full_path, 'r') as f:
                        content = f.read()
                    script_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(script_dir, 'icf§' + split[2])
                    with open(file_path, 'a') as f:
                        f.write(content)
                    print(f"File copied to {file_path}")
                except FileNotFoundError:
                    print(f"{full_path} does not exist")
                except Exception as e:
                    print(f"An error occurred: {e}")
            if arg == 'e':
                try:
                    full_path = wp + split[2]
                    print(f"Trying to open file: {full_path}")  # Debugging line
                    with open(full_path, 'r') as f:
                        content = f.read()
                        
                    key = Fernet.generate_key()
                    with open(script_dir, 'icfkey§' + split[2], 'a'):
                        f.write(key)

                    content = custom_encrypt_decrypt(key=key, text=content, operation='encrypt')
                    script_dir = os.path.dirname(os.path.abspath(__file__))

                    file_path = os.path.join(script_dir, 'icf§' + split[2])
                    with open(file_path, 'a') as f:
                        f.write(content)

                    print(f"File copied to {file_path}")

                except FileNotFoundError:
                    print(f"{full_path} does not exist")
                except Exception as e:
                    print(f"An error occurred: {e}")
        else:
            print('No valid arguments given')

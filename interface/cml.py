try:
    import kernel as k
    global kernel
    kernel = k.clk()
except:
    print('kernel not installed')
import os
import requests
import ast
import psutil
import platform
import GPUtil
import time
import curses

def process_monitor(screen):
    # Curses settings
    curses.curs_set(0)  # Hide cursor
    screen.nodelay(True)  # Make getch non-blocking
    max_y, max_x = screen.getmaxyx()  # Get screen dimensions
    header = f"{'PID':<10} | {'Name':<25} | {'CPU (%)':<10} | {'Memory (%)':<10}"
    separator = "-" * (len(header) + 10)  # Ensure separator fits within screen width
    while True:
        screen.clear()
        # Fetch process data
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            processes.append((proc.info['pid'], proc.info['name'], proc.info['cpu_percent'], proc.info['memory_percent']))
        # Print header
        screen.addstr(0, 0, header[:max_x])  # Ensure it doesn't exceed terminal width
        screen.addstr(1, 0, separator[:max_x])  # Ensure it fits within the width
        # Display processes
        for i, (pid, name, cpu, memory) in enumerate(processes):
            if i + 2 >= max_y:  # Prevent writing beyond screen height
                break
            name = name[:25] if len(name) > 25 else name  # Truncate long names
            screen.addstr(i + 2, 0, f"{pid:<10} | {name:<25} | {cpu:<10.2f} | {memory:<10.2f}"[:max_x])
        screen.refresh()
        # Check if 'q' is pressed to exit
        key = screen.getch()
        if key == ord('q'):
            break
        # Sleep to control refresh rate
        time.sleep(0.05)

def print_file_lines(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                print(line, end='')  # end='' prevents adding an extra newline
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_cpu_info_linux():
    with open('/proc/cpuinfo', 'r') as f:
        for line in f:
            if 'model name' in line:
                return line.split(':')[1].strip()

while True:
    cmd = input("Enter command: ")
    rem_cmd = ' '.join(cmd.split(' ')[1:])
    
    if cmd.startswith('write'):
        key = rem_cmd
        val = input(f'input value for "{key}": ')
        kernel.write(key.strip(), val.strip())
        print(f"Stored '{val.strip()}' to '{key.strip()}'")
    
    elif cmd.startswith('get'):
        key = cmd.split(' ')[1]
        value = kernel.get(key.strip())
        if value is not None:
            print(value)
        else:
            print(f"No value found for key: {key.strip()}")
            
    elif cmd.startswith('kernel'):
        print(kernel.getraw())

    elif cmd == 'clear':
        os.system('clear')

    elif cmd.startswith('clss'):
        kernel.clss_blocking(rem_cmd + '.clss')

    elif cmd.startswith('install'):
        print('fetching package dict from:')
        print('https://raw.githubusercontent.com/simon-esp/ChainLink/refs/heads/main/packages/packages.json')
        packs = ast.literal_eval(requests.get('https://raw.githubusercontent.com/simon-esp/ChainLink/refs/heads/main/packages/packages.json').text.strip('\n'))
        print('fethed packages')
        bytes = packs[rem_cmd + '_b']
        if input(f'package is {bytes} bytes, download? [n/y]: ').lower() == 'y':
            package_link = packs[rem_cmd + '_l']
            print(f'installing from {package_link}')
            pack = requests.get(package_link).text
            print('done installing')
            print('moving to file..')
            package_name = packs.get(f'{rem_cmd}_n', None)
            with open(package_name, 'w') as f:
                f.write(pack)
            pack = ""
            packs = ""
            print('moved to files and cleaned up memory')

    elif cmd.lower() == 'clfetch':
        print_file_lines('clfetchlogo.txt')
        system_info = {}
        virtual_memory = psutil.virtual_memory()
        system_info['Total memory'] = f"{virtual_memory.total / (1024 ** 2):.2f} MB"
        system_info['Available memory'] = f"{virtual_memory.available / (1024 ** 2):.2f} MB"
        system_info['Used memory'] = f"{virtual_memory.used / (1024 ** 2):.2f} MB"
        system_info['Memory percent used'] = f"{virtual_memory.percent}%"

        # OS Information
        system_info['OS'] = f"{platform.system()} {platform.release()} ({platform.version()})"
        system_info['Architecture'] = platform.architecture()[0]
        system_info['Hostname'] = platform.node()
        system_info['Python Version'] = platform.python_version()

        # CPU Information
        system_info['CPU'] = get_cpu_info_linux()
        system_info['CPU Cores'] = psutil.cpu_count(logical=False)

        # Disk Usage
        disk_usage = psutil.disk_usage('/')
        system_info['Total Disk'] = f"{disk_usage.total / (1024 ** 3):.2f} GB"
        system_info['Used Disk'] = f"{disk_usage.used / (1024 ** 3):.2f} GB"
        system_info['Free Disk'] = f"{disk_usage.free / (1024 ** 3):.2f} GB"

        #GPU Information
        gpus = GPUtil.getGPUs()
        if gpus:
            for gpu in gpus:
                system_info['GPU'] = gpu.name
                system_info['GPU Memory Free'] = f"{gpu.memoryFree} MB"
                system_info['GPU Memory Used'] = f"{gpu.memoryUsed} MB"
                system_info['GPU Memory Total'] = f"{gpu.memoryTotal} MB"
                system_info['GPU Temperature'] = f"{gpu.temperature} °C"
        else:
            system_info['GPU'] = 'couldnt fetch gpu info'
        
        # Battery
        battery = psutil.sensors_battery()
        system_info['Battery'] = f"{battery}"
        
        for key, value in system_info.items():
            print(f"{key: <20}| {value}")
        print('\n')
        
    elif cmd.lower() == 'exit':
        break
    
    elif cmd.lower() == 'clpi':
        curses.wrapper(process_monitor)

    else:
        print(f"'{cmd}' is invalid sorry man")

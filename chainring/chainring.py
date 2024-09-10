import kernel
import interpreter

kernel = kernel.Memory()

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

    elif cmd.startswith('clss'):
        kernel.clss_blocking(rem_cmd + '.clss')

    elif cmd.lower() == 'exit':
        break
    else:
        print("idk what that means sorry man")

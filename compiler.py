import time

def get_scr(file):
    # Fetch file and turn into 1 string, no newlines
    try:
        with open(file, "r") as f:
            script = f.readlines()
            script = ''.join([line.strip() for line in script])
        return script
    except Exception as e:
        print('File was not found, or an error occurred')
        print(f'Error: {e}')
        return(";")
    
def eval(value):
    global variables
    if value[0] == '$':
        return variables.get(value)
    if value[0] == '"' and value[len(value)-1]:
        return value[1:len(value)-1]
    if value[0] + value[1] == '+!':
        return int(eval(value.split('!')[1])) + int(eval(value.split('!')[2]))
    if value[0] + value[1] == '-!':
        return int(eval(value.split('!')[1])) - int(eval(value.split('!')[2]))
    if value[0] + value[1] == '*!':
        return int(eval(value.split('!')[1])) * int(eval(value.split('!')[2]))
    if value[0] + value[1] == '/!':
        return int(eval(value.split('!')[1])) / int(eval(value.split('!')[2]))

def line(k,i):
    split = i.split(' ')

    if split[0] == 'v':
        key, value = " ".join(i.split(" ")[1:]).split('=', 1)
        value = eval(value)
        variables[key] = value

    if split[0] == 'wait':
        if split[1][0] == '$':
            time.sleep(int(variables.get(split[1])))
        else:
            time.sleep(int((" ".join(i.split(" ")[1:]))))
            
    if split[0] == 'echo':
        if split[1][0] == '$':
            print(variables.get(split[1]))
        else:
            print(" ".join(i.split(" ")[1:]))

    if split[0] == 'rep':
        iterate = " ".join(i.split(" ")[1:])
        iterate = " ".join(iterate.split(" ")[1:])
        iterate.replace(';', '')
        print(iterate)
        print(int(split[1]))
        for g in range(int(split[1])):
            for j,h in enumerate(iterate):
                line(j,h)

def compile(file):
    global variables
    variables = {}
    s = get_scr(file=file) # `s` is the script without newlines, which means its the script to compile
    s = s.split(';')
    s.pop(len(s)-1)
    print(s)
    for k,i in enumerate(s):
        line(k,i)
        

compile(r"C:\Users\spoki\OneDrive\chainlink\helloworld.cks") #temporary for easier testing

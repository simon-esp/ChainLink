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
    if value[0] == '"' and value[len(value)-1]:
        return value[1:len(value)-1]

def compile(file):
    vars = {}
    s = get_scr(file=file) # `s` is the script without newlines, which means its the script to compile
    s = s.split(';')
    s.pop(len(s)-1)
    print(s)
    for k,i in enumerate(s):

        split = i.split(' ')

        if split[0] == 'v':
            key, value = " ".join(i.split(" ")[1:]).split('=', 1)
            value = eval(value)
            vars[key] = value

        if split[0] == 'echo':
            if split[1][0] == '$':
                print(vars.get(split[1]))
            else:
                print(" ".join(i.split(" ")[1:]))

compile(r"C:\Users\spoki\OneDrive\chainlink\helloworld.cks") #temporary for easier testing

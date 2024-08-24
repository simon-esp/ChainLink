def get_scr(file):
    try:
        with open(file, "r") as f:
            script = f.readlines()
            script = ''.join([line.strip() for line in script])
        return script
    except Exception as e:
        print('File was not found, or an error occurred')
        print(f'Error: {e}')
        return(";")

def compile(file):
    s = get_scr(file=file) # `s` is the script without newlines, which means its the script to compile
    s = s.split(';')
    print(s)

compile(r"C:\Users\spoki\OneDrive\chainlink\helloworld.cks") #temporary for easier testing

import time
import ast

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
        return ";"
    
def condition(c):
    global variables
    try:
        r = c.split('|')[1]
        if r == 'F':
            r = False
        else:
            r == True
    except:
        r = True
    s = c.split('|')[0]
    operator = s.split(' ')[1]
    match operator:
        case '=':
            operands = s.split(' ')
            cond = float(eval_expression(operands[0])) == float(eval_expression(operands[2]))
    if cond:
        if r:return True
        else:return False
    else:
        if r:return False
        else: return True
def eval_expression(value):
    global variables
    split = value.split(' ')
    try:
        if split[1] == '+':
            operands = value.split(' ')
            return float(eval_expression(operands[0])) + float(eval_expression(operands[2]))
        if value[1] == '-':
            operands = value.split(' ')
            return float(eval_expression(operands[0])) - float(eval_expression(operands[2]))
        if value[1] == '*':
            operands = value.split(' ')
            return float(eval_expression(operands[0])) * float(eval_expression(operands[2]))
        if value[1] == '/':
            operands = value.split(' ')
            return float(eval_expression(operands[0])) / float(eval_expression(operands[2]))
    except:
        if value[0] == '$':
            return variables.get(value, 0)  # Default to 0 if the variable is not found
        if value[0] == "'" and value[-1] == "'":
            return value[1:-1]

def execute_line(i):
    global variables
    split = i.split(' ')
    match split[0]:

        case 'v':
            key, value = " ".join(i.split(" ")[1:]).split('=', 1)
            value = eval_expression(value)
            variables[key] = value
        
        case 'wait':
            if split[1][0] == '$':
                time.sleep(float(variables.get(split[1], 0)))
            else:
                time.sleep(float(split[1]))

        case 'echo':
            if split[1][0] == '$':
                print(variables.get(split[1], ''))
            else:
                print(" ".join(i.split(" ")[1:]))
        
        case 'rep':
            rep_count = int(split[1])
            script_to_repeat = ast.literal_eval('[' + ','.join(f'"{item.strip()}"' for item in (" ".join(i.split(" ")[2:]).strip().strip(';')).strip('[]').split(',')) + ']')
            for _ in range(rep_count):
                execute_script(script_to_repeat)

        case 'if':
            if condition(" ".join(i.split(" ")[1:]).strip().strip(';').split(":")[0]):
                script_to_do = ast.literal_eval('[' + ','.join(f'"{item.strip()}"' for item in (" ".join(i.split(" ")[1:]).strip().strip(';').split(":")[1]).strip('[]').split(',')) + ']')
                execute_script(script_to_do)
                
def execute_script(script):
    global variables
    for line in script:
        if line.strip():
            execute_line(line.strip())

def load(file):
    global variables
    variables = {}
    s = get_scr(file=file)  # `s` is the script without newlines, which means it's the script to compile
    lines = s.split(';')
    execute_script(lines)

# Example usage
load(r"C:\Users\spoki\OneDrive\chainlink\helloworld.cks")  # Update the path as needed

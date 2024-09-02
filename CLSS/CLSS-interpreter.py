def parse(p):
    s =  ''.join(p.splitlines())
    nesting = 0
    final = []
    comment = False
    string = ''
    indent = True
    for l,i in enumerate(s):
        if not l == len(s) - 1:
            if i == '~':
                comment = not comment
        if i == '{' and not comment:
            nesting += 1
        if i == '}' and not comment:
            nesting -= 1
        if not i == ' ':
            indent = False
        if i == ';' and nesting == 0 and not comment:
            final.append(string)
            string = ''
            indent = True
        elif not indent and not comment and not i == '~':
            string = string+i
    return(final)

def find_functions(p):
    global funcs
    for i in p:
        match i.split(' ')[0]:
            case 'def':
                keyword_gone = ' '.join(i.split(' ')[1:])
                p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                funcs[(' '.join(i.split(' ')[1:]).split(':')[0])] = p
    
def parse_eval(k):
    quotes = False
    array = []
    s = ''
    for i in k:
        if i == '"':
            quotes = not quotes  # Toggle quotes state
        if i == ' ' and not quotes:
            array.append(s)
            s = ''
        else:
            s += i
    if s:  # Add the last segment
        array.append(s)
    return array

def eval(e):
    global vars, lists
    if e.strip('-').isnumeric():
        return int(e)
    elif e.startswith('"') and e.endswith('"'):
        return e[1:-1]
    elif e in vars:
        return vars.get(e, None)
    elif e in lists:
        return lists.get(e, None)

    # Parsing more complex expressions
    l = parse_eval(e)
    f = eval(l[0])
    l.pop(0)
    while len(l) > 0:
        if l[0] == '+':
            f = int(f) + int(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '-':
            f = int(f) - int(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '*':
            f = int(f) * int(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '/':
            f = int(f) // int(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '++':
            f = str(f) + str(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '**':
            f = str(f) * int(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '=':
            f = str(f) == str(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '>':
            f = str(f) > str(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '<':
            f = str(f) < str(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == '!=':
            f = str(f) != str(eval(l[1]))
            l.pop(0); l.pop(0)
        elif l[0] == 'in':
            s = lists[str(eval(l[1]))]
            f = s[int(f)]
            l.pop(0); l.pop(0)
        elif l[0] == 'of':
            s = eval(l[1])
            print(s)
            f = s[int(f)]
            l.pop(0); l.pop(0)
        elif l[0] == 'len':
            f = len(str(f))
            l.pop(0)
        elif l[0] == 'chr':
            f = chr(int(f))
            l.pop(0)
        elif l[0] == 'ord':
            f = ord(str(f))
            l.pop(0)
        else:
            break  # If operator not recognized, break out
    return f

def interpret(s):
    global vars
    global funcs
    global lists
    global brk
    for i in s:
        if brk >= 1:
            brk -= 1
            break
        keyword_gone = ' '.join(i.split(' ')[1:])
        match i.split(' ')[0]:      
            case 'echo':
                print(eval(keyword_gone))
            case 'if':
                if eval(keyword_gone.split(':')[0]):
                    p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                    interpret(p)
            case 'rep':
                p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                for i in range(int(eval(keyword_gone.split(':')[0]))):
                    if brk >= 1:
                        brk -= 1
                        break
                    interpret(p)
            case 'while':
                p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                while eval(keyword_gone.split(':')[0]):
                    if brk >= 1:
                        brk -= 1
                        break
                    interpret(p)
            case 'var':
                vars[keyword_gone.split('=')[0]] = eval('='.join(keyword_gone.split('=')[1:]))
            case 'call':
                interpret(funcs[keyword_gone])
            case 'input':
                vars[keyword_gone.split(':')[0]] = input(eval(':'.join(keyword_gone.split(':')[1:])))
            case 'brake':
                brk = int(eval(keyword_gone))
            case 'halt':
                brk = 9999999999999999999999999999999999999999999999999999
            case 'append':
                new_val = eval('='.join(keyword_gone.split('=')[1:]))
                key = keyword_gone.split('=')[0]
                old_val = lists.get(key, [])
                old_val.append(new_val)
                lists[key] = old_val
            case 'declare':
                lists[keyword_gone.split('=')[0]] = []
            case 'puncture':
                new_val = eval(':'.join(keyword_gone.split(':')[1:]))
                key = keyword_gone.split(':')[0]
                old_val = lists.get(key, [])
                old_val.pop(int(new_val))
                lists[key] = old_val
            case 'change':
                new_val = eval('='.join(keyword_gone.split('=')[1:]))
                key = keyword_gone.split(':')[0]
                item = int(eval(keyword_gone.split(':')[1].split('=')[0]))
                old_val = lists.get(key, [])
                old_val[item] = new_val
                lists[key] = old_val

import time
start_time = time.time()
global vars
global lists
global brk
vars = {}
funcs = {}
brk = False
lists = {}
with open('C:\\Users\\spoki\\OneDrive\\chainlink\\test.clss', 'r') as f:
        s = f.read()
script = parse(s)
find_functions(script)
interpret(script)
end_time = time.time()
elapsed_time_ms = (end_time - start_time)
print(f"Finished in {elapsed_time_ms:.2f} seconds")

def parse(p):
    s =  ''.join(p.splitlines())
    nesting = 0
    final = []
    string = ''
    indent = True
    for i in s:
        if i == '{':
            nesting += 1
        if i == '}':
            nesting -= 1
        if not i == ' ':
            indent = False
        if i == ';' and nesting == 0:
            final.append(string)
            string = ''
            indent = True
        elif not indent:
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

def condition(cond):
    if cond == 'True':
        return True
    if cond == 'False':
        return False
    l = cond.split(' ')
    if l[1] == '>':
        return int(eval(l[0])) + int(eval(l[2]))
    
def eval(c):
    global vars
    if c.startswith('e'):
        e = c[1:]
        if str(e).startswith('$') and not ' ' in str(e):
            return vars[e.strip('$')]
        if str(e).isnumeric():
            return e
        if str(e).startswith('"') and str(e).endswith('"'):
            return e[1:-1]
        l = e.split(' ')
        if l[1] == '+':
            return int(eval(l[0])) + int(eval(l[2]))
        if l[1] == '++':
            return str(eval(l[0])) + str(eval(l[2]))
        if l[1] == '/':
            return int(eval(l[0])) / int(eval(l[2]))
        if l[1] == '*':
            return int(eval(l[0])) * int(eval(l[2]))
        if l[1] == '-':
            return int(eval(l[0])) - int(eval(l[2]))
    
            

def interpret(s):
    global vars
    global funcs
    for i in s:
        keyword_gone = ' '.join(i.split(' ')[1:])
        match i.split(' ')[0]:      
            case 'echo':
                print(eval(keyword_gone))
            case 'if':
                if condition(keyword_gone.split(':')[0]):
                    p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                    interpret(p)
            case 'rep':
                p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                for i in range(int(eval(keyword_gone.split(':')[0]))):
                    interpret(p)
            case 'while':
                p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                while condition(keyword_gone.split(':')[0]):
                    interpret(p)
            case 'var':
                vars[keyword_gone.split('=')[0]] = eval('='.join(keyword_gone.split('=')[1:]))
            case 'var+':
                vars[keyword_gone.split('=')[0]] = int(eval(vars[keyword_gone.split('=')[0]])+int('='.join(keyword_gone.split('=')[1:])))
            case 'call':
                interpret(funcs[keyword_gone])
            case 'input':
                vars[keyword_gone.split(':')[0]] = input(eval(':'.join(keyword_gone.split(':')[1:])))

global vars
vars = {}
funcs = {}
with open('C:\\Users\\spoki\\OneDrive\\chainlink\\test.clss', 'r') as f:
        s = f.read()
script = parse(s)
find_functions(script)
interpret(script)

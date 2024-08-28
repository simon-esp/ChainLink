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
                p = parse(':'.join(' '.join(i.split(' ')[1:].split(':')[1:])[1:-1]))
                funcs[(' '.join(i.split(' ')[1:]).split(':')[0])] = p
                print(p)

def condition(cond):
    if cond == 'True':
        return True
    if cond == 'False':
        return False

def interpret(s):
    global vars
    global funcs
    for i in s:
        keyword_gone = ' '.join(i.split(' ')[1:])
        match i.split(' ')[0]:      
            case 'echo':
                print(vars[keyword_gone.strip('$')] if keyword_gone[0] == '$' else keyword_gone)
            case 'if':
                if condition(keyword_gone.split(':')[0]):
                    p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                    interpret(p)
            case 'rep':
                p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                for i in range(int(keyword_gone.split(':')[0])):
                    interpret(p)
            case 'var':
                vars[keyword_gone.split('=')[0]] = '='.join(keyword_gone.split('=')[1:])
            case 'var+':
                vars[keyword_gone.split('=')[0]] = int(vars[keyword_gone.split('=')[0]])+int('='.join(keyword_gone.split('=')[1:]))

global vars
vars = {}
with open('C:\\Users\\spoki\\OneDrive\\chainlink\\test.clss', 'r') as f:
        s = f.read()
script = parse(s)
find_functions(script)
interpret(script)
print(script)

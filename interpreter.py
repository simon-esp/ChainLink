def parse(p):
    s =  ''.join(p.splitlines())
    nesting = 0
    x = []
    y = ''
    for i in s:
        if i == '{':
            nesting += 1
        if i == '}':
            nesting -= 1
        if i == ';' and nesting == 0:
            x.append(y)
            y = ''
        else:
            y = y+i
    return(x)

def condition(cond):
    if cond == 'True':
        return True
    if cond == 'False':
        return False

def interpret(s):
    
    for i in s:
        keyword_gone = ' '.join(i.split(' ')[1:])
        match i.split(' ')[0]:      
            case 'echo':
                print(keyword_gone)
            case 'if':
                if condition(keyword_gone.split(':')[0]):
                    p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                    interpret(p)


with open('/home/simonesp/test.clss', 'r') as f:
        s = f.read()
interpret(parse(s))

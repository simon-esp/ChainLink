import time
import os
import kernel
import keyboard

def parse(p):
    s = ''.join(p.splitlines())
    nesting = 0
    final = []
    comment = False
    string = ''
    indent = True
    for l, i in enumerate(s):
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
            string += i
    return final

def find_functions(p):
    funcs_temp = {}
    for i in p:
        if i.startswith('def '):
            func_name = i.split(' ')[1].split(':')[0]
            func_body = ':'.join(i.split(':')[1:])[1:-1]
            parsed_body = parse(func_body)
            funcs_temp[func_name] = parsed_body
    return funcs_temp

def parse_eval(k):
    quotes = False
    array = []
    s = ''
    for i in k:
        if i == '"':
            quotes = not quotes
        if i == ' ' and not quotes:
            array.append(s)
            s = ''
        else:
            s += i
    if s:
        array.append(s)
    return array

def eval(e):
    #print(e+".")
    global vars, lists
    if e.strip('-').strip('.').isnumeric():
        return int(e)
    elif e.startswith('"') and e.endswith('"'):
        return e[1:-1]
    elif e in vars:
        return vars.get(e, None)
    elif e in lists:
        return lists.get(e, None)
    elif e.startswith('$$'):
        with open(str(e.strip('*$')), 'r') as file:
            return file.readlines()
    elif e.startswith('*$'):
        with open(str(e.strip('*$')), 'r') as file:
            return file.readline()
    elif e.startswith('*'):
        with open(str(e.strip('*')), 'r') as file:
            return file.read()
    elif e.startswith('#') and not " " in e:
        return eval(arguments[int(e.strip('#'))])
    elif e.startswith('%'):
        return kernel.clk().get(eval(str(e.strip('%'))))
    elif e.startswith('?'):
        f = e.strip('?')

        module = f.split(' ')[0]
        func_call = ' '.join(f.split(' ')[1:])
        func_name, func_args = func_call.split(' ', 1)
        if module in mods and func_name in mods[module]:
            return interpret(mods[module][func_name], func_args[1:-1].split(', '))
        else:
            return f"Function {func_name} in module {module} not found"
    elif e == 'file-dirname':
        return os.path.dirname(os.path.abspath(__file__))
    elif e == 'get-all-mem':
        return kernel.clk().getraw()
    elif e == 'lcp':
        return list(kernel.clk().get('pressed_keys'))[-1]
    elif e == 'kp':
        return not len(list(kernel.clk().get('pressed_keys'))) <= 0

    # More complex expression parsing
    if e.startswith('p"') and e.endswith('"'):
        e = e[1:]
    l = parse_eval(e)
    if not l:
        return None  # Avoid popping from an empty list
    f = eval(l[0])
    l.pop(0)
    
    while len(l) > 0:
        op = l.pop(0)
        if op in {'len', 'lenl', 'chr', 'ord', 'func', 'keyprs', 'rev'}:  # Unary operations
            if op == 'len':
                f = len(str(f))
            if op == 'lenl':
                f = len(list(f))
            elif op == 'chr':
                f = chr(int(f))
            elif op == 'ord':
                f = ord(str(f))
            elif op == 'func':
                f = interpret(funcs[f])
            elif op == 'keyprs':
                f = f in kernel.clk().get('pressed_keys')
            elif op == 'rev':
                f = not f
            continue
        
        if len(l) == 0:
            raise ValueError("Missing operand for operation")  # Handle missing operand

        operand = eval(l.pop(0))
        if op == '+':
            f = int(f) + int(operand)
        elif op == '-':
            f = int(f) - int(operand)
        elif op == '--':
            f = str(f)[:len(str(f)) - int(operand)]
        elif op == '*':
            f = int(f) * int(operand)
        elif op == '/':
            f = int(f)  / int(operand)

        elif op == '%':
            f = int(f) % int(operand)
        elif op == '++':
            f = str(f) + str(operand)
        elif op == '**':
            f = str(f) * int(operand)
        elif op == '=':
            f = str(f) == str(operand)
        elif op == '!=':
            f = str(f) != str(operand)
        elif op == '>':
            f = str(f) > str(operand)
        elif op == '<':
            f = str(f) < str(operand)
        elif op == 'in':
            f = lists[str(operand)][int(f)]
        elif op == 'of':
            f = operand[int(f)]
    return f

def interpret(s, args=None):
    global vars, funcs, lists, brk, mods
    if args:
        global arguments
        arguments = args

    for i in s:
        if brk >= 1:
            brk -= 1
            break
        keyword_gone = ' '.join(i.split(' ')[1:])
        match i.split(' ')[0]:
            case 'echo':
                print(eval(keyword_gone))
            case 'sleep':
                time.sleep(float(eval(keyword_gone)))
            case 'if':
                if eval(keyword_gone.split(':')[0]):
                    p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                    interpret(p)
            case 'rep':
                p = parse(':'.join(keyword_gone.split(':')[1:])[1:-1])
                for _ in range(int(eval(keyword_gone.split(':')[0]))):
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
                if keyword_gone.split(' ')[0] in funcs:
                    func_name, func_args = keyword_gone.split(' ')
                    interpret(funcs[func_name], func_args[1:-1].split(', '))
                else:
                    print(f"Function {keyword_gone.split(' ')[0]} not found")
            case 'input':
                vars[keyword_gone.split(':')[0]] = input(eval(':'.join(keyword_gone.split(':')[1:])))
            case 'brake':
                brk = int(eval(keyword_gone))
            case 'passat':
                while not eval(keyword_gone):
                    pass
            case 'halt':
                brk = float('inf')
            case 'sys-cmd':
                os.system(eval(keyword_gone))
            case 'append':
                new_val = eval('='.join(keyword_gone.split('=')[1:]))
                key = keyword_gone.split('=')[0]
                old_val = lists.get(key, [])
                old_val.append(new_val)
                lists[key] = old_val
            case 'declare':
                lists[keyword_gone.split('=')[0]] = []
            case 'puncture':
                key = keyword_gone.split(':')[0]
                new_val = int(eval(':'.join(keyword_gone.split(':')[1:])))
                old_val = lists.get(key, [])
                if new_val < len(old_val):
                    old_val.pop(new_val)
                    lists[key] = old_val
            case 'change':
                new_val = eval('='.join(keyword_gone.split('=')[1:]))
                key = keyword_gone.split(':')[0]
                item = int(eval(keyword_gone.split(':')[1].split('=')[0]))
                old_val = lists.get(key, [])
                if item < len(old_val):
                    old_val[item] = new_val
                    lists[key] = old_val
            case 'w-mem':
                memory_instance = kernel.clk()
                memory_instance.write(str(eval(keyword_gone.split('=')[0])), str(eval('='.join(keyword_gone.split('=')[1:]))))
            case 'import':
                if '=' in keyword_gone:
                    module_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), keyword_gone.split('=')[0])
                    module_name = keyword_gone.split('=')[1]
                else:
                    module_file = keyword_gone
                    module_name = keyword_gone
                with open(module_file + '.clss', 'r') as f:
                    module_script = parse(f.read())
                mods[module_name] = find_functions(module_script)
            case 'mod':
                module = keyword_gone.split(' ')[0]
                func_call = ' '.join(keyword_gone.split(' ')[1:])
                func_name, func_args = func_call.split(' ', 1)
                if module in mods and func_name in mods[module]:
                    interpret(mods[module][func_name], func_args[1:-1].split(', '))
                else:
                    print(f"Function {func_name} in module {module} not found")
            case 'return':
                return eval(keyword_gone)
            case 'pack':
                f = keyword_gone
                module = f.split(' ')[0]
                func_call = ' '.join(f.split(' ')[1:])
                func_name, func_args = func_call.split(' ', 1)
                if module in mods and func_name in mods[module]:
                    interpret(mods[module][func_name], func_args[1:-1].split(', '))
                else:
                    print(f"Function {func_name} in module {module} not found")
            case 'render':
                memory_instance = kernel.clk()
                memory_instance.graphics()

def raw_clss(code):
    start_time = time.time()
    global vars, lists, brk, funcs, mods
    mods = {}
    vars = {}
    brk = 0
    lists = {}
    script = parse(code)
    funcs = find_functions(script)
    interpret(script)
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time)
    print(f"Finished in {elapsed_time_ms:.2f} ms")

def clss(dir):
    start_time = time.time()
    global vars, lists, brk, funcs, mods
    mods = {}
    vars = {}
    funcs = {}
    brk = 0
    lists = {}
    with open(dir, 'r') as f:
        script = parse(f.read())
    funcs = find_functions(script)
    interpret(script)
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time)
    print(f"Finished in {elapsed_time_ms:.2f} ms")

if __name__ == '__main__':
    clss('/home/simonesp/Documents/python/chainlink/test.clss')

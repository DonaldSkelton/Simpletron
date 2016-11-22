class token:
    def __init__(self, type = None, value = ''):
        self.type = type
        self.value = value

def evalMath(tokens):
    postfix = []
    opstack = []
    precedence = {'*': 5,
                  '/': 4,
                  '+': 3,
                  '-': 2,
                  '(': 1}
    for t in tokens:
        if t.type != 'operator':
            postfix.append(t)
        elif t.value == '(':
            opstack.append(t)
        elif t.value == ')':
            while opstack:
                t = opstack.pop()
                if t.value == '(':
                    break
                else:
                    postfix.append(t)
        else:
            if opstack:
                temp = opstack[-1]
            while opstack and precedence[temp.value] >= precedence[t.value]:
                postfix.append(opstack.pop())
                temp = opstack[-1]
            opstack.append(t)
    while opstack:
        postfix.append(opstack.pop())
    return postfix

math = [token('var', 'A'), token('operator', '+'), token('var', 'B'), token('operator', '*'),
        token('operator', '('), token('var', 'C'), token('operator', '+'), token('var', 'D'), token('operator', ')')]

post = evalMath(math)

for t in post:
    print(t.value, end='')

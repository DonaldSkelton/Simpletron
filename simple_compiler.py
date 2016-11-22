class token:
    def __init__(self, type = None, value = ''):
        self.type = type
        self.value = value

class lexer:
    def __init__(self, fname):
        self.tokens = []
        self.file = open(fname, 'r')

    def tokenize(self):
        operators= '()+-*/=!<>'
        for n, line in enumerate(self.file):
            self.tokens.append([])
            pos = 0
            current_token = token()
            try:
                for i in range(len(line) +1):
                    if line[i].isdigit() or (line[i] in '+-' and line[i+1].isdigit() and (i != 0 and not line[i-1].isdigit())):
                        current_token.type = 'int'
                        current_token.value += line[i]
                        if line[i+1].isdigit():
                            continue
                        else:
                            self.tokens[n].append(current_token)
                            current_token = token()
                            continue
                    elif line[i].isalpha():
                        if current_token.type == 'var':
                            current_token.type = 'word'
                        elif current_token.type == None:
                            current_token.type = 'var'
                        current_token.value += line[i]
                        if line[i+1].isalpha():
                            continue
                        else:
                            self.tokens[n].append(current_token)
                            current_token = token()
                            continue
                    elif line[i] in operators:
                        current_token.type = 'operator'
                        current_token.value += line[i]
                        if line[i+1] in operators:
                            continue
                        else:
                            self.tokens[n].append(current_token)
                            current_token = token()
                            continue
                    elif line[i].isspace():
                        continue
                    else:
                        raise SyntaxError('Bad token on Line: '+str(n)+' Position: '+str(i))
            except IndexError:
                continue
        return self.tokens

class symbol:
    def __init__(self, name='', type=None, address=0):
        self.name = name
        self.type = type
        self.address = address

class flag:
    def __init__(self, address=0, symbol=''):
        self.address = address
        self.symbol = symbol

class symbolTable:
    def __init__(self):
        self.Symbols = []
        self.Flags = []
        self.stackCounter = 99


    def getSymbol(self, name, type, address=-1):
        if address == -1: address = self.stackCounter
        for s in self.Symbols:
            if s.name == name:
                return s
        if type == 'V' and name[-4:].isdigit(): #ignore sign
            type = 'C'
        s = symbol(name, type, address)
        if type != 'L':
            self.stackCounter -= 1
        self.Symbols.append(s)
        return s

    def lookupSymbol(self, name, address):
        for s in self.Symbols:
            if s.name == name:
                return (s.address, False)
        self.Flags.append(flag(address, name))
        return (0, True)

    def __contains__(self, x):
        for s in self.Symbols:
            if s.name == x:
                return True
        else:
            return False



class compiler:
    def __init__(self, infile, ofile=''):
        if not ofile:
            self.ofile = infile[0:-infile[::-1].find('.')]+'sml'
        else:
            self.ofile = ofile
        self.Tokens = lexer(infile).tokenize()
        self.Output = []
        self.Symbols = symbolTable()
        self.instructionCounter = 0
        self.Keywords = ['rem', 'input', 'let', 'print', 'goto', 'if', 'end']
        self.TempCount = 0

    def postfix(self, tokens):
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

    def writeOperation(self, op, evalStack, tempStore):
        opcodes = { '+': 3000,
                    '-': 3100,
                    '/': 3200,
                    '*': 3300}
        opAddress = evalStack.pop()
        loadAddress = evalStack.pop()
        self.Output.append(2000 + loadAddress)
        self.instructionCounter += 1
        self.Output.append(opcodes[op] + opAddress)
        self.instructionCounter += 1
        if tempStore:
            storeAddress = self.Symbols.getSymbol('temp'+str(self.TempCount), 'V').address
            self.TempCount += 1
            self.Output.append(2100 + storeAddress)
            self.instructionCounter += 1
            evalStack.append(storeAddress)


    def evalMath(self, tokens):
        postfix = self.postfix(tokens)
        evalStack = []
        for i, token in enumerate(postfix):
            tempStore = False
            if token.type != 'operator':
                evalStack.append(self.Symbols.getSymbol(token.value, 'V').address)
            else:
                if i != len(postfix) - 1:
                    tempStore = True
                self.writeOperation(token.value, evalStack, tempStore)




    def evalComparison(self, tokens):
        val1 = tokens[0].value
        val2 = tokens[2].value
        op = tokens[1].value
        dest = tokens[4].value
        if op == '<':
            self.Output.append(2000+self.Symbols.getSymbol(val1, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3100+self.Symbols.getSymbol(val2, 'V').address)
            self.instructionCounter += 1
            self.Output.append(4100+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1
        elif op == '<=':
            self.Output.append(2000+self.Symbols.getSymbol(val1, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3100+self.Symbols.getSymbol(val2, 'V').address)
            self.instructionCounter += 1
            self.Output.append(4100+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1
            self.Output.append(4200+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1
        elif op == '>':
            self.Output.append(2000+self.Symbols.getSymbol(val2, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3100+self.Symbols.getSymbol(val1, 'V').address)
            self.instructionCounter += 1
            self.Output.append(4100+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1
        elif op == '>=':
            self.Output.append(2000+self.Symbols.getSymbol(val2, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3100+self.Symbols.getSymbol(val1, 'V').address)
            self.instructionCounter += 1
            self.Output.append(4100+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1
            self.Output.append(4200+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1
        elif op == '==':
            self.Output.append(2000+self.Symbols.getSymbol(val1, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3100+self.Symbols.getSymbol(val2, 'V').address)
            self.instructionCounter += 1
            self.Output.append(4200+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1
        elif op == '!=':
            self.Output.append(2000+self.Symbols.getSymbol(val1, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3100+self.Symbols.getSymbol(val2, 'V').address)
            self.instructionCounter += 1
            self.Output.append(4200+self.instructionCounter+2)
            self.instructionCounter += 1
            self.Output.append(4000+self.Symbols.lookupSymbol(dest, self.instructionCounter)[0])
            self.instructionCounter += 1


    def firstPass(self):
        for line in self.Tokens:
            lineNumber = line[0]
            if (lineNumber.type == 'int' and
            lineNumber.value not in self.Symbols):
                self.Symbols.getSymbol(lineNumber.value, 'L', self.instructionCounter)
            else:
                raise SyntaxError('Invalid Line Number: '+lineNumber.value)
            command = line[1]
            if (command.type != 'word' or
            command.value not in self.Keywords):
                raise SyntaxError('Invalid Command: '+command.value)
            if command.value == 'rem':
                continue
            elif command.value == 'input':
                var = self.Symbols.getSymbol(line[2].value, 'V')
                self.Output.append(1000+var.address)
                self.instructionCounter += 1
                continue
            elif command.value == 'let':
                var = self.Symbols.getSymbol(line[2].value, 'V')
                self.evalMath(line[4:])
                self.Output.append(2100 + var.address)
                self.instructionCounter += 1
                continue
            elif command.value == 'print':
                address, flagged = self.Symbols.lookupSymbol(line[2].value, self.instructionCounter)
                self.Output.append(1100 + address)
                self.instructionCounter += 1
                continue
            elif command.value == 'goto':
                address, flagged = self.Symbols.lookupSymbol(line[2].value, self.instructionCounter)
                self.Output.append(4000 + address)
                self.instructionCounter += 1
                continue
            elif command.value == 'if':
                self.evalComparison(line[2:])
            elif command.value == 'end':
                self.Output.append(4300)
                self.instructionCounter += 1
                continue
            else:
                raise SyntaxError('Invalid Command: '+command.value)

    def secondPass(self):
        for flag in self.Symbols.Flags:
            address, stillFlagged = self.Symbols.lookupSymbol(flag.symbol, flag.address)
            if not stillFlagged:
                self.Output[flag.address] += address
            else:
                raise NameError('Could Not Resolve Symbol: '+flag.symbol)

    def insertConstants(self):
        found = False
        constants = []
        for symbol in self.Symbols.Symbols:
            if symbol.type == 'C':
                found = True
                constants.append(symbol)
        if found:
            temp = [0 for _ in range(100 - len(self.Output))]
            self.Output += temp
        for symbol in constants:
            self.Output[symbol.address] = int(symbol.name)

    def writeFile(self):
        with open(self.ofile, 'w') as ofile:
            for line in self.Output:
                ofile.write('{0:0=+5d}'.format(line)+'\n')

if __name__ == '__main__':
    infile = input('File to be compiled: ')
    c = compiler(infile)
    c.firstPass()
    c.secondPass()
    c.insertConstants()
    c.writeFile()

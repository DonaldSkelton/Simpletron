

tempCount = 0

for i, t in enumerate(postfix):
    if t.type == 'operator':
        if t.value == '+':
            self.Output.append(2000+self.Symbols.getSymbol(postfix[i-2].value, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3000+self.Symbols.getSymbol(postfix[i-1].value, 'V').address)
            self.instructionCounter += 1
            if i != len(postfix)-1:
                temp = 'temp'+str(tempCount)
                tempCount += 1
                postfix[i] = token('var', temp)
                self.Output.append(2100+self.Symbols.getSymbol(temp, 'V').address)
                self.instructionCounter += 1
                if i - 3 >= 0:
                    postfix[i-1] = postfix[i-3]
        elif t.value == '-':
            self.Output.append(2000+self.Symbols.getSymbol(postfix[i-2].value, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3100+self.Symbols.getSymbol(postfix[i-1].value, 'V').address)
            self.instructionCounter += 1
            if i != len(postfix)-1:
                temp = 'temp'+str(tempCount)
                tempCount += 1
                postfix[i] = token('var', temp)
                self.Output.append(2100+self.Symbols.getSymbol(temp, 'V').address)
                self.instructionCounter += 1
                if i - 3 >= 0:
                    postfix[i-1] = postfix[i-3]
        elif t.value == '/':
            self.Output.append(2000+self.Symbols.getSymbol(postfix[i-2].value, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3200+self.Symbols.getSymbol(postfix[i-1].value, 'V').address)
            self.instructionCounter += 1
            if i != len(postfix)-1:
                temp = 'temp'+str(tempCount)
                tempCount += 1
                postfix[i] = token('var', temp)
                self.Output.append(2100+self.Symbols.getSymbol(temp, 'V').address)
                self.instructionCounter += 1
                if i - 3 >= 0:
                    postfix[i-1] = postfix[i-3]
        elif t.value == '*':
            self.Output.append(2000+self.Symbols.getSymbol(postfix[i-2].value, 'V').address)
            self.instructionCounter += 1
            self.Output.append(3300+self.Symbols.getSymbol(postfix[i-1].value, 'V').address)
            self.instructionCounter += 1
            if i != len(postfix)-1:
                temp = 'temp'+str(tempCount)
                tempCount += 1
                postfix[i] = token('var', temp)
                self.Output.append(2100+self.Symbols.getSymbol(temp, 'V').address)
                self.instructionCounter += 1
                if i - 3 >= 0:
                    postfix[i-1] = postfix[i-3]
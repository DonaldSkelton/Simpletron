from copy import *


class Simpletron():
    def __init__(self):
        self.accumulator=0
        self.instructionCounter=0
        self.instructionRegister=0
        self.operationCode=0
        self.operand=0
        self.memory=[0 for i in range(100)]


    def fetch(self):
        self.instructionRegister=copy(self.memory[self.instructionCounter])
        self.instructionCounter+=1


    def decode(self):
        self.operationCode=self.instructionRegister // 100
        self.operand=self.instructionRegister % 100


    def execute(self):
        def READ(X:int):       #Read a word from the keyboard into X location in memory
            word=''
            while word == '':
                try:
                    word=input('INPUT: ')
                    if not ((len(word) == 4) or ((len(word) == 5) and (word[0] in '+-'))):
                        raise RuntimeError('invalid word')
                    word=int(word)
                except:
                    word=''
                    print('*** Please enter a valid 4 digit word ***')
            self.memory[X]=copy(word)

        def WRITE(X:int):      #Write the word at X location in memory to the screen
            print(self.memory[X])

        def LOAD(X:int):       #Load the word at X location in memory to the accumulator
            self.accumulator=copy(self.memory[X])

        def STORE(X:int):      #Store a word from the accumulator at X location in memory
            self.memory[X]=copy(self.accumulator)

        def ADD(X:int):        #Add the word at X location in memory to the accumulator
            self.accumulator += self.memory[X]

        def SUBTRACT(X:int):   #Subtract the word at X location in memory from the accumulator
            self.accumulator -= self.memory[X]

        def DIVIDE(X:int):     #Divide the word at X location in memory into the accumulator
            if self.memory[X] == 0:
                print('***  ERROR: CANNOT DIVIDE BY ZERO  ***')
                print('*** EXECUTION STOPPED BEFORE HALT! ***')
                self.dump()
                exit(1)
            self.accumulator = self.accumulator // self.memory[X]

        def MULTIPLY(X:int):   #Multiply the accumulator by the word at X location in memory
            self.accumulator = self.accumulator * self.memory[X]

        def BRANCH(X:int):     #Branch to X location in memory
            self.instructionCounter = copy(X)

        def BRANCHNEG(X:int):  #Branch to X location in memory if the accumulator is negative
            if self.accumulator < 0:
                self.instructionCounter = copy(X)

        def BRANCHZERO(X:int): #Branch to X location in memory if the accumulator is zero
            if self.accumulator == 0:
                self.instructionCounter = copy(X)

        def HALT(X:int):       #The program has finished. REG + MEM Dump
            print('\n*** Simpletron exucution terminated ***')
            self.dump()
            exit(0)

        operations={10:READ,
                    11:WRITE,
                    20:LOAD,
                    21:STORE,
                    30:ADD,
                    31:SUBTRACT,
                    32:DIVIDE,
                    33:MULTIPLY,
                    40:BRANCH,
                    41:BRANCHNEG,
                    42:BRANCHZERO,
                    43:HALT}
        
        try:
            operations[self.operationCode](self.operand)
        except SystemExit:
            raise
        except:
            print('***       INVALID OPERATION!       ***')
            print('*** EXECUTION STOPPED BEFORE HALT! ***')
            self.dump()
            exit(1)
    
    
    def dump(self):
        print('\nREGISTERS:')
        print('{0:<23s}{1:0=+5d}'.format('accumulator',self.accumulator))
        print('{0:<23s}{1:0>2d}'.format('instructionCounter',self.instructionCounter))
        print('{0:<23s}{1:0=+5d}'.format('instructionRegister',self.instructionRegister))
        print('{0:<23s}{1:0>2d}'.format('operationCode',self.operationCode))
        print('{0:<23s}{1:0>2d}'.format('operand',self.operand))
        print('\nMEMORY:')
        print('       0     1     2     3     4     5     6     7     8     9')
        for i in range(10):
            row=i*10
            s=('{:>2d}'.format(row))+' '
            for col in range(10):
                s+=('{:0=+5d}'.format(self.memory[row+col])+' ')
            print(s)        


    def load(self):
        for i in range(100):
            word=''
            while word == '':
                try:
                    word=input('{:0>2d}'.format(i)+' ? ')
                    if not ((len(word) == 4) or ((len(word) == 5) and (word[0] in '+-'))
                    or (word == '-99999') or (word == '-99990')):
                        raise RuntimeError('invalid word')
                    int(word)
                except:
                    word=''
                    print('*** Please enter a valid 4 digit word ***')
            
            if word=='-99999':
                break
            if word=='-99990':
                self.loadFile()
                break
            self.memory[i]=int(word)
            if i == 99:
                print('*** MEMORY FULL! ***')
    
    
    def loadFile(self):
        fname=input('Filename to be loaded: ')
        file = open(fname,'r')
        strings=file.readlines()
        for i,string in enumerate(strings):
            self.memory[i]=int(string)
        print('*** Program loaded from file***\n')
    
    
    def run(self):
        while True:
            self.fetch()
            self.decode()
            self.execute()        


def main():
    print('*** Welcom to Simpletron! ***')
    print('\n*** Please enter your program one instruction ***')
    print('*** (or data word) at a time. I will type the ***')
    print('*** location number and a question mark (?).  ***')
    print('*** You then type the word for that location. ***')
    print('*** To load program from file, type sentinel  ***')
    print('*** value -99990. Then specify the filename.  ***')
    print('*** Type the sentinel -99999 to stop entering ***')
    print('*** your program. ***\n')
    simpletron=Simpletron()
    simpletron.load()
    print('\n*** Program loading completed ***')
    print('*** Program execution begins  ***\n')
    simpletron.run()

if __name__=='__main__':
    main()

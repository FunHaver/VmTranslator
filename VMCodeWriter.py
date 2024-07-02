import os, sys, re

class VMCodeWriter:
    def __init__(self, fileName, outFilePath):
        self.outFile = open(outFilePath, 'w', encoding='utf-8')
        self.comparisonNo = 0
        self.__fileName = ""
        self.setFileName(fileName)

    def __del__(self):
        self.outFile.close()
    
    #write with an os-specific line separator :)
    def __asmOut(self, asmString):
        self.outFile.write(asmString)
        self.outFile.write(os.linesep)

    def __writeStaticVariable(self, index):
        return self.__fileName + "." + str(index)
    
    def __assignDRegisterToMemoryMapValue(self, symbol, index):
        self.__asmOut("@" + symbol)
        self.__asmOut("D=M")
        self.__asmOut("@" + str(index))
        self.__asmOut("D=D+A")
        self.__asmOut("A=D")
        self.__asmOut("D=M")
    
    def __pushDRegisterToStack(self):
        # *SP=D
        self.__asmOut("@SP")
        self.__asmOut("A=M")
        self.__asmOut("M=D")
        # SP++
        self.__asmOut("@SP")
        self.__asmOut("M=M+1")

    def __pushSegment(self, segment, index):
        
        if segment == "constant":
            # D=index
            self.__asmOut("@" + str(index))
            self.__asmOut("D=A")
        elif segment == "local":
            # D=*(LCL + index)
            self.__assignDRegisterToMemoryMapValue("LCL", index)
        elif segment == "argument":
            # D=*(ARG + index)
            self.__assignDRegisterToMemoryMapValue("ARG", index)
        elif segment == "this":
            # D=*(THIS + index)
            self.__assignDRegisterToMemoryMapValue("THIS", index)
        elif segment == "that":
            # D=*(THAT + index)
            self.__assignDRegisterToMemoryMapValue("THAT", index)
        elif segment == "pointer":
            self.__asmOut("@" + str(3 + index))
            self.__asmOut("D=M")
        elif segment == "temp":
            self.__asmOut("@" + str(5 + index))
            self.__asmOut("D=M")
        elif segment == "static":
            self.__asmOut("@" + self.__writeStaticVariable(index))
            self.__asmOut("D=M")
        else:
            sys.exit("Unknown memory segment \"" + segment + "\"")
        self.__pushDRegisterToStack()

    # These memory segments are referenced via a pointer in RAM[0..4]. 
    # Those pointers are stored in fixed ram locations
    def __popToMapping(self, segment, index):

        # @R13 = index + @segment
        self.__asmOut("@" + str(index))
        self.__asmOut("D=A")
        self.__asmOut("@" + segment)
        self.__asmOut("D=D+M")
        self.__asmOut("@R13")
        self.__asmOut("M=D")
        # SP--
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")
        # D = *SP
        self.__asmOut("A=M")
        self.__asmOut("D=M")
        # *RAM[(index + segment)] = D
        self.__asmOut("@R13")
        self.__asmOut("A=M")
        self.__asmOut("M=D")

    # These memory segments are stored directly to at a fixed area of the ram
    def __popToFixedAddress(self, segment, index):
        ramAddress = ""
        if segment == "POINTER":
            ramAddress = str(3 + index)
        elif segment == "TEMP":
            ramAddress = str(5 + index)
        
        # SP--
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")
        # D = *SP
        self.__asmOut("A=M")
        self.__asmOut("D=M")
        # RAM[segment + index] = D
        self.__asmOut("@" + ramAddress)
        self.__asmOut("M=D")

    def __popToStatic(self, index):
        # SP--
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")
        # D = *SP
        self.__asmOut("A=M")
        self.__asmOut("D=M")
        # self.__fileName.index = D
        self.__asmOut("@" + self.__writeStaticVariable(index))
        self.__asmOut("M=D")

    #Here we use a "general purpose VM Implementation Register" to store the destination address of the popped value
    def __popSegment(self, segment, index):
        if segment == "local":
            self.__popToMapping("LCL", index)
        elif segment == "argument":
            self.__popToMapping("ARG", index)
        elif segment == "this":
            self.__popToMapping("THIS", index)
        elif segment == "that":
            self.__popToMapping("THAT", index)
        elif segment == "temp":
            self.__popToFixedAddress("TEMP", index)
        elif segment == "pointer":
            self.__popToFixedAddress("POINTER", index)
        elif segment == "static":
            self.__popToStatic(index)
        else: 
            sys.exit("Unknown memory segment \"" + segment + "\"")
            
    def __performUnaryArithmetic(self, command):
        # SP--
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")

        # D = *SP
        self.__asmOut("A=M")

        if command == "not":
            # *SP = !*SP
            self.__asmOut("M=!M")
        elif command == "neg":
            # *SP = !*SP
            self.__asmOut("M=-M")
        else:
            sys.exit("Command \"" + command + "\" not found")

        # SP++
        self.__asmOut("@SP")
        self.__asmOut("M=M+1")
        
    def __isBinaryArithmetic(self, command):
        if command == "add":
            return True
        elif command == "sub":
            return True
        elif command == "eq":
            return True
        elif command == "gt":
            return True
        elif command == "lt":
            return True
        elif command == "and":
            return True
        elif command == "or":
            return True
        else:
            return False
    
    def __performComparisonOperation(self, command):
            # x - y
            self.__asmOut("D=M-D")
            self.__asmOut("@IS_TRUE_" + str(self.comparisonNo))
            if command == "eq":
                self.__asmOut("D;JEQ")
            elif command == "lt":
                self.__asmOut("D;JLT")
            elif command == "gt":
                self.__asmOut("D;JGT")
            else:
                sys.exit("Command \"" + command + "\" not found")
            
            # if the test returned false
            self.__asmOut("D=0")
            self.__asmOut("@DONE_" + str(self.comparisonNo))
            self.__asmOut("0;JMP")

            # if the test returned true
            self.__asmOut("(IS_TRUE_" + str(self.comparisonNo) +")")
            self.__asmOut("D=-1")

            # end of routine for writing true or false to D register
            self.__asmOut("(DONE_" + str(self.comparisonNo) + ")")
        
    # convention is to put "x" into the D register, and reference "y" from the M register
    def __performBinaryArithmetic(self, command):
        # SP--
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")
        # RAM[i] = *SP
        self.__asmOut("A=M")
        self.__asmOut("D=M")
        # SP--
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")

        self.__asmOut("A=M")
        if command == "add":
            # x + y
            self.__asmOut("D=M+D")
        elif command == "sub":
            # x - y
            self.__asmOut("D=M-D")
        elif command == "or":
            # x | y
            self.__asmOut("D=D|M")
        elif command == "and":
            # x & y
            self.__asmOut("D=D&M")
        elif command == "eq" or command == "gt" or command == "lt":
            self.__performComparisonOperation(command)
        else:
            sys.exit("Command \"" + command + "\" not found")

        self.__pushDRegisterToStack()
        
    # Writes to the output file the 
    # assembly code that implements the given
    # arithmetic or logic command
    def writeArithmetic(self, command):
        self.comparisonNo += 1
        vmComment = "// " + command
        self.__asmOut(vmComment)

        if command == "neg" or command == "not":
            self.__performUnaryArithmetic(command)
        elif self.__isBinaryArithmetic(command):
            self.__performBinaryArithmetic(command)
        else:
            print("Artithmetic \"" + command + "\" not yet implemented")

    # Writes to the output file the 
    # assembly code that implements the given
    # push or pop command
    def writePushPop(self, command, segment, index):
        vmComment = "// " + command + " " + segment + " " + str(index)
        self.__asmOut(vmComment)
        
        if command == "push":
            self.__pushSegment(segment, index)
        elif command == "pop":
            self.__popSegment(segment,index)

    def writeLabel(self, command, label):
        vmComment = "// " + command + " " + label
        self.__asmOut(vmComment)
        self.__asmOut("(" + label + ")")

    def writeIf(self, command, label):
        vmComment = "// " + command + " " + label
        self.__asmOut(vmComment) 
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")
        self.__asmOut("A=M")
        self.__asmOut("D=M")
        self.__asmOut("@" + label)
        self.__asmOut("D;JNE")

    def writeGoto(self, command, label):
        vmComment = "// " + command + " " + label
        self.__asmOut(vmComment) 
        self.__asmOut("@" + label)
        self.__asmOut("0;JMP")   

    def writeCall(self, command, functionName, nArgs):
        vmCommand = "// " + command + " " + functionName + " " + nArgs

        self.__asmOut(vmCommand)

        # Push caller return address to stack
        self.__asmOut("@returnAddress")
        self.__asmOut("D=M")
        self.__pushDRegisterToStack()

        # Push caller LCL address to stack
        self.__asmOut("@LCL")
        self.__asmOut("D=M")
        self.__pushDRegisterToStack()

        # Push caller arg address to stack
        self.__asmOut("@ARG")
        self.__asmOut("D=M")
        self.__pushDRegisterToStack()

        # Push caller THIS to stack
        self.__asmOut("@THIS")
        self.__asmOut("D=M")
        self.__pushDRegisterToStack()

        # Push caller THAT to stack
        self.__asmOut("@THAT")
        self.__asmOut("D=M")
        self.__pushDRegisterToStack()

        # Assign callee ARG pointer to first parameter location
        # @ARG = SP-5-nArgs
        self.__asmOut("@SP")
        self.__asmOut("D=M")
        self.__asmOut("@5")
        self.__asmOut("D=D-A")
        self.__asmOut("@" + str(nArgs))
        self.__asmOut("D=D-A")
        self.__asmOut("@ARG")
        self.__asmOut("M=D")

        # Assign callee LCL pointer to current Stack pointer value
        self.__asmOut("@SP")
        self.__asmOut("D=M")
        self.__asmOut("@LCL")
        self.__asmOut("M=D")

        # Go to the function
        self.__asmOut("@" + functionName)
        self.__asmOut("0;JMP")

        # Declare label for returnAddress
        self.__asmOut("(returnAddress)")

    # Sets the label for the function in asm, then initializes LCL for fn, then increments stack to
    # Make sure we don't overwrite anything in LCL

    def writeFunction(self, command, functionName, numLocals):
        vmComment = "// " + command + " " + functionName + " " + str(numLocals)
        self.__asmOut(vmComment)
        # declare function label
        self.__asmOut("(" + functionName + ")")
        # allocate local memory
        for x in range(0,numLocals):
            #Set @LCL[x] = 0, same as pushing 0s to stack
            self.__pushSegment("constant", 0)
            

    def writeReturn(self, command):
        vmComment = "// " + command
        self.__asmOut(vmComment)

        # temp variable to store mem location of end of stack frame
        self.__asmOut("@LCL")
        self.__asmOut("D=M")
        self.__asmOut("@R14")
        self.__asmOut("M=D")

        # temp variable to store return address of fn
        self.__asmOut("@5")
        self.__asmOut("D=A")
        self.__asmOut("@R14")
        self.__asmOut("A=M-D")
        self.__asmOut("D=M")
        self.__asmOut("@R15")
        self.__asmOut("M=D")

        # pop top value from fn stack and move to location arg 0, the top of the stack for the parent fn
        self.__popSegment("argument", 0)

        # move stack pointer back to where the caller of the parent fn expects it to be in memory
        self.__asmOut("@ARG")
        self.__asmOut("D=M+1")
        self.__asmOut("@SP")
        self.__asmOut("M=D")

        # restore named pointer values to caller's (parent fn's) state
        # THAT
        self.__asmOut("@R14")
        self.__asmOut("A=M-1")
        self.__asmOut("D=M")
        self.__asmOut("@THAT")
        self.__asmOut("M=D")

        # THIS
        self.__asmOut("@2")
        self.__asmOut("D=A")
        self.__asmOut("@R14")
        self.__asmOut("A=M-D")
        self.__asmOut("D=M")
        self.__asmOut("@THIS")
        self.__asmOut("M=D")

        # ARG
        self.__asmOut("@3")
        self.__asmOut("D=A")
        self.__asmOut("@R14")
        self.__asmOut("A=M-D")
        self.__asmOut("D=M")
        self.__asmOut("@ARG")
        self.__asmOut("M=D")

        # LCL
        self.__asmOut("@4")
        self.__asmOut("D=A")
        self.__asmOut("@R14")
        self.__asmOut("A=M-D")
        self.__asmOut("D=M")
        self.__asmOut("@LCL")
        self.__asmOut("M=D")

        #Jump back to return address and continue execution from parent fn
        self.__asmOut("@R15")
        self.__asmOut("0;JMP")

    # Informs the codeWriter that the translation
    # of a new VM file has started
    def setFileName(self, name):
        self.__fileName = re.sub('\\.vm$', '', name)


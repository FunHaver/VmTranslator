import os, sys, re

class VMCodeWriter:
    def __init__(self, fileName, outFilePath):
        self.outFile = open(outFilePath, 'w', encoding='utf-8')
        self.instructionNo = 0
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
        # *SP=D
        self.__asmOut("@SP")
        self.__asmOut("A=M")
        self.__asmOut("M=D")
        # SP++
        self.__asmOut("@SP")
        self.__asmOut("M=M+1")

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
            self.__asmOut("@IS_TRUE_" + str(self.instructionNo))
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
            self.__asmOut("@DONE_" + str(self.instructionNo))
            self.__asmOut("0;JMP")

            # if the test returned true
            self.__asmOut("(IS_TRUE_" + str(self.instructionNo) +")")
            self.__asmOut("D=-1")

            # end of routine for writing true or false to D register
            self.__asmOut("(DONE_" + str(self.instructionNo) + ")")
        
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

        # *SP = D
        self.__asmOut("@SP")
        self.__asmOut("A=M")
        self.__asmOut("M=D")
        # SP++
        self.__asmOut("@SP")
        self.__asmOut("M=M+1")
        
    # Writes to the output file the 
    # assembly code that implements the given
    # arithmetic or logic command
    def writeArithmetic(self, command):
        self.instructionNo += 1
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
        self.instructionNo += 1
        vmComment = "// " + command + " " + segment + " " + str(index)
        self.__asmOut(vmComment)
        
        if command == "push":
            self.__pushSegment(segment, index)
        elif command == "pop":
            self.__popSegment(segment,index)

    def writeLabel(self, command, arg):
        self.instructionNo+=1
        vmComment = "// " + command + " " + arg
        self.__asmOut(vmComment)
        self.__asmOut("(" + arg + ")")

    def writeIf(self, command, arg):
        self.instructionNo+=1
        vmComment = "// " + command + " " + arg
        self.__asmOut(vmComment) 
        self.__asmOut("@SP")
        self.__asmOut("M=M-1")
        self.__asmOut("A=M")
        self.__asmOut("D=M")
        self.__asmOut("@" + arg)
        self.__asmOut("D;JNE")

    def writeGoto(self, command, arg):
        self.instructionNo+=1
        vmComment = "// " + command + " " + arg
        self.__asmOut(vmComment) 
        self.__asmOut("@" + arg)
        self.__asmOut("0;JMP")   

    # Informs the codeWriter that the translation
    # of a new VM file has started
    def setFileName(self, name):
        self.__fileName = re.sub('\\.vm$', '', name)


import os, sys
class VMCodeWriter:
    def __init__(self, outFilePath):
        self.outFile = open(outFilePath, 'w', encoding='utf-8')
        self.instructionNo = 0

    def __del__(self):
        self.outFile.close()
    
    #write with an os-specific line separator :)
    def __asmOut(self, asmString):
        self.outFile.write(asmString)
        self.outFile.write(os.linesep)

    def __pushSegment(self, segment, index):
        # D=index
        if segment == "constant":
            self.__asmOut("@" + str(index))
            self.__asmOut("D=A")
        else:
            return
        # *SP=D
        self.__asmOut("@SP")
        self.__asmOut("A=M")
        self.__asmOut("M=D")
        # SP++
        self.__asmOut("@SP")
        self.__asmOut("M=M+1")

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


import os
class VMCodeWriter:
    def __init__(self, outFilePath):
        self.outFile = open(outFilePath, 'w', encoding='utf-8')

    def __del__(self):
        self.outFile.close()
    
    #write with an os-specific line separator :)
    def __asmOut(self, asmString):
        self.outFile.write(asmString)
        self.outFile.write(os.linesep)

    def __push(self, segment, index):
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
    # Writes to the output file the 
    # assembly code that implements the given
    # arithmetic or logic command
    def writeArithmetic(self, command):
        vmComment = "// " + command
        self.__asmOut(vmComment)

        if command == "add":
            # SP--
            self.__asmOut("@SP")
            self.__asmOut("M=M-1")
            # RAM[i] = *SP
            self.__asmOut("A=M")
            self.__asmOut("D=M")
            self.__asmOut("@operand_2")
            self.__asmOut("M=D")
            # SP--
            self.__asmOut("@SP")
            self.__asmOut("M=M-1")
            # add two stack items
            self.__asmOut("A=M")
            self.__asmOut("D=M")
            self.__asmOut("@operand_2")
            self.__asmOut("D=D+M")
            # *SP = D
            self.__asmOut("@SP")
            self.__asmOut("A=M")
            self.__asmOut("M=D")
            # SP++
            self.__asmOut("@SP")
            self.__asmOut("M=M+1")
    
    # Writes to the output file the 
    # assembly code that implements the given
    # push or pop command
    def writePushPop(self, command, segment, index):
        vmComment = "// " + command + " " + segment + " " + str(index)
        self.__asmOut(vmComment)
        
        if command == "push":
            self.__push(segment, index)


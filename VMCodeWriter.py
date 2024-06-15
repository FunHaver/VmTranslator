import os
class VMCodeWriter:
    def __init__(self, outFile):
        self.outFile = outFile

    # Increment value at @SP, the stack pointer, to point to the next
    # available spot on the stack
    def __incrementStackPointer(self):
        self.outFile.write("@SP")
        self.outFile.write(os.linesep)
        self.outFile.write("M=M+1")
        self.outFile.write(os.linesep)

    # Store stack pointer mem location in address register
    # Making the new address the memory location that is the value stored at @SP
    def __setAddressToStackPointer(self):
        self.outFile.write("@SP")
        self.outFile.write(os.linesep)
        self.outFile.write("A=M")
        self.outFile.write(os.linesep)

    def __pushConstant(self, index):
        
        #load constant into D register
        self.outFile.write("@" + str(index))
        self.outFile.write(os.linesep)
        self.outFile.write("D=A")
        self.outFile.write(os.linesep)
        
        self.__setAddressToStackPointer()

        #Store constant at stack location
        self.outFile.write("M=D")
        self.outFile.write(os.linesep)

    def __writePush(self, segment, index):
        if segment == "constant":
            self.__pushConstant(index)
        else:
            self.outFile.write(segment + " not yet implemented")
            self.outFile.write(os.linesep)

        self.__incrementStackPointer()

    # Writes to the output file the 
    # assembly code that implements the given
    # arithmetic or logic command
    def writeArithmetic(self, command):
        vmComment = "// " + command
        self.outFile.write(vmComment)
        self.outFile.write(os.linesep)

    
    # Writes to the output file the 
    # assembly code that implements the given
    # push or pop command
    def writePushPop(self, command, segment, index):
        vmComment = "// " + command + " " + segment + " " + str(index)
        self.outFile.write(vmComment)
        self.outFile.write(os.linesep)

        if command == "push":
            self.__writePush(segment, index)
        elif command == "pop":
            self.outFile.write(command + " not yet implemented")
            self.outFile.write(os.linesep)


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

    # Writes to the output file the 
    # assembly code that implements the given
    # arithmetic or logic command
    def writeArithmetic(self, command):
        vmComment = "// " + command
        self.__asmOut(vmComment)

    
    # Writes to the output file the 
    # assembly code that implements the given
    # push or pop command
    def writePushPop(self, command, segment, index):
        vmComment = "// " + command + " " + segment + " " + str(index)
        self.__asmOut(vmComment)


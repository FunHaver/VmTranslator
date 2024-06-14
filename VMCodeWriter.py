class VMCodeWriter:
    def __init__(self, writeFile):
        self.writeFile = writeFile

    # Writes to the output file the 
    # assembly code that implements the given
    # arithmetic or logic command
    def writeArithmetic(self, command):
        return None
    
    # Writes to the output file the 
    # assembly code that implements the given
    # push or pop command
    def writePushPop(self, command, segment, index):
        return None
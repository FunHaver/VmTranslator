import sys, os, re
from VMParser import VMParser
from VMCodeWriter import VMCodeWriter
def main():

    # Initialize environment
    if len(sys.argv) < 2:
        sys.exit("ERROR: No VM file specified")
    workingDirectory = os.getcwd()
    filePath = sys.argv[1]
    pathList = filePath.split("/")
    fileName = pathList[len(pathList) - 1]
    vmPath = os.path.join(workingDirectory, filePath)
    outFilePath = workingDirectory + "/" + re.sub(r'\.vm$',".asm", fileName)
    
    parser = VMParser(vmPath)
    codeWriter = VMCodeWriter(fileName,outFilePath)

    while parser.hasMoreLines():
        parser.advance()
        if parser.commandType() == "C_PUSH" or parser.commandType() == "C_POP":
            codeWriter.writePushPop(parser.currentCommand(), parser.arg1(), parser.arg2())
        elif parser.commandType() == "C_ARITHMETIC":
            codeWriter.writeArithmetic(parser.currentCommand())
        else:
            print("Implement command: " + parser.currentCommand())

    del parser
    del codeWriter


main()
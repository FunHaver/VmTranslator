import sys, os, re
from VMParser import VMParser
from VMCodeWriter import VMCodeWriter
def main():

    # Initialize environment
    if len(sys.argv) < 2:
        sys.exit("ERROR: No VM file specified")
    workingDirectory = os.getcwd()
    filePath = sys.argv[1]
    vmFiles = []
    outFilePath = None
    if os.path.isdir(filePath):
        dirContents = os.listdir(filePath)
        for file in dirContents:
            if file.endswith(".vm"):
                vmFiles.append(os.path.join(workingDirectory, filePath, file))
        vmDirParts = filePath.split(os.path.sep)

        if len(vmDirParts[len(vmDirParts) - 1]) == 0:
            vmDirParts.pop()
        outFileName = vmDirParts[len(vmDirParts) - 1]
        outFilePath = os.path.join(workingDirectory, outFileName + ".asm")
    else:
        vmFiles.append(os.path.join(workingDirectory, filePath))
        outFileName = re.sub(r'\.vm$', '', os.path.split(filePath)[1])
        outFilePath = os.path.join(workingDirectory, outFileName + ".asm")
        
    outFileName = os.path.split(outFilePath)[1]
    codeWriter = VMCodeWriter(outFilePath)

    for file in vmFiles:
        parser = VMParser(file)
        codeWriter.setFileName(os.path.split(file)[1])
        while parser.hasMoreLines():
            parser.advance()
            if parser.commandType() == "C_PUSH" or parser.commandType() == "C_POP":
                codeWriter.writePushPop(parser.currentCommand(), parser.arg1(), parser.arg2())
            elif parser.commandType() == "C_ARITHMETIC":
                codeWriter.writeArithmetic(parser.currentCommand())
            elif parser.commandType() == "C_LABEL":
                codeWriter.writeLabel(parser.currentCommand(), parser.arg1())
            elif parser.commandType() == "C_IF":
                codeWriter.writeIf(parser.currentCommand(), parser.arg1())
            elif parser.commandType() == "C_GOTO":
                codeWriter.writeGoto(parser.currentCommand(), parser.arg1())
            elif parser.commandType() == "C_FUNCTION":
                codeWriter.writeFunction(parser.currentCommand(), parser.arg1(), parser.arg2())
            elif parser.commandType() == "C_RETURN":
                codeWriter.writeReturn(parser.currentCommand())
            elif parser.commandType() == "C_CALL":
                codeWriter.writeCall(parser.currentCommand(), parser.arg1(), parser.arg2())
            else:
                print("Implement command: " + parser.currentCommand())

        del parser
    del codeWriter


main()
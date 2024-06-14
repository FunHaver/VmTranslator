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


    inFile = open(vmPath, 'r', encoding="utf-8")
    outFile = open(outFilePath, 'w', encoding='utf-8')
    
    parser = VMParser(inFile)
    codeWriter = VMCodeWriter(outFile)

    while parser.hasMoreLines():
        parser.advance()
        
    inFile.close()
    outFile.close()


main()
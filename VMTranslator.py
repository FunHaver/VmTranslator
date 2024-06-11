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
    parser = VMParser()
    codeWriter = VMCodeWriter()

    inFile = open(vmPath, 'r', encoding="utf-8")
    outFile = open(outFilePath, 'w', encoding='utf-8')
    for line in inFile:
        #parse
        #covert to asm
        #write line out
        outFile.write(line)
    
    inFile.close()
    outFile.close()


main()
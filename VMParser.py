import sys
class VMParser:

    def __init__(self, inFilePath):
        self.inFile = open(inFilePath, 'r', encoding='utf-8')
        self.__currentCommand = ""
        self.__commandType = "UNKNOWN"

    def __del__(self):
        self.inFile.close()
    
    def __isArithmeticCommand(self, command):
        if command == "add":
            return True
        elif command == "sub":
            return True
        elif command == "neg":
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
        elif command == "not":
            return True
        else:
            return False
    
    def __classifyCommand(self, command):
        
        if self.__isArithmeticCommand(command):
            return "C_ARITHMETIC"
        elif command == "pop":
            return "C_POP"
        elif command == "push":
            return "C_PUSH"
        elif command == "label":
            return "C_LABEL"
        elif command == "if-goto":
            return "C_IF"
        elif command == "goto":
            return "C_GOTO"
        elif command == "function":
            return "C_FUNCTION"
        elif command == "return":
            return "C_RETURN"
        elif command == "call":
            return "C_CALL"
        else: 
            return "UNKNOWN"
    
    def __seekNextCommand(self, file):
        line = file.readline().rstrip()
        stripped = "".join(line.split())
        if len(stripped) == 0:
            return self.__seekNextCommand(file)
        elif stripped[0] == "/" and stripped[1] == "/":
            return self.__seekNextCommand(file)   
        else:
            return line
            
    # Any more lines in the input
    def hasMoreLines(self):
        currentPos = self.inFile.tell()
        self.inFile.seek(currentPos + 1)
        nextLine = self.inFile.readline()
        self.inFile.seek(currentPos)
        return nextLine != ""

    # Reads next command from input and makes it the
    # current command
    def advance(self):
        vmInstruction = self.__seekNextCommand(self.inFile)
        commandList = vmInstruction.split()
        self.__currentCommand = commandList[0]
        self.__commandType = self.__classifyCommand(self.currentCommand())
        if self.commandType() == "UNKNOWN":
            sys.exit("Unknown command: \"" + vmInstruction + "\"")
        elif self.commandType() == "C_PUSH" or self.commandType() == "C_POP":
            self.__arg1 = commandList[1]
            self.__arg2 = int(commandList[2])
        elif self.commandType() == "C_ARITHMETIC":
            return
        else:
            self.__arg1 = commandList[1]
    
    # Returns the type of the current command (C_FOO)
    def commandType(self):
        return self.__commandType
    
    # Returns the current command in string form
    def currentCommand(self):
        return self.__currentCommand
    
    # Returns the first part of the current command
    # Should not be called if the command type is C_RETURN
    def arg1(self):

        return self.__arg1

    # Returns second part of the command, should only be called if
    # command is of type C_PUSH, C_POP, C_FUNCTION, C_CALL
    def arg2(self):
        return self.__arg2;
    
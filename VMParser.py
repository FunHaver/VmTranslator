class VMParser:

    def __init__(self):
        print("Initialized Parser")

    # Any more lines in the input
    def hasMoreLines(self):
        return False;

    # Reads next command from input and makes it the
    # current command
    def advance(self):
        return None
    
    # Returns the type of the current command (C_FOO)
    def commandType(self):
        return None
    
    # Returns the first part of the current command
    # Should not be called if the command type is C_RETURN
    def arg1(self):
        return None

    # Returns second part of the command, should only be called if
    # command is of type C_PUSH, C_POP, C_FUNCTION, C_CALL
    def arg2(self):
        return None
    
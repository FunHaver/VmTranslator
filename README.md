# VM Translator
A Python implementation of the Virtual Machine Translator described in NAND2TETRIS Part 2, Units 1 and 2. 
This program read files containing the VM Bytecode specified in Part 2 of the NAND2TETRIS course and outputs a single HACK assembly file. The HACK assembly language is specified in NAND2TETRIS Part 1, Unit 4.

## Usage
**System Requirements**
 * Python 3.x
 * git

To use this translator, first you must have a file or files written in the VM Bytecode specified in the nand2tetris book.

Some example files are provided in the test_vm_files directory.

First, clone this repository
```bash
git clone https://github.com/FunHaver/VMTranslator
```

Then, execute the VMTranslator.py file found in the repository's root directory. This program takes one argument, either:
1. The location of the VM file to be translated.
2. The location of the directory containing vm files to be translated. (Note: this program does not support sub-directories)

Example execution
```bash
cd VmTranslator
python3 VMTranslator.py test_vm_files/FunctionCalls/FibonacciElement
```

The resulting .asm file will be written to your current working directory.

The result of the example command will place a .asm file in the VMTranslator directory.

## Running the .asm file
Now that you are in posession of a HACK assembly file, it can be tested via the CPU emulator tool, which will assemble the file, provided by the NAND2TETRIS course located here: https://nand2tetris.github.io/web-ide/cpu. 

Or it can be fed into a HACK assembler [like this one](https://github.com/FunHaver/HackAssembler) and then you may use the aformentioned CPU emulator tool to execute the binary. Both options provide the same result.
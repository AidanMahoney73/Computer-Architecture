"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010

CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.eflag = False
        self.gflag = False
        self.lflag = False

    def load(self):
        """Load a program into memory."""

        address = 0

        file = sys.argv[1]
        if file:
            with open(file) as f:
                for line in f:
                    line = line.split('#')
                    # print(line)

                    if line[0] == "":
                        continue

                    self.ram[address] = int(line[0], 2)
                    # print(self.ram[0:address+1])
                    address += 1

        else:
            print("you done messed up AAidan")
            sys.exit(0)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        while self.running:

            command = self.ram[self.pc]

            if command == HLT:
                # print(f"Next task is HLT ({self.ram[self.pc]})")
                self.running = False
                sys.exit(1)

            elif command == LDI:
                # print(f"Next task is LDI ({self.ram[self.pc]})")
                # print(f"Put value {self.ram[self.pc+2]} into reg{self.ram[self.pc+1]}")
                self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
                self.pc += 3

            elif command == PRN:
                # print(f"Next task is PRN ({self.ram[self.pc]})")
                print(self.reg[self.ram[self.pc+1]])
                self.pc += 2

            elif command == CMP:
                a = self.reg[self.ram[self.pc+1]]
                b = self.reg[self.ram[self.pc+2]]
                if a > b:
                    self.gflag = True
                elif a < b:
                    self.lflag = True
                else:
                    self.eflag = True
                self.pc += 3

            elif command == JEQ:
                if self.eflag == True:
                    self.pc = self.reg[self.ram[self.pc+1]]
                else:
                    self.pc += 2

            elif command == JNE:
                if self.eflag == False:
                    self.pc = self.reg[self.ram[self.pc+1]]
                else:
                    self.pc += 2

            elif command == JMP:
                self.pc = self.reg[self.ram[self.pc+1]]

            else:
                print(f"That functionality has Not been incorporated ({command})!")
                # print(f"Next task is {self.ram[self.pc]}")
                sys.exit(1)

            # self.pc += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

import sys
import binascii

# data = open(sys.argv[1], "r").read()

minimal1 = "6060604052600a8060106000396000f360606040526008565b00"
minimal2 = "606060405261010c806100126000396000f360606040526000357c0100000000000000000000000000000000000000000000000000000000900480636d4ce63c1461003957610037565b005b61004660048050506100b4565b60405180806020018281038252838181518152602001915080519060200190808383829060006004602084601f0104600f02600301f150905090810190601f1680156100a65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6020604051908101604052806000815260200150604060405190810160405280600b81526020017f48656c6c6f20576f726c640000000000000000000000000000000000000000008152602001509050610109565b9056"
data = minimal1

binary = binascii.unhexlify(data)


class Opcode:

    def __init__(self, value, mnemonic, adds=0, deletes=0, codeargs=0,
                 i=""):
        """ defines an opcode.
            value - the opcode value, e.g. 0x00
            mnemonic - opcode mnemonic, e.g. STOP
            adds - number of bytes added to stack
            deletes - number of bytes removed from stack
            codeargs - number of subsequence bytes read from code
            i - additional info
        """
        self.value = value
        self.mnemonic = mnemonic
        self.adds = adds
        self.deletes = deletes
        self.codeargs = codeargs
        self.i = i

    def __call__(self, pointer, program):
        """
            handle opcode from programcode, returns additional adjustment
        """
        args = " ".join(hex(program[pointer + i])
                        for i in range(self.codeargs))
        out = self.mnemonic
        if args:
            out += " " + args

        if self.i:
            out = out.ljust(40, " ") + "# " + self.i
        print(out)
        return self.codeargs


class VM:
    opcodes = [
        Opcode(0x00, "STOP", i="Halts execution"),
        Opcode(0x39, "CODECOPY", deletes=3,
               i="Copy code running in current environment to memory"),
        Opcode(0x52, "MSTORE", deletes=2, i="Save word to memory"),
        Opcode(0x56, "JUMP", deletes=1, i="Alters program counter"),
        Opcode(0x5b, "JUMPDEST", i="Mark a valid destination for jumps"),
        Opcode(0x60, "PUSH1", adds=1, codeargs=1,
               i="Place 1 byte item on stack"),
        Opcode(0x80, "DUP1", deletes=1, adds=2, i="Duplicate 1st stack item"),
        Opcode(0x81, "DUP2", deletes=1, adds=2, i="Duplicate 2nd stack item"),
        Opcode(0xf3, "RETURN", deletes=2,
               i="Halt execution returning output data")


    ]

    def __init__(self):
        self.map = {o.value: o for o in self.opcodes}

    def decompile(self, program):
        pointer = 0
        while True:
            try:
                code = program[pointer]
            except IndexError:
                break

            pointer += 1
            try:
                pointer += self.map[code](pointer, program)
            except KeyError:
                print("UNKNOWN", hex(code))

VM().decompile(binary)

    # if code == Opcode.STOP:
    #     print("STOP")
    # elif code == Opcode.CODECOPY:
    #     print("CODECOPY")
    # elif code == Opcode.PUSH1:
    #     print("PUSH1", hex(binary[pointer]))
    #     pointer += 1
    # elif code == Opcode.MSTORE:
    #     arg1 = binary[pointer]
    #     arg2 = binary[pointer + 1]
    #     print("MSTORE", hex(arg1), hex(arg2))
    #     pointer += 2
    # elif code == Opcode.JUMP:
    #     print("JUMP")
    # elif code == Opcode.JUMPDEST:
    #     print("JUMPDEST")
    # elif code == Opcode.DUP1:
    #     arg1 = binary[pointer]
    #     arg2 = binary[pointer + 1]
    #     print("DUP1", hex(arg1), hex(arg2))
    #     pointer += 2
    # elif code == Opcode.RETURN:
    #     print("RETURN")
    # else:
    #     print("UNKNOWN", hex(code))

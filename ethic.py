import sys
import binascii


class OpDef:

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
            Create opcode instance from program and definition
        """
        return Opcode(self,
                      pointer,
                      program[pointer + 1:pointer + 1 + self.codeargs])


class Opcode:

    def __init__(self, definition, pointer, args):
        self.pointer = pointer
        self.definition = definition
        self.args = args

    def __str__(self):
        out = self.definition.mnemonic
        if self.args:
            out += " " + " ".join(hex(a) for a in self.args)

        if self.definition.i:
            out = out.ljust(40, " ") + "# " + self.definition.i
        return out


class Decompiler:
    opcodes = [
        OpDef(0x00, "STOP", i="Halts execution"),
        OpDef(0x01, "ADD", adds=1, deletes=2, i="Addition operation"),
        OpDef(0x02, "MUL", adds=1, deletes=2, i="Multiplication operation"),
        OpDef(0x03, "SUB", adds=1, deletes=2, i="Subtraction operation"),
        OpDef(0x04, "DIV", adds=1, deletes=2, i="Integer division operation"),
        OpDef(0x05, "SDIV", adds=1, deletes=2,
              i="Signed integer division operation (truncated)"),
        OpDef(0x06, "MOD", adds=1, deletes=2, i="Modulo remainder operation"),
        OpDef(0x07, "SMOD", adds=1, deletes=2,
              i="Signed modulo remainder operation"),
        OpDef(0x08, "ADDMOD", adds=1, deletes=3,
              i="Modulo addition operation"),
        OpDef(0x09, "MULMOD", adds=1, deletes=3,
              i="Modulo multiplication oepration"),
        OpDef(0x0a, "EXP", adds=1, deletes=2, i="Exponential operation"),
        OpDef(0x0b, "SIGNEXTEND", adds=1, deletes=2,
              i="Extended length of two's complement signed integer"),

        OpDef(0x10, "LT", adds=1, deletes=2, i="Less-than comparison"),
        OpDef(0x11, "GT", adds=1, deletes=2, i="Greater-than comparison"),
        OpDef(0x12, "SLT", adds=1, deletes=2, i="Signed less-than comparison"),
        OpDef(0x13, "SGT", adds=1, deletes=2,
              i="Signed greater-than comparison"),
        OpDef(0x14, "EQ", adds=1, deletes=2, i="Equality comparison"),
        OpDef(0x15, "ISZERO", adds=1, deletes=1, i="Simple not operator"),
        OpDef(0x16, "AND", adds=1, deletes=2, i="Bitwise AND operation"),
        OpDef(0x17, "OR", adds=1, deletes=2, i="Bitwise OR operation"),
        OpDef(0x18, "XOR", adds=1, deletes=2, i="Bitwise XOR operation"),
        OpDef(0x19, "NOT", adds=1, deletes=1, i="Bitwise NOT operation"),
        OpDef(0x1a, "BYTE", adds=1, deletes=2,
              i="Retrieve single byte from word"),

        OpDef(0x20, "SHA3", adds=1, deletes=2, i="Compute Keccak-256 hash"),

        OpDef(0x35, "CALLDATALOAD", adds=1, deletes=1,
              i="Get input data of current environment"),
        OpDef(0x39, "CODECOPY", deletes=3,
              i="Copy code running in current environment to memory"),

        OpDef(0x50, "POP", deletes=1, i="Remove item from stack"),
        OpDef(0x51, "MLOAD", adds=1, deletes=1, i="Load word from memory"),
        OpDef(0x52, "MSTORE", deletes=2, i="Save word to memory"),
        OpDef(0x56, "JUMP", deletes=1, i="Alter the program counter"),
        OpDef(0x56, "JUMPI", deletes=2,
              i="Conditionally alter the program counter"),
        OpDef(0x5b, "JUMPDEST", i="Mark a valid destination for jumps"),
        OpDef(0x60, "PUSH1", adds=1, codeargs=1,
              i="Place 1 byte item on stack"),
    ] + [
        OpDef(0x60 + i, "PUSH{0}".format(i + 1), adds=1, codeargs=i + 1,
              i="Place {0} byte item on stack".format(i))
        for i in range(32)
    ] + [
        OpDef(0x80 + i, "DUP{0}".format(i), deletes=1 + i, adds=2 + i,
              i="Duplicate {0}st/nd/th stack item".format(i))
        for i in range(16)
    ] + [
        OpDef(0x90 + i, "SWAP{0}".format(i + 1), adds=1,
              i="Exchange 1st and {0}th/nd stack items".format(i + 2))
        for i in range(16)
    ] + [
        OpDef(0xf3, "RETURN", deletes=2,
              i="Halt execution returning output data")

    ]

    def __init__(self):
        self.map = {o.value: o for o in self.opcodes}

    def decompile(self, program):
        pointer = 0
        decompiled = []

        while True:
            try:
                code = program[pointer]
            except IndexError:
                break

            opcode = self.map.get(code)
            if not opcode:
                opcode = OpDef(code, "UNKNOWN {0:x}".format(code))
            res = opcode(pointer, program)
            decompiled.append(res)
            pointer += (1 + res.definition.codeargs)

        for opcode in decompiled:
            print(opcode)

minimal1 = "6060604052600a8060106000396000f360606040526008565b00"
minimal2 = "606060405261010c806100126000396000f360606040526000357c0100000000000000000000000000000000000000000000000000000000900480636d4ce63c1461003957610037565b005b61004660048050506100b4565b60405180806020018281038252838181518152602001915080519060200190808383829060006004602084601f0104600f02600301f150905090810190601f1680156100a65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6020604051908101604052806000815260200150604060405190810160405280600b81526020017f48656c6c6f20576f726c640000000000000000000000000000000000000000008152602001509050610109565b9056"
data = minimal2

binary = binascii.unhexlify(data)

Decompiler().decompile(binary)

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
        OpDef(0x39, "CODECOPY", deletes=3,
              i="Copy code running in current environment to memory"),
        OpDef(0x52, "MSTORE", deletes=2, i="Save word to memory"),
        OpDef(0x56, "JUMP", deletes=1, i="Alters program counter"),
        OpDef(0x5b, "JUMPDEST", i="Mark a valid destination for jumps"),
        OpDef(0x60, "PUSH1", adds=1, codeargs=1,
              i="Place 1 byte item on stack"),
        OpDef(0x80, "DUP1", deletes=1, adds=2,
              i="Duplicate 1st stack item"),
        OpDef(0x81, "DUP2", deletes=1, adds=2,
              i="Duplicate 2nd stack item"),
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

            try:
                res = self.map[code](pointer, program)
            except KeyError:
                res = OpDef(code, "UNKNOWN")
            decompiled.append(res)
            pointer += (1 + res.definition.codeargs)

        for opcode in decompiled:
            print(opcode)

minimal1 = "6060604052600a8060106000396000f360606040526008565b00"
minimal2 = "606060405261010c806100126000396000f360606040526000357c0100000000000000000000000000000000000000000000000000000000900480636d4ce63c1461003957610037565b005b61004660048050506100b4565b60405180806020018281038252838181518152602001915080519060200190808383829060006004602084601f0104600f02600301f150905090810190601f1680156100a65780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6020604051908101604052806000815260200150604060405190810160405280600b81526020017f48656c6c6f20576f726c640000000000000000000000000000000000000000008152602001509050610109565b9056"
data = minimal2

binary = binascii.unhexlify(data)

Decompiler().decompile(binary)

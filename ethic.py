import sys
import binascii

# data = open(sys.argv[1], "r").read()

minimal1 = "6060604052600a8060106000396000f360606040526008565b00"
data = minimal1

binary = binascii.unhexlify(data)

class Opcode:
    STOP = 0x00
    CODECOPY = 0x39
    MSTORE = 0x52
    JUMP = 0x56
    JUMPDEST = 0x5b
    PUSH1 = 0x60
    DUP1 = 0x80
    DUP2 = 0x81  # .. and so forth up to 0x8f / DUP16

    RETURN = 0xf3

pointer = 0
while True:
    try:
        code = binary[pointer]
    except IndexError:
        break

    pointer += 1
    if code == Opcode.STOP:
        print("STOP")
    elif code == Opcode.CODECOPY:
        print("CODECOPY")
    elif code == Opcode.PUSH1:
        print("PUSH1", hex(binary[pointer]))
        pointer += 1
    elif code == Opcode.MSTORE:
        arg1 = binary[pointer]
        arg2 = binary[pointer+1]
        print("MSTORE", hex(arg1), hex(arg2))
        pointer += 2
    elif code == Opcode.JUMP:
        print("JUMP")
    elif code == Opcode.JUMPDEST:
        print("JUMPDEST")
    elif code == Opcode.DUP1:
        arg1 = binary[pointer]
        arg2 = binary[pointer+1]
        print("DUP1", hex(arg1), hex(arg2))
        pointer += 2
    elif code == Opcode.RETURN:
        print("RETURN")
    else:
        print("UNKNOWN", hex(code))

# Ethereum Inverse Compiler (ethic)

Ethic is a feeble attempt at building that (somewhat) decompiles ethereum
code.

Don't expect too much at this point, it currently even fails at properly
decoding all opcodes and it may never produce more than hints and pseudo
code. But any help / automation that can help with analyzing Ethereum contracts
is useful.

## Installing and using

Ethic is being written using Python3.4. Python2 will probably not work without
modifications.

Simply invoke

    ./ethic.py <codefile>

where *codefile* contains hex-ascii code, e.g.

    6060604052600a8060106000396000f360606040526008565b00

while would produce

    0     PUSH1 0x60                        # Place 1 byte item on stack
    2     PUSH1 0x40                        # Place 1 byte item on stack
    4     MSTORE                            # Save word to memory
    5     PUSH1 0xa                         # Place 1 byte item on stack
    7     DUP1                              # Duplicate 1st/nd/th stack item
    8     PUSH1 0x10                        # Place 1 byte item on stack
    10    PUSH1 0x0                         # Place 1 byte item on stack
    12    CODECOPY                          # Copy code running in current environment to memory
    13    PUSH1 0x0                         # Place 1 byte item on stack
    15    RETURN                            # Halt execution returning output data
    16    PUSH1 0x60                        # Place 1 byte item on stack
    18    PUSH1 0x40                        # Place 1 byte item on stack
    20    MSTORE                            # Save word to memory
    21    PUSH1 0x8                         # Place 1 byte item on stack
    23    JUMP                              # Alter the program counter
    24    JUMPDEST                          # Mark a valid destination for jumps
    25    STOP                              # Halts execution

## License

See LICENSE

## Credits

Ethic was written by Ivo van der Wijk

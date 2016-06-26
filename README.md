# Etherum Inverse Compiler (ethic)

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


## License

See LICENSE

## Credits

Ethic was written by Ivo van der Wijk

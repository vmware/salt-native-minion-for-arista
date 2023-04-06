# Salt Project Native Minions for Arista Change Log

## Support for Salt 3005.1

BACKWARDS COMPATIBILITY:
* Ensure previous functionality is maintained where possible

ENHANCEMENTS:
* Support for FastCLI on Arista
* Support for cacpirca on 64-bit

BUG FIXES:
* Fixes as per Salt 3005.1
* Salt 3005.1 requirements altered for zeromq.txt to only allow for later version of pyzmq

TESTS:
* CI/CD pipeline tests of 32-bit and 64-bit build product

RELEASE:
* Supports Python 3.9.14 internally on 64-bit
* Supports Python 3.7/14 internally on 32-bit (Py 3.9 had issues on 32-bit)

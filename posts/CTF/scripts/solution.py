#!/usr/bin/env python3

def zor(x, y):
	for i in range(1, 300):
		if ((i >> x) ^ i) == y:

			return i
			
def decode(hexx):
	hhex = []
	for i in range(1, len(hexx)//2 + 1):
		hhex.append(int(hexx[(2*i-2):(2*i)],16))


	v13 = [i for i in hhex]

	v14 = len(v13)
	for i in range(v14):

		for j in range(3,0,-1):
			v13[i] = zor(j, v13[i])
		if  i > 0 :
			
			v1 = hhex[i - 1]
			v2 = v13[i]
			v13[i] = v2 ^ v1
				

	#print(''.join([chr(i) for i in v13]))
	
	flag=''
	for i in range(len(v13)):
		if i & 1 == 0:
			flag += chr(v13[i] - 3)
		else:
			if v13[i] < 90:
				v =(v13[i] + 3) % 90 
				v += 64 if v < 65 else 0
				flag += chr(v)
			else:
				v =(v13[i] + 3) % 122
				v += 96 if v < 96 else 0
				flag += chr(v)
	return flag[::-1]

with open('flag.enc') as f:
	data = f.read()

print(data)
print((decoddd('423777044c206f02452e')+decoddd('502f6c0a4737771b463c6f175a2070'))[4:])

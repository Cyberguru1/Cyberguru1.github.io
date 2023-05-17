#!/usr/bin/env python3

from Crypto.Cipher import AES
values=[238,236,133,123,132,215,41,111,93,8,227,45,179,170,235,139,150,187,160,231,187,46,155,206,207,143,107,226,131,54,202,248]

key = bytearray(values)
with open('SaveFile.sav', 'rb') as f:
	cipher = f.read()
	
iv = cipher[:16]
cipher = cipher[16:]
xcipher = AES.new(key, AES.MODE_CBC, iv)
mess = xcipher.decrypt(cipher)
print(mess)

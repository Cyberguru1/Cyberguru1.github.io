#!/usr/bin/python 

# script for extracting header id and creating unique links for eahc posts
import re
import requests
import sys

url = sys.argv[1]
contents = requests.get(url).text

pattern = r'<h1 id="([^"]+)"'

match = re.findall(pattern, contents)
if match:
    id_content = match

    for i in id_content:
        print(f"- [{i}]({url}#{i})")
    print("\n\n")
    for i in id_content:
        print(f"{url}#{i}")


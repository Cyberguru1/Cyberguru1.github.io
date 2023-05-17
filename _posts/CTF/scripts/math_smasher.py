#!/usr/bin/python3
from sympy import *
import urllib.request as urllib2
import urllib.parse as urllib
from PIL import Image
import PIL.ImageOps
import io
import sympy
from pydantic import env_settings
from pytesseract import pytesseract
import re

def on_blacklist(text):
    if len(text) != 4:
        return True
    blacklisted = ["I", "O", "Z", "Q", "G", "T" "l", "C", "X", "V", "B", "U"]
    for character in blacklisted:
        if character in text:
            return True
    matcher = re.match("[a-zA-Z0-9]+", text)
    if matcher is None or len(matcher.group()) != 4:
        return True
    return False



max = 0
port = "32632" # change port number from challenge website when u start a new container
lastScore = 0
booll = False
prev  = urllib.urlencode({'eqn_ans': 'NULL'}).encode("utf-8")

while True:
    
    fdd = urllib2.urlopen("http://challenge.nahamcon.com:"+port)
    fdd = fdd.read().decode('utf-8')
    data = re.search("<p class=\"count\">(.*?)</p>", fdd)
    if data is not None:
        data = data.group(1)
        print("score : ",data)
    f = urllib2.urlopen("http://challenge.nahamcon.com:" +port+"/static/eqn.png")
    image_file = io.BytesIO(f.read())
    im = Image.open(image_file)
    im = PIL.ImageOps.invert(im)

    im.save('lll.png')



    custom_config = r"--psm 7  --user-patterns patterns.txt "

    text = pytesseract.image_to_string(im, config=custom_config)
    text = text.replace(" ","")
    text = text.replace("T", "7")
    text = text.replace("A", "4")
    print("question: ", text)
    if '°' in text:
        text = '*'.join(text.split('°'))
    # if  on_blacklist(text):
    #      urllib2.urlopen("http://challenge.nahamcon.com:"+port+"/",prev)
  
    text =  eval(text)
    try:
        if int(str(text).split('.')[1].lstrip('0')) != 0:
            text = text
    except:
        text = int(text)

    text = f"{text:.4f}".rstrip('0') if  isinstance(text, float) else text
    print("answer: ", text)
    params = {"eqn_ans": text}

    encoded_params = urllib.urlencode(params).encode("utf-8")

    prev = encoded_params

    urllib2.urlopen("http://challenge.nahamcon.com:"+port+"/",encoded_params)

from PIL import Image, ImageOps
import pytesseract
import requests
import io

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
URL = "http://challenge.nahamcon.com:32522"
IMAGE = "/static/eqn.png"
URL_IMAGE = URL + "/" + IMAGE
FLAG_URL= URL + "/static/flag.png"

def readImageFromUrl():
    data = requests.get(url=URL_IMAGE)
    return data.content

def downloadFlag():
    data = requests.get(url=FLAG_URL)
    if data.status_code != 404:
        with open("flag.png","wb") as f:
            f.write(data.content)
    

def sendResult(result):
    data ={"eqn_ans":str(result)}
    response=  requests.post(url=URL,data=data)
    array = response.content.decode().split('<p class="count">')[-1]
    count, others = array.split("</p>")
    print("Count: " + str(count))

    #verify if flag pop
    if "display: none;" not in others:
        downloadFlag()

cpt= 0
while True:
    cpt+=1
    print("\nCPT: "+ str(cpt))
    data = readImageFromUrl()
    
    img1 =Image.open(io.BytesIO(data))
    # invert color for  a better contrast
    img1 = ImageOps.invert(img1)
    
    # crop to focus on the calcule
    img1=img1.crop((0,100,img1.width,(img1.height/1.5)))
    
    # img1.save(f"./pics/img_{cpt}.png")

    text = pytesseract.image_to_string(img1).strip()
    
    print(text)
    
    if text != "":
        text = text.replace("°","*").replace(" ","")
        result = round(eval(text),4)
        
        print(result)
        sendResult(result)

#!/usr/bin/env python3

import os
import email
import email.parser
from email.parser import HeaderParser
import base64
import smtplib
import requests
import json

#yellow color / Term display
def yellowtxt(yellow):
    print(f"\033[93m {yellow}\033[00m")

yellowtxt("""
 ___ __  __ _      _____         _ ___
| __|  \/  | |    |_   _|__  ___| | _ ) _____ __
| _|| |\/| | |__    | |/ _ \/ _ \ | _ \/ _ \ \ /
|___|_|  |_|____|   |_|\___/\___/_|___/\___/_\_\\
""")

choice = input("""
        [1] Read EML header
        [2] Decode base64 to text
        [3] Encode text to base64
        [4] Send an email (new)
        [5] SEND an EML as email
        [6] SCAN an EML
        [0] Exit 
        >>> """)

#RED ERROR"
def error(err):
    print(f"\033[91m {err}\033[00m")

#1 READ EML HEADER#
def reademl():
    filepath = input("\nEnter file path: ")
    emlFile = open(filepath, "r")
    msg = email.message_from_file(emlFile)
    emlFile.close()

    parser = email.parser.HeaderParser()
    header = parser.parsestr(msg.as_string())

    for h in header.items():
        print(h)

#2 DECODE#
def decode():
    text = input("\nEnter base64 string: ")
    if text:
        try:
            b64_txt = text
            b64_bytes = b64_txt.encode('utf-8')
            txt_bytes = base64.b64decode(b64_bytes)
            clear_txt = txt_bytes.decode('utf-8')
            print(clear_txt)
        except:
            error("Please enter a valid base64 string!")

#3 ENCODE#
def encode():
    b64txt = input("\nEnter txt string: ")
    if b64txt:
        try:
            clear_txt = b64txt
            txt_bytes = clear_txt.encode('utf-8')
            b64_bytes = base64.b64encode(txt_bytes)
            b64_txt = b64_bytes.decode('utf-8')
            print(b64_txt)
        except:
            error("Please enter a valid utf-8 string!")

#4 SEND AN EMAIL#
def send():
    fromaddr = input("\nMAIL FROM: ")
    toaddr = input("RCPT TO: ")
    subject = input("SUBJECT: ")
    content = input("DATA: ")
    msg = """\
            From: "%s"\r\n\
            To: "%s"\r\n\
            Subject: "%s"\r\n\
            \r\n\
            "%s"
            """ % (fromaddr,",".join(toaddr),subject,content)

    try:
        server = smtplib.SMTP('smtp.yopmail.com', 25)
        server.sendmail(fromaddr, toaddr, msg)
        return {"code": "250", "message": "OK"}
    except smtplib.SMTPException as e:
        print(e)
    server.quit()

#5 SEND AN EML AS EMAIL
def sendeml():
    fromaddr = input("\nMAIL FROM: ")
    toaddr = input("RCPT TO: ")
    eml_path = input("path of your EML: ")
    try:
        eml_file = open(eml_path, "r")
        msg = email.message_from_file(eml_file)
        eml_file.close()
    except:
        print("Bad path/file | Error")

    try:
        server = smtplib.SMTP('smtp.yopmail.com', 25)
        server.helo = "goto.fr"
        result_smtp = server.sendmail(fromaddr, toaddr, msg.as_string())
        server.quit()
        return {"code": "250", "message": "OK"}
    except smtplib.SMTPException as e:
        print(e)

#6 SCAN AN EMAIL#
def scanfile():
    chfile = input("\nPath of your file: ")
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'
    params = {'apikey': 'f01114f93052b4534fce7308988ff069df6b1ef9bb2383723bb38872aa0d56dc'}
    files = {'file': (f'{chfile}', open(f'{chfile}', 'rb'))}
    response = requests.post(url, files=files, params=params)
    dataa = response.json()
    perma = dataa['permalink']
    print("Scan URL: "+perma)

#USER CHOICE
if choice == "1":
    reademl()
elif choice == "2":
    decode()
elif choice == "3":
    encode()
elif choice == "4":
    sendmail()
elif choice == "5":
    sendeml()
elif choice == "6":
    scanfile()
elif choice == "7":
    diff2headers()
else:
    yellowtxt("\nGood Bye Sir!")


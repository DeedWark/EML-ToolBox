#!/usr/bin/env python3
###################################
##     Kenji DURIEZ - 08/2020    ##
##github.com/DeedWark/EML-ToolBox##
##            Ver 1.0            ##
###################################

import os
import email
import email.parser
from email.parser import HeaderParser
import base64
import smtplib
import dns.resolver
import requests
import json

#yellow color / Term display
def yellowtxt(yellow):
    print(f"\033[93m{yellow}\033[00m")
def greentxt(green):
    print(f"\033[92m{green}\033[00m")
def error(err):
    print(f"\033[91m{err}\033[00m")

yellowtxt("""
 ___ __  __ _      _____         _ ___
| __|  \/  | |    |_   _|__  ___| | _ ) _____ __
| _|| |\/| | |__    | |/ _ \/ _ \ | _ \/ _ \ \ /
|___|_|  |_|____|   |_|\___/\___/_|___/\___/_\_\\
""")

choice = input("""\
        [1] Read EML header
        [2] Decode base64 to text
        [3] Encode text to base64
        [4] Send an email (new)
        [5] Send an EML as email
        [6] Scan an EML (VirusTotal)
        [7] Help / More info
        [0] Exit
        >>> """)

#1 READ EML HEADER#
def reademl():
    filepath = input("\nEnter file path: ")
    try:
        emlFile = open(filepath, "r")
        msg = email.message_from_file(emlFile)
        emlFile.close()

        parser = email.parser.HeaderParser()
        header = parser.parsestr(msg.as_string())
        print()
    
        for h in header.items():
            print(*h)
        print()
    except:
        error("Bad file | Encoding error")

#2 DECODE BASE64#
def decode():
    b64txt = input("\nEnter base64 string: ")
    if b64txt:
        try:
            decodedB64 = base64.urlsafe_b64decode(b64txt)
            decodedStr = str(decodedB64, "utf-8")
            print(decodedStr)
        except:
            error("Please enter a valid base64 string!")

#3 ENCODE BASE64#
def encode():
    cleartxt = input("\nEnter txt string: ")
    if cleartxt:
        try:
            encodedTxt = base64.urlsafe_b64encode(cleartxt.encode("utf-8"))
            encodedStr = str(encodedTxt, "utf-8")
            print(encodedStr)
        except:
            error("Please enter a valid utf-8 string!")

#4 SEND AN EMAIL#
def sendmail():
    try:
        sender = input("\nMAIL FROM: ")
        receiver = input("RCPT TO: ")

        #Get MX/SMTP
        try:
            domain = receiver.split("@")[1]
            mx = dns.resolver.resolve(domain, "MX")
            for server in mx:
                pass
            smtp = str(server.exchange)
            smtpServ = smtp.rstrip(".")
        except:
            error("No SMTP server found!")
            exit()

        serv = input(f"SMTP (default: {smtpServ}): ")
        if serv:
            smtpServ = serv
        else:
            smtpServ = smtpServ
        subject = input("SUBJECT: ")
        alias = input("Alias / From (ex: ToolBox <toolbox@python.org>): ")
        #CONTENT (Multiline)
        multiline = []
        content = input("CONTENT: ")
        while True:
            contentline = input()
            if contentline:
                multiline.append(contentline)
            else:
                break
            contentall = '\n'.join(multiline)

        contentmore = f"""From: {alias}\nTo: {receiver}\nSubject: {subject}\n\n{contentall}"""
    except KeyboardInterrupt:
        error(" Interrupted!")
        exit()

    try:
        smtpObj = smtplib.SMTP(smtpServ, 25)
        smtpObj.sendmail(sender, receiver, contentmore)
        greentxt("250: Message sent")
        smtpObj.quit()
    except smtplib.SMTPException as e:
        error("Error - Message not sent!")
        print(e)
        exit()
    

#5 SEND AN EML AS EMAIL#
def sendeml():
    eml_path = input("\nPath of your EML: ")

    try:
        eml_file = open(eml_path, "r")
        msg = email.message_from_file(eml_file)
    except:
        error("Bad path/file | Error")
        exit()

    try:
        sender = input("MAIL FROM: ")
        receiver = input("RCPT TO: ")

        #Get MX/SMTP
        try:
            domain = receiver.split("@")[1]
            mx = dns.resolver.resolve(domain, "MX")
            for server in mx:
                pass
            smtp = str(server.exchange)
            smtpServ = smtp.rstrip(".")
        except:
            error("No SMTP server found")

        serv = input(f"SMTP (default: {smtpServ}): ")
        if serv:
            smtpServ = serv
        else:
            smtpServ = smtpServ
    except KeyboardInterrupt:
        error(" Interrupted!")
        exit()

    try:
        server = smtplib.SMTP(smtpServ, 25)
        server.sendmail(sender, receiver, msg.as_string())
        server.quit()
        greentxt("250: Message sent")
        server.close()
    except smtplib.SMTPException as e:
        error("Error - Message not sent!")
        print(e)
    eml_file.close()
    

#6 SCAN AN EMAIL (VirusTotal API)#
def scanfile():
    chfile = input("\nPath of your file: ")
    try:
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        files = {'file': (f'{chfile}', open(f'{chfile}', 'rb'))}
        params = {'apikey': 'f01114f93052b4534fce7308988ff069df6b1ef9bb2383723bb38872aa0d56dc'}
        response = requests.post(url, files=files, params=params)
        dataa = response.json()
        perma = dataa['permalink']
        print("Scan URL: "+perma)
    except:
        error("Bad path/file | Error")
        exit()
    print()
    try:
        url_res = 'https://www.virustotal.com/vtapi/v2/file/report'
        res = dataa['resource']
        params_res = {'apikey': 'f01114f93052b4534fce7308988ff069df6b1ef9bb2383723bb38872aa0d56dc', 'resource': '{}'.format(res)}

        response_res = requests.get(url_res, params=params_res)

        dataa_res = response_res.json()
        format_res = json.dumps(dataa_res, indent=4)
        print(format_res)
    except:
        print("Bad resource | Check the link")
        exit()

def help():
    info = """
    (1) Show e-mail headers (.eml file)
    (2) Decode encoded base64 string to text (utf-8) string (URL safe)
    (3) Encode text (utf-8) string to base64 string (URL safe)
    (4) Send an e-mail with smtplib (from (w/mail from), to, subject, data, smtp)
    (5) Send an .eml file as e-mail (from (w/mail from), to, subject, data, smtp)
    (6) Scan an file (With VirusTotal API | see virustotal.com/gui/home/upload for more info)
    """
    print(info)

#USER CHOICE#
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
    help()
else:
    yellowtxt("\nGood Bye Sir!")
    exit()

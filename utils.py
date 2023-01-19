import __future__
import http.client
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
from .models import *
from urllib.parse import urlparse
import json

def pad(data):
    length = 32 - (len(data) % 32)
    data += chr(length)*length
    return data


def unpad(data):

    return data[0:-ord(data[-1])]


def encrypt(plainText, workingKey, iv):
    plainText = pad(str(plainText))
    enc_cipher = AES.new(workingKey.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    encryptedText = hexlify(enc_cipher.encrypt(plainText.encode('utf-8'))).decode('utf-8')
    return encryptedText


def decrypt(cipherText, workingKey, iv):
    encryptedText = unhexlify(cipherText)
    dec_cipher = AES.new(workingKey.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    decryptedText = unpad(dec_cipher.decrypt(encryptedText).decode('utf-8'))
    return decryptedText


def checkout(encencryptedText):
    credential_obj = Credential.objects.all()
    url=str(credential_obj[0].payment_url)
    accesscode = str(credential_obj[0].accesscode)
    payment_url = urlparse(url).netloc
    conn = http.client.HTTPConnection('sandbox.hesabe.com')
    payload = json.dumps({"data":encencryptedText})

    headers = {
        'content-type': "application/json; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    }
    headers["accesscode"] = accesscode
    conn.request("POST",urlparse(url).path+'/checkout',payload, headers)
    res = conn.getresponse()

    data = res.read()
    return data.decode("utf-8")

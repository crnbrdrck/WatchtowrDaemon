#importing various modules
from firebase import firebase
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from config import *
from db import *
import subprocess

authentication = FirebaseAuthentication(FIREBASE_SECRET, email, extra={'id': ID})
firebase = FirebaseApplication(FIREBASE_URL,authentication)

def startDaemon():
    subprocess.call("./start.sh", shell=True)
    with open('osVersion.txt', 'r') as f:
        osVersion = f.readlines()
    lines = [line.rstrip('\n') for line in open('applicationList.txt')]
    print(lines[1].split(" "))
    appHashTable = {}
    for i in range(1,len(lines)):
        tempLines = lines[i].split(" ")
        appHashTable[tempLines[0]] = tempLines[1]

    
    update_server(osVersion,appHashTable)

startDaemon()
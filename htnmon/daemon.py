# Importing various modules
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from .config import *
from .db import *
import subprocess
from sys import stderr

authentication = FirebaseAuthentication(FIREBASE_SECRET, email, extra={'id': ID})
firebase = FirebaseApplication(FIREBASE_URL,authentication)

def startDaemon():
    print('HTNMon Daemon starting up', file=stderr)
    print('Starting application list fetch', file=stderr)
    subprocess.call("/bin/appList", shell=True)
    print('Application list complete', file=stderr)
    with open('osVersion.txt', 'r') as f:
        osVersion = f.readlines()
    print('Retrieved os_version', file=stderr)
    lines = [line.rstrip('\n') for line in open('applicationList.txt')]
    appHashTable = {}
    for i in range(1,len(lines)):
        tempLines = lines[i].split(" ")
        appHashTable[tempLines[0].split('/')[0]] = tempLines[1]
    print('Generated appTable. Sending data to server', file=stderr)
    update_server(osVersion,appHashTable)
    print('Success. Sleeping', file=stderr)


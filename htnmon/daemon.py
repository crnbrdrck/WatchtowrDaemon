#i mporting various modules
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from config import *
from db import *
import subprocess

authentication = FirebaseAuthentication(FIREBASE_SECRET, email, extra={'id': ID})
firebase = FirebaseApplication(FIREBASE_URL,authentication)

def startDaemon():
    osVersionCommand = "lsb_release -a"
    osVersion = subprocess.check_output(['bash','-c', osVersionCommand])
    applicationCommand = "apt list"
    applicationList = subprocess.check_output(['bash','-c', applicationCommand]).split('\n')
    applicationHash = {}
    for i in applicationList:
        tempList = i.split(" ")
        applicationHash[tempList[0]] = tempList[1]
    
    update_server(osVersion,applicationHash)

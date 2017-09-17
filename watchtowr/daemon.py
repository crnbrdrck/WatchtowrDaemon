# Importing various modules
from datetime import datetime
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from threading import Thread
import re
from shlex import split
import subprocess
from sys import stderr
from .config import SERVER_ID
from .db import *

authentication = FirebaseAuthentication(FIREBASE_SECRET, email, extra={'id': ID})
firebase = FirebaseApplication(FIREBASE_URL,authentication)


def check_commands():
    # Check for new commands to be run by this daemon process
    commands = firebase.get('commands', SERVER_ID)
    # firebase.delete('commands', SERVER_ID)
    # Run through each of the commands and run them in a subprocess
    for command in commands:
        if not command['run_time']:
            p = subprocess.Popen(split(command['cmd']), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            firebase.update('commands', command['name'], {
                'stdout': stdout.decode(),
                'stderr': stderr.decode(),
                'exit_code': p.returncode,
                'run_time': datetime.now().strftime('%H:%M:%S %d/%m/%y')
            })


def startDaemon(service_calls):
    # Start a thread to check the firebase api for commands this system needs to run
    Thread(target=check_commands).start()
    # Every 30 minutes, do the application list part
    if service_calls % 6 == 0:
        print('WatchTowr Daemon starting up', file=stderr)
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
            appHashTable[re.sub('[.$\[\]#/]', ' ', tempLines[0])] = re.sub('[.$\[\]#/]', ' ', tempLines[1])
        print('Generated appTable. Sending data to server', file=stderr)
        update_server(osVersion,appHashTable)
        print('Success. Sleeping', file=stderr)



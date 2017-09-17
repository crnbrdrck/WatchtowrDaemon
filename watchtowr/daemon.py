# Importing various modules
from datetime import datetime
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from threading import Thread
import re
from shlex import split
from shelve import open as sh_open
import subprocess
from sys import stderr
from .config import SERVER_ID
from .db import *

authentication = FirebaseAuthentication(FIREBASE_SECRET, email, extra={'id': ID})
firebase = FirebaseApplication(FIREBASE_URL,authentication)


def check_commands():
    # Check for new commands to be run by this daemon process
    commands = firebase.get('commands', SERVER_ID)
    if not commands:
        return
    # firebase.delete('commands', SERVER_ID)
    # Run through each of the commands and run them in a subprocess
    for command, data in commands.items():
        if not data['run_time']:
            safe = False
            for CMD in WHITELISTED_COMMANDS:
                if CMD in data['cmd']:
                    safe = True
                    break
            if safe:
                print('Running cmd "%s"' % command)
                p = subprocess.Popen(split(data['cmd']), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = p.communicate()
                firebase.put('commands/%s' % SERVER_ID, command, {
                    'stdout': stdout.decode(),
                    'stderr': stderr.decode(),
                    'exit_code': p.returncode,
                    'run_time': datetime.now().strftime('%H:%M:%S %d/%m/%y'),
                    'cmd': data['cmd']
                 })
            else:
                firebase.put('commands/%s' % SERVER_ID, command, {
                    'stdout': 'COMMAND NOT ALLOWED',
                    'stderr': 'COMMAND NOT ALLOWED',
                    'exit_code': -1,
                    'cmd': data['cmd']
                })


def startDaemon():
    # Start a thread to check the firebase api for commands this system needs to run
    Thread(target=check_commands).start()
    with sh_open('service_calls') as data:
        data.setdefault('service_calls', 0)
        data['service_calls'] += 1
        service_calls = data['service_calls']
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



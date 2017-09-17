from firebase.firebase import FirebaseApplication
import requests
import socket
from .config import *

firebase = FirebaseApplication(FIREBASE_URL, None)


def update_server(os_version, applications):
    # Given applications, a dict of name: version, update all information about this server
    # Get the server id from config
    server_id = SERVER_ID
    key = 'servers/' + server_id
    firebase.put(key, 'os_version', os_version)
    firebase.delete(key, 'applications')
    for application in applications:
        firebase.post(key + '/applications', {application: applications[application]})


def register_server(user_id, server_name):
    key = 'servers/'
    data = {'name': server_name, 'user_id': user_id}
    # Get the ip and lat-long position
    # Do an ipapi lookup
    response = requests.get('https://ipapi.co/json/')
    data['ip'] = response.json()['ip']
    data['location'] = {'lat': response.json()['latitude'], 'long': response.json()['longitude']}
    result = firebase.post(
        key, data)
    # Write the server id to the config file
    with open('watchtowr/config.py', 'a') as filehandle:
        filehandle.write('\n')
        filehandle.write('SERVER_ID = "')
        filehandle.write(result['name'])
<<<<<<< HEAD:htnmon/db.py
        filehandle.write('\n')
=======
        filehandle.write('"\n')
    return result['name']
>>>>>>> 03f29ebe3edfcb0968f3bc4225825007a1542bdf:watchtowr/db.py

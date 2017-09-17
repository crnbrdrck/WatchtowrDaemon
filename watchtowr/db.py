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
    firebase.post(key + '/applications', [{application: applications[application]} for application in applications])


def register_server(user_id, server_name):
    key = 'servers/'
    data = {'name': server_name, 'user_id': user_id}
    # Get the ip and lat-long position
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    data['ip'] = ip
    s.close()
    # Do an ipapi lookup
    response = requests.get('https://ipapi.co/%s/json/' % ip)
    data['location'] = (response.json()['latitude'], response.json()['longitude'])
    result = firebase.post(
        key, data)
    # Write the server id to the config file
    with open('watchtowr/config.py', 'a') as filehandle:
        filehandle.write('\n')
        filehandle.write('SERVER_ID = "')
        filehandle.write(result['name'])
        filehandle.write('"\n')
    return result['name']

from firebase.firebase import FirebaseApplication

from htnmon.config import *

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
    result = firebase.post(key, {'name': server_name, 'user_id': user_id})
    # Write the server id to the config file
    with open('config.py', 'a') as filehandle:
        filehandle.write('\n')
        filehandle.write('SERVER_ID = "')
        filehandle.write(result['name'])
        filehandle.write('\n')

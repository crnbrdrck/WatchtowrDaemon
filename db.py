from firebase.firebase import FirebaseApplication
from config import *


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

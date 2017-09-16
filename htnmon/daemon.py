#importing various modules
from firebase import firebase
from firebase.firebase import FirebaseApplication, FirebaseAuthentication

#connecting to firebase database
FIREBASE_SECRET = 'OrbXyqLOPRHI76mpc7cv8UUUVGuI8Uo5XALqt4SN'
FIREBASE_URL = 'https://htn-threatmonitor.firebaseio.com/'

email = 'basimsahaf62@gmail.com'
authentication = FirebaseAuthentication(FIREBASE_SECRET, email, extra={'id': 'MEnfSGdd6PTC9nsBT2z74jhB3KZ2'})
firebase = FirebaseApplication('https://htn-threatmonitor.firebaseio.com/',authentication)
result = firebase.get('/applications', None)
print result
print authentication.extra

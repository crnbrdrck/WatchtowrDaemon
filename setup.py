from distutils.core import setup
from watchtowr.db import register_server
from os import environ, system
from setuptools.command.install import install


class PostInstall(install):

    def run(self):
        # Register the server in our database
        user_id = environ.get('HTN_USER_ID', None)
        if user_id is None:
            raise Exception('HTN_USER_ID must be set')
        server_name = environ.get('HTN_SERVER_NAME', None)
        if server_name is None:
            raise Exception('HTN_SERVER_NAME must be set')
        print('Server ID', register_server(user_id, server_name))
        # Move the sh script to the /bin folder
        with open('watchtowr/start.sh') as infile:
            with open('/bin/appList', 'w') as outfile:
                outfile.write(infile.read())
        system('chmod +x /bin/appList')
        # Register this script as a service
        data = """[Unit]
Description=Threat monitoring service developed at Hack The North 2017  using Google's Firebase and eSentire's Cymon systems.

[Service]
ExecStart=/bin/bash -c "while true; do /usr/bin/python3 -c 'from watchtowr import daemon; daemon.startDaemon()'; sleep 30m; done;"

[Install]
WantedBy=multi-user.target
        """
        with open('/etc/systemd/system/watchtowr.service', 'w') as filehandle:
            filehandle.write(data)
        # Set up daemon to run
        system('systemctl daemon-reload; systemctl enable watchtowr; systemctl start watchtowr')
        # Super
        install.run(self)


setup(
    name='watchtowr',
    version='0.1dev',
    packages=['watchtowr'],
    license='',
    url='wat.ch/towr',
    author='A team',
    author_email='a_team@hackthenorth.com',
    cmdclass={
        'install': PostInstall
    },
    long_description='Half of our project for Hack The North 2017'
)

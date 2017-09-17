from distutils.core import setup
from htnmon.db import register_server
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
        register_server(user_id, server_name)
        # Register this script as a service
        data = """[Unit]
Description= Service developed at Hack The North using Google's Firebase and eSentire's Cymon systems.

[Service]
ExecStart=/bin/bash -c "while true; do /usr/bin/env python3 -m htnmon; sleep 30m; done;"

[Install]
WantedBy=multi-user.target
        """
        with open('/etc/systemd/system/htn.service', 'w') as filehandle:
            filehandle.write(data)
        # Set up daemon to run
        system('systemctl daemon-reload; systemctl enable htn; systemctl start htn')
        # Super
        install.run(self)


setup(
    name='HTNThreatMonitor',
    version='0.1dev',
    packages=['htnmon'],
    license='',
    url='hackthenorth.com',
    author='A team',
    author_email='a_team@hackthenorth.com',
    cmdclass={
        'install': PostInstall
    },
    long_description='Half of our project for Hack The North 2017'
)
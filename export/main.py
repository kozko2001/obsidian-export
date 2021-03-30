import aioeasywebdav
import asyncio
from os.path import basename, split

loop = asyncio.get_event_loop()

from os import environ
from sys import argv

NEXT_CLOUD_HOST = environ['NEXT_CLOUD_HOST']
NEXT_CLOUD_USER = environ['NEXT_CLOUD_USER']
NEXT_CLOUD_PASSWORD = environ['NEXT_CLOUD_PASSWORD']

source = argv[1]
destination = argv[2]

import owncloud

oc = owncloud.Client(NEXT_CLOUD_HOST)

oc.login(NEXT_CLOUD_USER, NEXT_CLOUD_PASSWORD)

oc.get_directory_as_zip(source, destination)


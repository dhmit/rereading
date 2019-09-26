"""

Local development Django settings for dhmit/rereading

Under no circumstances run the server with these settings in production!

"""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gpsthg6vl(=mziauv)us-7p8d5@ex_5j4s@gx=g$jfqdumdezv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [] # wildcard

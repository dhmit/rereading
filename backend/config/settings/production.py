"""

Production Dango settings for dhmit/rereading

"""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import


# SECURITY WARNING: keep the secret key used in production secret!
# TODO(ra): move this into an environment variable
SECRET_KEY = 'gpsthg6vl(=mziauv)us-7p8d5@ex_5j4s@gx=g$jfqdumdezv'

# SECURITY WARNING: don't run with debug turned on in production!
# TODO(ra): set false
DEBUG = True

ALLOWED_HOSTS = [
    'rereading.dhmit.xyz',
]

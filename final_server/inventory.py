import hashlib
import getpass

MAX_PORT = 49152
MIN_PORT = 10000
BASE_PORT = int(hashlib.md5(getpass.getuser()).hexdigest()[:8], 16) % \
  (MAX_PORT - MIN_PORT) + MIN_PORT

server = '127.0.0.1:%d' % BASE_PORT
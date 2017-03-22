from cache import Cache
from memcache import Client

client = Client(['localhost:11211'], debug=True)
cache = Cache(client)

import json
from redis import StrictRedis

from settings import REDIS_HOST, REDIS_PORT


class Threader:

    def __init__(self):
        self.redis = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def add_thread(self, client, thread):
        self.redis.lpush(f'threads:{client}', json.dumps(thread))

    def get_threads(self, client):
        return self.redis.lrange(f'threads:{client}', 0, -1)

    def get_thread(self, client, topic):
        threads = self.get_threads(client)
        for thread in threads:
            th = json.loads(thread)
            if th["topic"]["id"] == topic:
                return th
        return "Topic not found"

    def delete_threads(self, client):
        self.redis.delete(f'threads:{client}')

    def delete_thread(self, client, topic):
        threads = self.get_threads(client)
        self.delete_threads(client)
        deleted_thread = None
        for thread in threads:
            th = json.loads(thread)
            if th["topic"]["id"] != topic:
                self.add_thread(client, th)
            else:
                deleted_thread = th
        return deleted_thread


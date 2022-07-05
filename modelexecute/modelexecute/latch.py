import os
import redis
import uuid

class CountdownLatch():
    def __init__(self, n: int = None) -> None:
        self.redis = redis.Redis(host=os.environ['LOCALHOST'], port=6379, db=0, password=os.environ['REDIS_PASSWORD'])
        if n is not None:
            self.latch_id = str(uuid.uuid4())
            self.redis.set(self.latch_id, n)
    def countdown(self, latch_id):
        self.redis.set(latch_id, int(self.redis.get(latch_id)) - 1)
    def latch_count(self, latch_id):
        return self.redis.get(latch_id)
    def get_latch_id(self):
        return self.latch_id
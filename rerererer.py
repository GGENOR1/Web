from rediscluster import RedisCluster

 # Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "127.0.0.1", "port": "6381"}, {"host": "127.0.0.1", "port": "6382"}] # ... and etc.
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

rc.set("foo", "bar")

print(rc.get("foo"))

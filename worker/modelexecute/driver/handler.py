from statistics import mean
from modelexecute.partition import Partitioner
from modelexecute.latch import CountdownLatch
import json
import requests


def handle(req: dict):

    bucket = req['bucket']
    print(bucket)
    key = req['key']
    print(key)
    partitioner = Partitioner(bucket=bucket, key=key,
                              max_partition_size=30000, poke_increment=400)

    partitioner.partition()
    print(partitioner.get_partitions())
    latch = CountdownLatch(len(partitioner.get_partitions()))
    print(latch.get_latch_id())
    for partition in partitioner.get_partitions():
        print(partition)
        requests.post('http://gateway.openfaas.svc.cluster.local:8080/async-function/worker', json={
            'length': partition.length,
            'offset': partition.offset,
            'bucket': bucket,
            'key': key,
            'latch_id': latch.get_latch_id()
        })

    return json.dumps({
        'partitions': len(partitioner.get_partitions()),
        'latch_id': latch.get_latch_id()
    })

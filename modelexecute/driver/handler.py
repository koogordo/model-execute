from statistics import mean
from modelexecute.partition import Partitioner
from modelexecute.latch import CountdownLatch
import json
import requests


def handle(req: dict):

    bucket = req['bucket']
    key = req['key']
    max_partition_size = req['max_partition_size']
    partitioner = Partitioner(bucket=bucket, key=key,
                              max_partition_size=max_partition_size, poke_increment=400)

    partitioner.partition()

    latch = CountdownLatch(len(partitioner.get_partitions()))

    for partition in partitioner.get_partitions():

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

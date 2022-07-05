from modelexecute.partition import Partition
from modelexecute.latch import CountdownLatch
from modelexecute.awssession import AwsSession
def handle(req):
    partition: Partition = Partition(
        bucket=req['bucket'],
        key=req['key']
    )
    partition.offset = req['offset']
    partition.length = req['length']
    latch_id = req['latch_id']
    countdown_latch = CountdownLatch()
    
    s3_client = AwsSession().get_client('s3')
    
    s3_client.put_object(Bucket=partition.bucket, Key=f'{partition.key}_{countdown_latch.latch_count(latch_id)}', Body=partition.read())
    
    countdown_latch.countdown(latch_id)
    return req
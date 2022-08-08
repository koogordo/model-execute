from modelexecute.partition import Partition
from modelexecute.latch import CountdownLatch
from modelexecute.awssession import AwsSession
def handle(req):
    countdown_latch = CountdownLatch()
    latch_id = req['latch_id']
    countdown_latch.countdown(latch_id)
    
    countdown: int = int(countdown_latch.latch_count(latch_id))
    
    if countdown > 0:
        
        partition: Partition = Partition(
            bucket=req['bucket'],
            key=req['key']
        )
        partition.offset = req['offset']
        partition.length = req['length']
    
    
    
        s3_client = AwsSession().get_client('s3')
        
        raw_model_input: bytes = partition.read()['Body'].read()
        
        # TODO Load model from pkl
        # execute model on input
        # get output and format as json per line with input and corresponding output
        # put the output to s3
        model_output: bytes = b''
        s3_client.put_object(Bucket=partition.bucket, Key=f'{partition.key}_{countdown_latch.latch_count(latch_id).decode(encoding="utf-8")}', Body=model_output)
    else:
        # call the outpout consolidator
        pass
        
        
    return req
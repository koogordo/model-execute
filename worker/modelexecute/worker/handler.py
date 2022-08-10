import sys
import pandas
from io import BytesIO

from modelexecute.partition import Partition
from modelexecute.latch import CountdownLatch
from modelexecute.awssession import AwsSession
from modelexecute.modelmanager import Model, ModelDef



def handle(req):
    countdown_latch = CountdownLatch()
    latch_id = req['latch_id']
    
    countdown: int = int(countdown_latch.latch_count(latch_id))
        
    partition: Partition = Partition(
        bucket=req['bucket'],
        key=req['key']
    )
    partition.offset = req['offset']
    partition.length = req['length']



    s3_client = AwsSession().get_client('s3')
    
    raw_model_input: bytes = partition.read()['Body'].read()
    sys.stdout.write('>>>>>>>>> raw input: ' + raw_model_input.decode('utf-8'))
    sys.stdout.flush()
    # TODO Load model from pkl
    # execute model on input
    # get output and format as json per line with input and corresponding output
    # put the output to s3
    
    model: Model = Model(
        ModelDef(
            pkl_path='/home/app/function/model_store/python_model.pkl', 
            predict_method='predict', 
            output_location=f's3://model-execute/output/winequality/latch_id/{countdown}.json'
            )
        )

    model               \
    .load_model()       \
    .predict(pandas.read_json(BytesIO(raw_model_input), lines=True))          \
    .write_prediction() \
        
    countdown_latch.countdown(latch_id)
    countdown: int = int(countdown_latch.latch_count(latch_id))
    
    if countdown == 0:
        # TODO do next thing
        pass
        
        
    return req
from io import BytesIO
from typing import Dict
import pandas

from sqlalchemy import update

from flask import jsonify, make_response, Blueprint, request

from modelexecute.latch import CountdownLatch
from modelexecute.partition import Partition as Partition
from modelexecute.modelmanager import Model, ModelDef
from modelexecute.awssession import split_s3_path
from modelexecute.db import get_session
from modelexecute.models import Run, RunTask

executor_blueprint: Blueprint = Blueprint('executor', import_name=__name__)


@executor_blueprint.post('/batch')
def batch():
    session = get_session()
    data = request.get_json()
    run_task_id = data['run_task_id']
    run_task: RunTask = session.get(RunTask, run_task_id)
    run_task.status = 'RUNNING'
    session.flush()

    bucket, key = split_s3_path(run_task.run.input)
    partition: Partition = Partition(
        bucket=bucket,
        key=key
    )

    partition.offset = run_task.offset
    partition.length = run_task.length

    raw_model_input: bytes = partition.read()['Body'].read()
    output_location = f's3://model-execute/output/winequality/{run_task_id}.json'
    model: Model = Model(
        ModelDef(
            pkl_path='/home/app/function/model_store/python_model.pkl',
            predict_method='predict',
            output_location=output_location
        )
    )

    model               \
        .load_model()       \
        .predict(raw_model_input, lines=True) \
    .write_prediction()

    run_task.status = 'SUCCESS'
    session.flush()

    if len(list(filter(lambda x: x.status == 'SUCCESS', run_task.run.tasks))) == len(run_task.run.tasks):
        run: Run = session.get(Run, run_task.run_id)
        run.status = 'SUCCESS'
        session.flush()

    return make_response(jsonify({'partition_id': run_task_id}), 200)


@ executor_blueprint.post('/live')
def execute():
    return make_response(jsonify({'message': 'action is not yet supported.'}), 404)

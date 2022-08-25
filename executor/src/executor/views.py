from io import BytesIO
from flask import current_app

from sqlalchemy import update

from flask import jsonify, make_response, Blueprint, request

from modelexecute.partition import Partition as Partition
from modelexecute.model import model_service
from modelexecute.aws import split_s3_path
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

    partition.offset = run_task.beginning_offset
    partition.length = run_task.ending_offset - run_task.beginning_offset

    raw_model_input: bytes = partition.read()['Body'].read()
    output_location = f's3://model-execute/output/{current_app.config.get("MODEL_NAME")}/{run_task_id}.json'
    run_task.output = output_location

    prediction: str = model_service.predict(raw_model_input)
    model_service.write_prediction(
        location=output_location, prediction=prediction)

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

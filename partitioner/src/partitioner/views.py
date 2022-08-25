from flask import Blueprint, current_app, request, make_response, jsonify
from requests import post

from modelexecute.partition import Partitioner
from modelexecute.aws import split_s3_path
from modelexecute.db import get_session
from modelexecute.models import RunTask

partitioner_blueprint: Blueprint = Blueprint(
    'partitioner', import_name=__name__)


@partitioner_blueprint.post('/partition')
def partition():
    session = get_session()
    data = request.get_json()
    run_task_id = data['run_task_id']
    print(run_task_id)
    run_task: RunTask = session.get(RunTask, run_task_id)

    run_task.status = 'PARTITIONING'

    session.commit()

    bucket, key = split_s3_path(run_task.run.input)
    partitioner: Partitioner = Partitioner(
        bucket=bucket, key=key, max_partition_size=run_task.run.max_partition_size, poke_increment=1000)

    run_task.ending_offset = partitioner.get_ending_offset(
        run_task.partition_num)

    session.commit()

    if len(list(filter(lambda x: x.ending_offset is not None, run_task.run.tasks))) == len(run_task.run.tasks):
        post(current_app.config.get('CONTROLPLANE_URL'),
             json={'run_id': str(run_task.run.id)})

    return make_response(jsonify(data), 200)

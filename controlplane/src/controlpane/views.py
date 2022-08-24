
import uuid
from flask import Blueprint, current_app
from requests import post

from modelexecute.partition import Partitioner
from modelexecute.db import get_session
from modelexecute.models import Run, RunTask

from flask import request, jsonify, make_response


controlplane_blueprint: Blueprint = Blueprint(
    'controlplane', import_name=__name__)


@controlplane_blueprint.post('/submit')
def submit() -> None:
    session = get_session()
    data = request.get_json()
    bucket = data['bucket']
    key = data['key']
    max_partition_size = data['max_partition_size']
    input = f's3://{bucket}/{key}'
    run_id: str = str(uuid.uuid4())
    run: Run = Run(
        id=run_id,
        model_name=current_app.config.get('MODEL_NAME'),
        input=input,
        status='RUNNING'
    )
    session.add(run)
    session.commit()

    partitioner = Partitioner(bucket=bucket, key=key,
                              max_partition_size=max_partition_size, poke_increment=400)

    partitioner.partition()

    for partition in partitioner.get_partitions():
        run_task_id: str = str(uuid.uuid4())
        run_task: RunTask = RunTask(
            id=run_task_id,
            length=partition.length,
            offset=partition.offset,
            run_id=run_id,
            status='SCHEDULED'
        )
        session.add(run_task)
        session.flush()
        post(current_app.config.get('EXECUTOR_URL'), json={
            'run_task_id': run_task_id
        })
            

    return make_response(jsonify({
        'run_id': run_id
    }), 200)

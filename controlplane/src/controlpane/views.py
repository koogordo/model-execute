
import uuid
from flask import Blueprint, current_app, request, jsonify, make_response
from requests import post

from modelexecute.partition import Partitioner
from modelexecute.db import get_session
from modelexecute.models import Run, RunTask


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
        max_partition_size=max_partition_size,
        status='RUNNING'
    )
    session.add(run)
    session.commit()

    partitioner = Partitioner(bucket=bucket, key=key,
                              max_partition_size=max_partition_size, poke_increment=1000)

    # partitioner.partition()

    for i in range(partitioner.number_of_partitions()):
        run_task_id: str = str(uuid.uuid4())
        run_task: RunTask = RunTask(
            id=run_task_id,
            run_id=run_id,
            partition_num=i+1,
            status='SCHEDULED'
        )
        session.add(run_task)
        session.commit()
        post(current_app.config.get('PARTITIONER_URL'), json={
            'run_task_id': run_task_id
        })

    return make_response(jsonify({
        'run_id': run_id
    }), 200)


@controlplane_blueprint.post('/submit-partitions')
def submit_partitions():
    session = get_session()
    data = request.get_json()
    run_id = data['run_id']

    run: Run = session.get(Run, run_id)

    for i in range(len(run.tasks)):
        if i == 0:
            run.tasks[i].beginning_offset = 0
        else:
            run.tasks[i].beginning_offset = run.tasks[i-1].ending_offset

        run.tasks[i].status = 'SCHEDULED'

        session.commit()

        post(current_app.config.get('EXECUTOR_URL'), json={
            'run_task_id': str(run.tasks[i].id)
        })

    return make_response(jsonify({
        'run_id': run_id
    }), 200)

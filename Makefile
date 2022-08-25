start-env:
	docker-compose up -d

teardown:
	docker-compose down

seed-model-input:
	awslocal s3 mb s3://model-execute
	awslocal s3 cp /Users/gor5760/udpr/model-execute/model_input.json  s3://model-execute/model_input.json

clean:
	rm -rf **/build
	rm -rf **/*.egg-info
	rm -rf build
	rm -rf executor/modelexecute
	rm -rf executor/src/executor.egg-info
	rm -rf executor/src/build
	rm -rf controlplane/modelexecute
	rm -rf controlplane/src/controlplane.egg-info
	rm -rf controlplane/src/build
	rm -rf partitioner/modelexecute
	rm -rf partitioner/src/partitioner.egg-info
	rm -rf partitioner/src/build
	rm -rf modelexecute/modelexecute.egg-info
	rm -rf modelexecute/build
	rm -rf modelexecute/__pycache__

sync-deps:
	pip install -r requirements.txt

dry-build:
	cp -r modelexecute controlplane/ && cp -r modelexecute executor/ && cp -r modelexecute partitioner/ && faas-cli build --shrinkwrap
	
build:
	cp -r modelexecute controlplane/ && cp -r modelexecute executor/ && cp -r modelexecute partitioner/ && faas-cli build --shrinkwrap
	docker build -f build/controlplane/Dockerfile build/controlplane -t koogordo/modelexecute-controlplane
	docker build -f build/executor/Dockerfile build/executor -t koogordo/modelexecute-executor
	docker build -f build/partitioner/Dockerfile build/partitioner -t koogordo/modelexecute-partitioner

push: 
	docker push koogordo/modelexecute-controlplane
	docker push koogordo/modelexecute-executor
	docker push koogordo/modelexecute-partitioner
deploy:
	faas-cli deploy -f stack.yml




start-env:
	docker-compose up -d

teardown:
	docker-compose down

seed:
	aws --endpoint-url=http://localhost:4566 s3 mb s3://model-execute
	aws --endpoint-url=http://localhost:4566 s3 cp /Users/gor5760/udpr/model-execute/model_input.json  s3://model-execute/model_input.json

clean:
	rm -rf build
	rm -rf worker/modelexecute
	rm -rf driver/modelexecute
	rm -rf modelexecute/modelexecute.egg-info

build:
	cp -r modelexecute driver/ && cp -r modelexecute worker/ && faas-cli build --shrinkwrap
	docker build -f build/driver/Dockerfile build/driver -t koogordo/modelexecute-driver
	docker build -f build/worker/Dockerfile build/driver -t koogordo/modelexecute-worker

push: 
	docker push koogordo/modelexecute-driver
	docker push koogordo/modelexecute-worker

deploy:
	faas-cli deploy -f stack.yml




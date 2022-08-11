# model-execute
Codebase for model exection using fan in pattern

# Overview



## Driver
Partition's the data and passes the partitions off to the worker to be handled there.

## Worker
Executes the Wine Quality model on a specific partition of the input data.

# Dev Env Setup

## Prereqs

- make
- docker
- awscli-local (pip install awscli-local)
- faas-cli
- minikube / KinD with an installation of OpenFaas
- OpenFaas gateway is port-forwarded and faas-cli is authenticated

## Setup Dev Environment

  - Update the ```LOCALSTACK``` variable in the stack.yml file for each function
    - ```LOCALSTACK=host.docker.internal``` for KinD
    - ```LOCALSTACK=host.minikube.internal``` for minikube
## Startup Dev Environment

Run the following commands:

- Start docker services
  - ```make start-env```
  
- Seed model input data in localstack s3 so it can be accessed by driver and worker
  - ```make seed-model-input```

## Deploying functions in dev environment

### clean
```make clean```
- Removes the python build files from the project.
- Removes modelexecute package from the driver and worker directories.
- Removes egg-info

### build
```make build```
- Prepares the driver and worker docker build contexts and builds the images

### push
```make push```
- pushes dockerfiles for worker and driver to registry

### deploy
```make deploy```
- deploys functions to local openfaas using faas-cli

### full deploy
```make clean build push deploy```
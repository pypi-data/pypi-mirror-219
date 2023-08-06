## Deploy

### mlflow integration

The following demonstrates how to deploy a machine learning model using MLflow and Triton server. It first installs the necessary dependencies and configures the MLflow tracking and Triton server endpoint. Then it launches Triton server using Docker and registers the model to the MLflow tracking. Finally, it deploys the MLflow model to the Triton server.  


This example presents a local path as remote model repository of tritonserver can be served, and deploying models by mlflow-tritonserver.
```bash
# Install mlflow-tritonserver
pip install mlflow-tritonserver

# Configure mlflow tracing
mlflow server

# Configure remote model store
export TRITON_MODEL_REPO=/tmp/model_repository

# Prepare local model repository as remote model store for tritonserver
mkdir $TRITON_MODEL_REPO

# Launch tritonserver with docker
docker run -it --gpus=all \
    --shm-size=256m \
    --rm \
    -p8000:8000 -p8001:8001 -p8002:8002 \
    -v $TRITON_MODEL_REPO:/tmp/model_repository \
    -v $(pwd):/workspace -w /workspace \
    nvcr.io/nvidia/tritonserver:22.12-py3 \
    bash -c 'tritonserver --model-repository=/tmp/model_repository --model-control-mode=explicit --log-verbose=1'

# Check health
curl -v localhost:8000/v2/health/ready

# Configure mlflow tracking uri for registering models using mlflow_tritonserver
export MLFLOW_TRACKING_URI=http://localhost:5000

# Register model to mlflow tracking
mlflow_tritonserver_cli publish \
    --model_name onnx_float32_int32_int32 \
    --model_directory examples/onnx_float32_int32_int32 \
    --flavor triton

# Configure a local path as remote model store
export TRITON_MODEL_REPO=/tmp/model_repository

# Configure tritonserver endpoint for deploying models using mlflow deployments
export TRITON_URL=http://localhost:8000

# Deploy mlflow model to tritonserver
# For delete and update operations, refer to mlflow-tritonserver/README.md
mlflow deployments create \
    -t triton \
    --flavor triton \
    --name onnx_float32_int32_int32 \
    -m models:/onnx_float32_int32_int32/1

# Check model config
curl localhost:8000/v2/models/onnx_float32_int32_int32/config | jq
# Check model status
curl -X POST localhost:8000/v2/repository/index | jq
```


The following example presents a s3 url from minio as remote model repository of tritonserver can be served, and deploying models by mlflow-tritonserver.
```bash
# Start docker-compose
docker-compose -f deploy/docker/docker-compose.yml up -V --remove-orphans

# Configure mlflow tracking uri for registering models using mlflow_tritonserver
export MLFLOW_TRACKING_URI=http://localhost:5000

# Register model to mlflow tracking
mlflow_tritonserver_cli publish \
    --model_name onnx_float32_int32_int32 \
    --model_directory examples/onnx_float32_int32_int32 \
    --flavor triton

# Configure a s3 url from minio as remote model store
export TRITON_MODEL_REPO=s3://http://localhost:9000/models
# Set AWS access key ID for MinIO
export AWS_ACCESS_KEY_ID=minio
# Set AWS secret access key for MinIO
export AWS_SECRET_ACCESS_KEY=minio123
# Configure tritonserver endpoint for deploying models using mlflow deployments
export TRITON_URL=http://localhost:8000

# Deploy mlflow model to tritonserver
# For unload and update operations, refer to mlflow-tritonserver/README.md
mlflow deployments create \
    -t triton \
    --flavor triton \
    --name onnx_float32_int32_int32 \
    -m models:/onnx_float32_int32_int32/1

```

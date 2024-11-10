# jaeger-fastapi

1. This repo is an working example of traceability using jaeger
2. The Microservice is in Python with FastAPI framework
3. One service calls the other service and also the external API
4. For this testing, we have used a single docker image
5. And we have created a 2 container with some environment variables whichhelps in calling other microservice
6. With this steup we trace the network movement across the services


## Steps for deployment

1. Build docker image `docker build -t jaeger/fast-api-app:latest service`
2. Do `docker compose up -d`
3. Access the Jaeger UI `http://localhost:16686`
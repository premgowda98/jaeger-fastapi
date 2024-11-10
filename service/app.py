import os
import logging
import random
import time
import asyncio

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import requests
import uvicorn

from tracing import *
from prometheus import *
from constants import OTHER_SERVICE, OTHER_SERVICE_PORT

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()
FastAPIInstrumentor.instrument_app(app)

# Logger configuration
logger = logging.getLogger('app')
logging.basicConfig(level=logging.INFO)

# Function to simulate async task duration
async def simulate_async_task():
    random_time = random.random() * 5  # Random time between 0 and 5 seconds
    await asyncio.sleep(random_time)

# Middleware for metrics tracking
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    method = request.method
    path = str(request.url.path)
    status_code = response.status_code

    # Track request metrics
    http_request_counter.labels(method=method, path=path, status_code=status_code).inc()
    request_duration_histogram.labels(method=method, path=path, status_code=status_code).observe(duration)
    request_duration_summary.labels(method=method, path=path, status_code=status_code).observe(duration)
    return response

# Example route to check service health
@app.get("/")
async def root():
    return {"status": "🏃- Running"}

@app.get("/healthy")
async def healthy():
    return {"name": "👀 - Observability 🔥- Prem Gowda", "status": "healthy"}

@app.get("/serverError")
async def server_error():
    raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/notFound")
async def not_found():
    raise HTTPException(status_code=404, detail="Not Found")

# Route to log messages
@app.get("/logs")
async def logs():
    logger.info("Here are the logs")
    logger.info("Please have a look")
    logger.info("This is just for testing")
    return {"objective": "To generate logs"}

# Simulate a crash by raising an exception
@app.get("/crash")
async def crash():
    logger.error("Intentionally crashing the server...")
    raise Exception("Crash simulated")

# Async example task with gauge
@app.get("/example")
async def example(request: Request):
    end_gauge = gauge.labels(method=request.method, status="completed").set(0)
    await simulate_async_task()
    end_gauge.set(1)
    return {"message": "Async task completed"}

@app.get("/external")
def request_call():
    url = "https://jsonplaceholder.typicode.com/posts/1"  # Example external API (JSONPlaceholder)
    
    # Make a synchronous GET request using the requests library
    response = requests.get(url)
    
    # If the request was successful, return the response data
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}
    
@app.get("/other-service")
def request_call():
    url = f"http://{OTHER_SERVICE}:{OTHER_SERVICE_PORT}/external"  # Example external API (JSONPlaceholder)
    
    # Make a synchronous GET request using the requests library
    response = requests.get(url)
    
    # If the request was successful, return the response data
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data", "status_code": response.status_code}

# Prometheus metrics route
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(REGISTRY), media_type="text/plain")

# Start the FastAPI app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)
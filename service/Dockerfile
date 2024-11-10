# Step 1: Use an official Python runtime as a parent image
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Step 4: Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of the application code into the container
COPY . /app/

# Step 6: Set environment variable to indicate that the app is running in production
ENV PYTHONUNBUFFERED=1

# Step 7: Expose the port on which the FastAPI app will run (3001 in this case)
EXPOSE 3001

# Step 8: Run the FastAPI app using uvicorn when the container starts
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3001"]

# Use an official Python runtime as a parent image
FROM python:3.11.8-bookworm

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable
ENV MODULE_NAME="main"
ENV VARIABLE_NAME="app"
ENV PORT="8000"

# Run FastAPI server when the container launches
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
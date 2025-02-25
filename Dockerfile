FROM ubuntu:latest

# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask

# Make port 8574 available to the world outside this container
EXPOSE 8574

# Run app.py when the container launches
CMD ["python", "Ex3kaplat.py"]

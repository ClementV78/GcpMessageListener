# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
#RUN pip install --no-cache-dir -r requirements.txt

# Désactiver le buffering pour s'assurer que les logs s'affichent immédiatement
ENV PYTHONUNBUFFERED=1

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable


# Run main.py when the container launches
CMD ["python", "main.py"]
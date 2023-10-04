# Use the official Python base image for FastAPI
FROM python:3.11-slim

# Copy the entire src directory into the container
COPY ./src  /app/src


# Copy the requirements file into the container
COPY ./requirements.txt /app

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt


# Expose the port that your FastAPI application will run on (default is 8000)
EXPOSE 8000

# Define the command to run your FastAPI application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]







# # Use the official Python base image for FastAPI
# FROM python:3.11.4-slim

# # Set the working directory in the container
# WORKDIR /src

# # Copy the requirements file into the container
# COPY requirements.txt .

# # Install any needed packages specified in requirements.txt
# RUN pip install -r requirements.txt

# # Copy only the main.py file from the src folder into the container's /app directory
# # COPY src/ /app/

# # Copy the main.py file from the src folder into the container's /app directory
# COPY src/main.py .

# # Copy the entire src/asset/ml directory into the container's /app directory
# COPY src/asset/ml .

# # Expose the port that your FastAPI application will run on (default is 8000)
# EXPOSE 8000

# # Define the command to run your FastAPI application
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Lightweight official Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Show Python output immediately
ENV PYTHONUNBUFFERED=1

# Working directory inside container
WORKDIR /app

# Copy only dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Run the CLI application
CMD ["python", "app.py"]




# --------------------------------------------------------
# Use the official lightweight Python 3.12 image.
# This image already contains Python, so we don't have to install it.
# The "slim" version is smaller, making our Docker image faster to download.
# --------------------------------------------------------
#FROM python:3.12-slim


# --------------------------------------------------------
# Prevent Python from creating __pycache__ (.pyc) files
# inside the Docker container.
# These files are unnecessary for our project.
# --------------------------------------------------------
#ENV PYTHONDONTWRITEBYTECODE=1


# --------------------------------------------------------
# Display Python output immediately in Docker logs.
# Without this, print() statements may appear late.
# --------------------------------------------------------
#ENV PYTHONUNBUFFERED=1


# --------------------------------------------------------
# Set the working directory inside the container.
# All upcoming commands will run from this folder.
# If the folder doesn't exist, Docker creates it automatically.
# --------------------------------------------------------
#WORKDIR /app


# --------------------------------------------------------
# Copy only the requirements file first.
# This allows Docker to cache installed dependencies.
# If only our Python code changes later,
# Docker won't reinstall all packages.
# --------------------------------------------------------
#COPY requirements.txt .


# --------------------------------------------------------
# Install all required Python packages.
# --no-cache-dir reduces the final image size.
# --------------------------------------------------------
#RUN pip install --no-cache-dir -r requirements.txt


# --------------------------------------------------------
# Copy the remaining project files into the container.
# This includes app.py, database.py, tests, etc.
# --------------------------------------------------------
#COPY . .


# --------------------------------------------------------
# Start the application when the container starts.
# Docker automatically executes this command.
# --------------------------------------------------------
#CMD ["python", "app.py"]
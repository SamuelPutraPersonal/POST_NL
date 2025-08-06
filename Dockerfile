# Dockerfile

# Step 1: Start with a base image.
# This tells Docker to use a pre-built image that already has Python 3.9 installed,
# specifically a "slim" version which is smaller and more efficient.
FROM python:3.9-slim

# Step 2: Set the working directory in the container.
# All subsequent commands will run from this /app directory inside the Docker container.
WORKDIR /app

# Step 3: Copy the requirements.txt file into the /app directory in the container.
# We copy this first because if only requirements.txt changes, Docker can reuse previous steps.
COPY requirements.txt .

# Step 4: Install the Python dependencies listed in requirements.txt.
# --no-cache-dir saves space by not storing pip's cache.
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of our application's code (app.py, postal_validator.py)
# from your local folder into the /app directory in the container.
# The '.' on the left means "everything in the current directory (your project folder)".
# The '.' on the right means "to the current working directory in the container (/app)".
COPY . .

# Step 6: Tell Docker that our application will listen on port 5000 inside the container.
# This is just documentation; it doesn't actually publish the port to your computer.
EXPOSE 5000

# Step 7: Define the command that Docker should run when a container starts from this image.
# This will start our Flask application.
CMD ["python", "app.py"]

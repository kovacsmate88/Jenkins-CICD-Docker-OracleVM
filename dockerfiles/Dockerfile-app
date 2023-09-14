# Use an official Python runtime based on Alpine 3.17 as the base image.
# Alpine is often used to make lightweight images.
FROM python:3.9-alpine3.17

# Set the working directory inside the container to "/app".
WORKDIR /app

# Copy the files 'app.py' and 'requirements.txt' from the local directory to the "/app" directory in the container.
COPY app.py requirements.txt /app/

# Install any packages specified in 'requirements.txt'.
# Since we're using Alpine, pip3 installs Python packages into the Alpine image.
RUN pip3 install -r requirements.txt

# Run 'python3 app.py' when the container launches.
# This will start the Flask application.
CMD python3 app.py

# Expose port 5000 to interact with the application.
# This should match the port number in your Flask app.
EXPOSE 5000

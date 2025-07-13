# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of our application code (app.py) into the container
COPY . .

# Make port 8501 available to the world outside this container (Streamlit's default port)
EXPOSE 8501

# Define the command to run the app when the container starts
CMD ["streamlit", "run", "app.py"]
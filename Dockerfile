FROM python:3.12
# Set the working directory inside the container to /app
WORKDIR /app
# Copy the requirements.txt file from the host to the container's working directory
COPY requirements.txt .
# Install the requirements specified in requirements.txt using pip
RUN pip install -r requirements.txt
# Copy all the files from the host to the container's working directory
COPY . .
# Expose port 8000 for the application
EXPOSE 8000
# Start the application using uvicorn with the specified host and port
CMD ["uvicorn", "src.main:server", "--host", "0.0.0.0", "--port", "8000"]
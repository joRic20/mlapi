# Use a slim Python base image
FROM python:3.10-slim-buster

# Set working directory inside container
WORKDIR /app

# Copy and install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code into the image
COPY app/ /app

# Expose port 80 to the host
EXPOSE 80

# Launch Uvicorn, referencing main:app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

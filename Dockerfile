## Parent image
FROM python:3.10-slim

## Essential environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

## Work directory inside the docker container
WORKDIR /app

# Copy only the files required for installing dependencies
COPY setup.py requirements.txt ./

## Installing system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      curl && \
    rm -rf /var/lib/apt/lists/*

## Install Python dependencies setup.py "--no-cache-dir" removes the cache after installation
RUN pip install --no-cache-dir \
      --extra-index-url https://download.pytorch.org/whl/cpu \
      torch==2.7.1+cpu && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e .

# Copy the rest of the application code
COPY . .

## Expose only flask port
EXPOSE 5000

## Run the Flask app
CMD ["python", "app/application.py"]
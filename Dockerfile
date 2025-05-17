FROM python:3.12-slim

# Install system dependencies (optional but common)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

COPY . .

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["uvicorn", "--port", "8000", "--host", "0.0.0.0",  "app:app"]
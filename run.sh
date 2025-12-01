#!/bin/bash

# Wait for MongoDB to be ready (with better error handling)
echo "Waiting for MongoDB to be ready..."
max_attempts=30
attempt=0

while [ $attempt -lt $max_attempts ]; do
  if python -c "import pymongo; pymongo.MongoClient('${MONGO_URI}', serverSelectionTimeoutMS=5000).server_info()" 2>/dev/null; then
    echo "MongoDB is ready!"
    break
  fi
  attempt=$((attempt + 1))
  echo "MongoDB connection attempt $attempt/$max_attempts - sleeping"
  sleep 2
done

if [ $attempt -eq $max_attempts ]; then
  echo "Warning: Could not connect to MongoDB after $max_attempts attempts. Starting app anyway..."
fi

# Run the Flask application
python -m src.app


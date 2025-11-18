#!/bin/bash

# Wait for MongoDB to be ready
echo "Waiting for MongoDB to be ready..."
until python -c "import pymongo; pymongo.MongoClient('${MONGO_URI}', serverSelectionTimeoutMS=2000).server_info()" 2>/dev/null; do
  echo "MongoDB is unavailable - sleeping"
  sleep 2
done

echo "MongoDB is ready!"

# Run the Flask application
python -m src.app


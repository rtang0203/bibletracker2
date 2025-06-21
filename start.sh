#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 5

# Run database migrations
echo "Running database migrations..."
flask db upgrade

# Start the application
echo "Starting application..."
gunicorn run:app 
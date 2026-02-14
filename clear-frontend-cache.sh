#!/bin/bash
# Script to clear Next.js cache and restart frontend container

echo "=== Clearing Next.js Cache and Restarting Frontend ==="

# Stop the frontend container
echo "1. Stopping frontend container..."
docker-compose stop frontend

# Remove the .next cache directory from the host machine
echo "2. Removing .next cache directory..."
rm -rf frontend/.next
echo "   Cache cleared!"

# Restart the frontend container
echo "3. Starting frontend container..."
docker-compose up -d frontend

# Show logs
echo "4. Showing frontend logs (press Ctrl+C to exit)..."
sleep 3
docker-compose logs -f frontend

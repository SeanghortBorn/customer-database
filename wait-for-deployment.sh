#!/bin/bash

BACKEND_URL="${BACKEND_URL:-https://customer-db-api.onrender.com}"
MAX_ATTEMPTS=60
WAIT_SECONDS=5

echo "⏳ Waiting for Render deployment to complete..."
echo "📍 Monitoring: $BACKEND_URL/health/full"
echo ""

for i in $(seq 1 $MAX_ATTEMPTS); do
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/health/full")
    
    if [ "$HTTP_CODE" = "200" ]; then
        echo "✅ Deployment complete! Backend is ready."
        echo ""
        echo "Running full verification..."
        sleep 2
        ./test-production.sh
        exit 0
    elif [ "$HTTP_CODE" = "404" ]; then
        echo -ne "⏳ Attempt $i/$MAX_ATTEMPTS: Old version still running (404)... \r"
    elif [ "$HTTP_CODE" = "000" ] || [ "$HTTP_CODE" = "502" ] || [ "$HTTP_CODE" = "503" ]; then
        echo -ne "🔄 Attempt $i/$MAX_ATTEMPTS: Deployment in progress ($HTTP_CODE)... \r"
    else
        echo -ne "⚠️  Attempt $i/$MAX_ATTEMPTS: Unexpected status ($HTTP_CODE)... \r"
    fi
    
    sleep $WAIT_SECONDS
done

echo ""
echo "⏱️  Timeout reached. Check Render dashboard for deployment status:"
echo "   https://dashboard.render.com"

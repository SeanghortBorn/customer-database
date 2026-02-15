#!/bin/bash

# Replace these with your actual URLs
BACKEND_URL="${BACKEND_URL:-https://your-backend.onrender.com}"
FRONTEND_URL="${FRONTEND_URL:-https://your-app.vercel.app}"

echo "🔍 Testing Production Deployment..."
echo "📍 Backend:  $BACKEND_URL"
echo "📍 Frontend: $FRONTEND_URL"
echo ""

# Function to check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "⚠️  jq is not installed. Install it for pretty JSON output:"
    echo "   Ubuntu/Debian: sudo apt-get install jq"
    echo "   macOS: brew install jq"
    echo ""
    echo "Continuing without pretty printing..."
    JQ_CMD="cat"
else
    JQ_CMD="jq '.'"
fi

echo "1️⃣ Testing Backend Health..."
HTTP_CODE=$(curl -s -o response.json -w "%{http_code}" "$BACKEND_URL/health")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Status: $HTTP_CODE"
    cat response.json | eval $JQ_CMD
else
    echo "❌ Status: $HTTP_CODE"
    cat response.json
fi
echo ""

echo "2️⃣ Testing Full Health Check (Database + Supabase)..."
HTTP_CODE=$(curl -s -o response.json -w "%{http_code}" "$BACKEND_URL/health/full")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Status: $HTTP_CODE"
    cat response.json | eval $JQ_CMD
else
    echo "❌ Status: $HTTP_CODE"
    cat response.json
fi
echo ""

echo "3️⃣ Testing Backend Root Endpoint..."
HTTP_CODE=$(curl -s -o response.json -w "%{http_code}" "$BACKEND_URL/")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Status: $HTTP_CODE"
    cat response.json | eval $JQ_CMD
else
    echo "❌ Status: $HTTP_CODE"
    cat response.json
fi
rm -f response.json
echo ""

echo "4️⃣ Testing Frontend Availability..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Frontend Status: $HTTP_CODE"
else
    echo "❌ Frontend Status: $HTTP_CODE"
fi
echo ""

echo "5️⃣ Testing API Documentation..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/docs")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Swagger UI available at: $BACKEND_URL/docs"
else
    echo "⚠️  Swagger UI Status: $HTTP_CODE"
fi
echo ""

echo "📋 Summary:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Next Steps:"
echo "   1. Visit $BACKEND_URL/docs to see API documentation"
echo "   2. Visit $FRONTEND_URL and open browser console (F12)"
echo "   3. Try signing up with a test account"
echo "   4. Create a test workspace and list"
echo "   5. Check browser Network tab for API call responses"
echo ""
echo "🔧 If issues found:"
echo "   - Check Render logs for backend errors"
echo "   - Check Vercel logs for frontend errors"
echo "   - Verify environment variables are set correctly"
echo "   - See docs/05-operations/PRODUCTION_VERIFICATION.md"

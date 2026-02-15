# Production Verification Guide

This guide helps you verify that your frontend, backend, and Supabase are all connected successfully in production.

## 1. Backend Health Checks

### Basic Health Check
Tests if the backend API is running:
```bash
curl https://your-backend-url.onrender.com/health
```
Expected response:
```json
{"status": "ok", "service": "api"}
```

### Full Health Check
Tests database and Supabase connections:
```bash
curl https://your-backend-url.onrender.com/health/full
```
Expected response:
```json
{
  "status": "ok",
  "service": "api",
  "checks": {
    "database": {"status": "ok", "message": "Connected"},
    "supabase": {"status": "ok", "message": "Client initialized"}
  }
}
```

## 2. Check Render Logs

### View Backend Logs
1. Go to https://dashboard.render.com
2. Select your backend service
3. Click "Logs" tab
4. Look for:
   - ✅ `Uvicorn running on http://0.0.0.0:PORT`
   - ✅ `Application startup complete`
   - ❌ Any error messages or stack traces

### Common Error Patterns
- **ModuleNotFoundError**: Import path issues
- **Connection refused**: Database connection problems
- **Authentication failed**: Supabase credentials issue
- **Port binding failed**: Port configuration issue

## 3. Test Backend API Endpoints

### Test Root Endpoint
```bash
curl https://your-backend-url.onrender.com/
```
Expected: `{"message": "Customer Database API v0.1.0"}`

### Test API Documentation
Visit in browser:
- **Swagger UI**: `https://your-backend-url.onrender.com/docs`
- **ReDoc**: `https://your-backend-url.onrender.com/redoc`

Should see interactive API documentation if backend is running correctly.

## 4. Test Frontend Connection to Backend

### Check Browser Console
1. Open your frontend URL in browser (Vercel deployment)
2. Press `F12` to open Developer Tools
3. Go to "Console" tab
4. Look for:
   - ❌ CORS errors (cross-origin blocked)
   - ❌ Network errors (failed to fetch)
   - ❌ 401/403 errors (authentication issues)
   - ✅ Successful API responses with data

### Check Network Tab
1. In Developer Tools, go to "Network" tab
2. Try logging in or accessing a page
3. Look for API requests to your backend
4. Click on each request to see:
   - **Status**: Should be 200 (success), not 404/500
   - **Response**: Should contain expected JSON data
   - **Headers**: Should have proper CORS headers

## 5. Test Supabase Connection

### From Backend
The `/health/full` endpoint already tests this.

### From Frontend (Browser Console)
```javascript
// In your frontend at https://your-app.vercel.app
// Open browser console and type:
console.log(window.location.origin); // Verify correct domain
```

## 6. End-to-End Test Flow

### Manual Test Checklist
1. ✅ **Sign Up**: Create new account
   - Should redirect to JWT Authentication
   - Should return JWT token
   - Should create user in Supabase
   
2. ✅ **Login**: Sign in with credentials
   - Should authenticate via Supabase
   - Should receive access token
   - Frontend stores token in localStorage
   
3. ✅ **Create Workspace**: Make new workspace
   - Frontend sends POST to `/api/v1/workspaces`
   - Backend validates JWT token
   - Backend creates workspace in database
   - Response returns workspace data
   
4. ✅ **View Workspaces**: List all workspaces
   - Frontend sends GET to `/api/v1/workspaces`
   - Backend queries database
   - Returns array of workspaces
   
5. ✅ **Create List**: Add list to workspace
   - Frontend sends POST to `/api/v1/workspaces/{id}/lists`
   - Backend creates list
   - Audit log created

## 7. Environment Variables Check

### Backend (Render)
Verify these are set in Render dashboard:
```bash
DATABASE_URL=postgresql://...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJhbG...
FRONTEND_URL=https://your-app.vercel.app
```

### Frontend (Vercel)
Verify these are set in Vercel dashboard:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbG...
```

## 8. Quick Verification Script

Save this as `test-production.sh`:
```bash
#!/bin/bash

BACKEND_URL="https://your-backend.onrender.com"
FRONTEND_URL="https://your-app.vercel.app"

echo "🔍 Testing Production Deployment..."
echo ""

echo "1️⃣ Testing Backend Health..."
curl -s "$BACKEND_URL/health" | jq '.'
echo ""

echo "2️⃣ Testing Full Health Check..."
curl -s "$BACKEND_URL/health/full" | jq '.'
echo ""

echo "3️⃣ Testing Backend Root..."
curl -s "$BACKEND_URL/" | jq '.'
echo ""

echo "4️⃣ Testing Frontend (HTTP Status)..."
curl -I "$FRONTEND_URL" 2>&1 | grep "HTTP"
echo ""

echo "✅ Manual checks:"
echo "   - Visit $BACKEND_URL/docs for API docs"
echo "   - Visit $FRONTEND_URL and check browser console"
echo "   - Try signing up and creating a workspace"
```

Run with:
```bash
chmod +x test-production.sh
./test-production.sh
```

## 9. Common Issues and Solutions

### CORS Errors
**Symptom**: Browser console shows "blocked by CORS policy"
**Solution**: Add your frontend URL to `FRONTEND_URL` env var in Render

### 502 Bad Gateway
**Symptom**: Render shows 502 error
**Solution**: Check logs, backend may have crashed. Look for Python errors.

### Database Connection Failed
**Symptom**: `/health/full` shows database error
**Solution**: Verify `DATABASE_URL` is correct in Render env vars

### JWT Authentication Fails
**Symptom**: Login returns 401 or token validation fails
**Solution**: 
- Verify `SUPABASE_URL` and `SUPABASE_ANON_KEY` match in both frontend and backend
- Check Supabase dashboard for service status

### Frontend Can't Reach Backend
**Symptom**: All API calls fail with "Failed to fetch"
**Solution**: 
- Verify `NEXT_PUBLIC_API_URL` in Vercel matches your Render backend URL
- Check if backend is actually running on Render

## 10. Monitoring in Production

### Set Up Logging
- **Render**: Use built-in logs viewer
- **Vercel**: Check "Functions" tab for SSR logs

### Key Metrics to Watch
- Response times (should be < 1s)
- Error rates (should be near 0%)
- Database connection pool usage
- Memory usage

### Alerts to Set Up
- Backend health check failing
- 5xx error rate > 1%
- Database connection failures
- High response times (> 3s)

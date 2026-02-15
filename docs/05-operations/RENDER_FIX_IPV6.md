# Fix Render IPv6 Connection Issue

## Current Error
```
connection to server at "db.pbbkfqitjsaquaelwbsu.supabase.co" (IPv6 address), port 6543 failed: Network is unreachable
```

## Root Cause
Render doesn't support IPv6 connections to Supabase. We need to force IPv4 and use proper connection pooling.

## IMMEDIATE FIX - Update Render Environment Variable

### Step 1: Go to Render Dashboard
1. Open: https://dashboard.render.com
2. Select your service: **customer-db-api**
3. Click **Environment** tab
4. Find `DATABASE_URL` variable

### Step 2: Update DATABASE_URL

**Use Supabase's AWS IPv4-only pooler endpoint:**

```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**Key Changes:**
- ✅ Uses AWS pooler: `aws-0-us-east-1.pooler.supabase.com` (IPv4-only)
- ✅ Port `6543` (Transaction Mode)
- ✅ User format: `postgres.{project-ref}` → `postgres.pbbkfqitjsaquaelwbsu`
- ✅ Password URL-encoded: `-sA!?WN>,025` → `-sA%21%3FWN%3E%2C025`
- ✅ **No IPv6 resolution issues**

### Step 3: Save and Redeploy
1. Click **Save Changes**
2. Render will automatically redeploy
3. Wait 2-3 minutes for deployment

### Step 4: Verify Connection
After deployment completes:

```bash
# Check health endpoint
curl https://customer-db-api.onrender.com/health

# If you have a database health check endpoint
curl https://customer-db-api.onrender.com/health/database
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## Alternative Solutions (If Above Doesn't Work)

### Option 1: Use Session Pooler with Explicit IPv4
```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

This uses Supabase's AWS pooler which typically has better IPv4 support.

### Option 2: Add Connection Pool Settings to database.py
If the connection string alone doesn't work, update your database configuration.

## Troubleshooting

### Still seeing IPv6 errors?
1. Clear Render's build cache:
   - In Render dashboard → Settings
   - Click "Clear build cache & deploy"

2. Check Supabase project status:
   - https://status.supabase.com
   - Ensure no ongoing incidents

3. Verify your Supabase database is running:
   - Go to https://app.supabase.com
   - Check project health

### Connection timeout errors?
Add connection pool parameters to [database.py](../../backend/shared/database.py):
```python
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10
)
```

## Password URL Encoding Reference

Your Supabase password contains special characters that must be URL-encoded:

| Character | URL Encoded |
|-----------|-------------|
| `-`       | `-` (no change) |
| `!`       | `%21` |
| `?`       | `%3F` |
| `>`       | `%3E` |
| `,`       | `%2C` |

**Original:** `-sA!?WN>,025`  
**Encoded:** `-sA%21%3FWN%3E%2C025`

## Why Port 6543?

| Port | Mode | Render Support |
|------|------|----------------|
| 5432 | Direct connection | ❌ IPv6 issues |
| 6543 | Transaction pooler | ✅ Works with IPv4 |
| 5432 (pooler) | Session pooler | ✅ Alternative option |

Transaction pooler (6543) is recommended for serverless/cloud platforms like Render.

## Local Development vs Production

**Local (.env file):**
```env
DATABASE_URL=postgresql://postgres:-sA!?WN>,025@db.pbbkfqitjsaquaelwbsu.supabase.co:5432/postgres
```
- Direct connection (port 5432) works fine locally
- No need to URL-encode

**Render (Environment Variables):**
```
postgresql://postgres:-sA%21%3FWN%3E%2C025@db.pbbkfqitjsaquaelwbsu.supabase.co:6543/postgres
```
- Must use pooler (port 6543)
- Must URL-encode special characters

## Next Steps After Fix

1. Monitor deployment logs in Render
2. Test your API endpoints
3. Verify database queries work
4. Update any documentation with successful configuration

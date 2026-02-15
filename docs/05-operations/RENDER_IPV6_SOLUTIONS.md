# Render IPv6 Connection Issue - Complete Solutions

## Problem Summary
Render's network infrastructure resolves Supabase hostnames to IPv6 addresses, but IPv6 connectivity fails with "Network is unreachable" error.

## ✅ SOLUTION 1: Use Supabase AWS IPv4-only Pooler (RECOMMENDED)

This uses Supabase's AWS regional pooler which is IPv4-only and specifically designed for cloud platforms.

### Update DATABASE_URL in Render Dashboard:

```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**Why this works:**
- `aws-0-us-east-1.pooler.supabase.com` = IPv4-only endpoint
- Port `6543` = Transaction mode (perfect for serverless/APIs)
- No IPv6 address resolution

**Steps:**
1. Go to https://dashboard.render.com
2. Select: **customer-db-api**
3. Environment tab → Find `DATABASE_URL`
4. Paste the connection string above
5. Save → Auto-redeploys in 2-3 minutes

---

## ✅ SOLUTION 2: Try Different Region Pooler

If the US East pooler doesn't work, try other AWS regions:

### Option A: US West
```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-us-west-1.pooler.supabase.com:6543/postgres
```

### Option B: EU Central (if your Supabase is in EU)
```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-eu-central-1.pooler.supabase.com:6543/postgres
```

---

## ✅ SOLUTION 3: Check Supabase Pooler Documentation

If the above URLs don't work, get the correct pooler URL from Supabase:

1. Go to https://app.supabase.com
2. Select your project: **pbbkfqitjsaquaelwbsu**
3. Settings → Database
4. Find **Connection Pooling** section
5. Look for **Transaction mode** connection string
6. Copy the URL (it should look like: `postgres://postgres.[project]@aws-0-[region].pooler.supabase.com:6543/postgres`)
7. Replace `[YOUR-PASSWORD]` with: `-sA%21%3FWN%3E%2C025` (URL-encoded)

---

## ✅ SOLUTION 4: Use Session Mode Pooler (Port 5432)

If transaction mode doesn't work, try session mode:

```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```

**Differences:**
- Port `5432` = Session mode
- Maintains database sessions longer
- Slightly different behavior than transaction mode

---

## 🔍 Verification After Changing DATABASE_URL

### 1. Check Render Logs
Watch the deployment logs in Render dashboard:
- Should see: "Application startup complete"
- Should NOT see: "Network is unreachable"

### 2. Test Health Endpoint
```bash
curl https://customer-db-api.onrender.com/health/full
```

Expected response:
```json
{
  "status": "ok",
  "service": "api",
  "checks": {
    "database": {
      "status": "ok",
      "message": "Connected"
    }
  }
}
```

### 3. Check Database Connection in Logs
Look for SQLAlchemy connection messages in Render logs - should show successful pool creation.

---

## 🚨 If Still Failing

### Check 1: Verify Password Encoding
Your password: `-sA!?WN>,025`

URL-encoded characters:
| Original | Encoded |
|----------|---------|
| !        | %21     |
| ?        | %3F     |
| >        | %3E     |
| ,        | %2C     |

Result: `-sA%21%3FWN%3E%2C025`

### Check 2: Verify Supabase Database is Running
1. Go to https://app.supabase.com
2. Check project status (should be "Active")
3. Try connecting from Table Editor to ensure DB is up

### Check 3: Check Supabase Connection Pooler Status
1. Supabase Dashboard → Settings → Database
2. Verify "Enable connection pooler" is ON
3. Check pooler endpoints are available

### Check 4: Try Direct IPv4 Address (Temporary Test)

You can temporarily test with an IPv4 address to isolate the issue:

```bash
# Find IPv4 address of Supabase host (run locally)
dig +short db.pbbkfqitjsaquaelwbsu.supabase.co A

# If you get an IPv4 address like 1.2.3.4, you can temporarily test with:
postgresql://postgres:-sA%21%3FWN%3E%2C025@1.2.3.4:6543/postgres
```

⚠️ **Note:** Don't use IP addresses in production - they can change. This is only for testing.

---

## 📝 Current Configuration Summary

### Local Development (.env file)
```env
DATABASE_URL=postgresql://postgres:-sA!?WN>,025@db.pbbkfqitjsaquaelwbsu.supabase.co:5432/postgres
```
- Direct connection (port 5432)
- Works fine locally
- No URL encoding needed

### Production (Render Environment Variables)
```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```
- AWS pooler (IPv4-only)
- Transaction mode (port 6543)
- URL-encoded password

---

## 🆘 Need More Help?

1. **Share the exact DATABASE_URL** you set in Render (hide password)
2. **Share first 50 lines** of Render deployment logs
3. **Check Supabase Dashboard** for any alerts or status issues
4. **Verify region** - Ensure pooler region matches your Supabase project region

## Additional Resources

- [Render Database Connection Docs](https://render.com/docs/databases)
- [Supabase Connection Pooling](https://supabase.com/docs/guides/database/connecting-to-postgres#connection-pooler)
- [SQLAlchemy Connection Parameters](https://docs.sqlalchemy.org/en/20/core/engines.html)

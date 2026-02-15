# Supabase Connection Pooler Configuration

## Issue: Direct Connection Fails on Render

Your current DATABASE_URL uses direct connection (port 5432) which has IPv6 routing issues with Render.

## Solution: Use Supabase Connection Pooler

### For Render (Production):

**Update DATABASE_URL in Render Dashboard:**

**Option 1: Transaction Mode (Recommended for APIs)**
```
postgresql://postgres:-sA%21%3FWN%3E%2C025@db.pbbkfqitjsaquaelwbsu.supabase.co:6543/postgres
```
- Port: `6543` (pooler)
- Best for: REST APIs, short-lived connections
- Most compatible with cloud platforms

**Option 2: Session Mode Connection Pooler**
```
postgresql://postgres.pbbkfqitjsaquaelwbsu:-sA%21%3FWN%3E%2C025@aws-0-us-east-1.pooler.supabase.com:5432/postgres
```
- Uses Supabase's session pooler
- More compatible with cloud infrastructure

### Steps to Update:

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Select your backend service** (customer-db-api)
3. **Environment tab**
4. **Find `DATABASE_URL`**
5. **Replace with Transaction Mode URL** (port 6543):
   ```
   postgresql://postgres:-sA%21%3FWN%3E%2C025@db.pbbkfqitjsaquaelwbsu.supabase.co:6543/postgres
   ```
6. **Save Changes** → Render auto-redeploys

### Verify After Update:

After ~3 minutes:
```bash
curl https://customer-db-api.onrender.com/health/full | jq '.checks.database'

# Should show:
# {
#   "status": "ok",
#   "message": "Connected"
# }
```

### For Local Development:

Your local `.env` can stay the same (direct connection usually works locally):
```env
DATABASE_URL=postgresql://postgres:-sA!?WN>,025@db.pbbkfqitjsaquaelwbsu.supabase.co:5432/postgres
```

### Why Use Port 6543?

| Port | Mode | Use Case |
|------|------|----------|
| 5432 | Direct | Local development, persistent connections |
| 6543 | Transaction Pooler | APIs, cloud platforms (Render, Vercel) |
| 5432 (pooler) | Session Pooler | Alternative cloud option |

The transaction pooler (6543) handles connection management better for ephemeral cloud environments.

### Quick Reference:

**Current (Failing):**
```
postgres://...@db.xxx.supabase.co:5432/postgres  ❌ IPv6 routing issues
```

**Updated (Working):**
```
postgres://...@db.xxx.supabase.co:6543/postgres  ✅ Pooler, no IPv6 issues
```

### Alternative: IPv4-Only Connection String

If you prefer to stay on port 5432, you can try forcing IPv4, but this is less reliable:
```
postgresql://postgres:-sA%21%3FWN%3E%2C025@ipv4.db.pbbkfqitjsaquaelwbsu.supabase.co:5432/postgres
```

**Recommended:** Use port 6543 (transaction pooler) for best results.

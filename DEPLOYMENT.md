# Deployment Guide

## Backend Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select the `customer-database` repo
   - Render will automatically detect `render.yaml`

2. **Set Environment Variables**
   
   In Render dashboard, set these variables:
   
   ```bash
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_ANON_KEY=your-anon-key
   SUPABASE_SERVICE_KEY=your-service-role-key
   SUPABASE_JWT_SECRET=your-jwt-secret
   REDIS_URL=redis://your-redis-url:6379
   FRONTEND_URL=https://your-frontend.vercel.app
   ```

3. **Deploy**
   - Click "Apply"
   - Wait for build to complete

### Option 2: Manual Configuration

If not using render.yaml:

1. **Create Web Service**
   - New → Web Service
   - Connect repository
   - Configure:
     - **Name**: `customer-db-api`
     - **Root Directory**: Leave empty (repo root)
     - **Runtime**: Python 3
     - **Build Command**: `cd backend && pip install -r requirements.txt`
     - **Start Command**: `cd backend && uvicorn api_gateway.main:app --host 0.0.0.0 --port $PORT`

2. **Critical: Python Version**
   - Ensure `runtime.txt` exists at repo root with: `python-3.11.8`
   - If build fails with Python 3.14 error, click "Clear build cache & deploy"

3. **Set Environment Variables** (same as above)

### Troubleshooting

#### Issue: "pydantic-core" build fails with Rust/Cargo error

**Cause**: Render is using Python 3.14 instead of 3.11

**Solutions**:
1. Verify `runtime.txt` exists at repo root (not just in backend/)
2. Clear build cache: Settings → "Clear build cache & deploy"
3. Alternatively, set Root Directory to `backend` and update commands:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn api_gateway.main:app --host 0.0.0.0 --port $PORT`
   - Move or copy `runtime.txt` to `backend/runtime.txt`

#### Issue: CORS errors from frontend

**Cause**: `FRONTEND_URL` not set or incorrect

**Solution**: 
- Set `FRONTEND_URL` environment variable to your actual Vercel URL
- Format: `https://your-app.vercel.app` (no trailing slash)

#### Issue: Database connection fails

**Cause**: `DATABASE_URL` not set or incorrect format

**Solution**:
- For Supabase: Settings → Database → Connection string → URI
- Format: `postgresql://postgres.[project]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres`

---

## Frontend Deployment on Vercel

### Prerequisites
- Vercel account connected to GitHub

### Steps

1. **Deploy to Vercel**
   ```bash
   cd frontend
   npm install
   npx vercel
   ```

2. **Or use Vercel Dashboard**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - "Add New" → "Project"
   - Import `customer-database` repository
   - Configure:
     - **Framework Preset**: Next.js
     - **Root Directory**: `frontend`
     - **Build Command**: `npm run build`
     - **Output Directory**: `.next`

3. **Environment Variables**
   
   In Vercel project settings → Environment Variables:
   
   ```bash
   NEXT_PUBLIC_API_URL=https://customer-db-api.onrender.com
   NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
   ```

4. **Deploy**
   - Vercel auto-deploys on git push to main
   - Manual: `vercel --prod`

---

## Database Setup (Supabase)

### Already Configured
Your Supabase project: `pbbkfqitjsaquaelwbsu.supabase.co`

### Run Migrations

After deploying backend:

```bash
# Locally first (test)
cd backend
alembic upgrade head

# On Render (via SSH or script)
# Option 1: Add to build command
# Build Command: pip install -r requirements.txt && alembic upgrade head

# Option 2: Run migrations manually
# (SSH not available on Render free tier, so add to build command)
```

---

## Post-Deployment Checklist

- [ ] Backend health check: `https://your-api.onrender.com/health`
- [ ] Frontend loads: `https://your-app.vercel.app`
- [ ] CORS works: Check browser console for errors
- [ ] Database connected: Check logs in Render
- [ ] Environment variables set in both Render and Vercel
- [ ] Update `FRONTEND_URL` in Render with actual Vercel URL
- [ ] Update `NEXT_PUBLIC_API_URL` in Vercel with actual Render URL

---

## Monitoring

### Render
- View logs: Dashboard → Service → Logs
- Metrics: Dashboard → Service → Metrics

### Vercel
- View logs: Dashboard → Project → Deployments → [deployment] → Logs
- Analytics: Dashboard → Project → Analytics

### Supabase
- Database metrics: Dashboard → Database
- API logs: Dashboard → API Logs

---

## Updating

### Backend
```bash
git push origin main
# Render auto-deploys
```

### Frontend
```bash
git push origin main
# Vercel auto-deploys
```

---

## Costs

- **Render Free Tier**: 
  - Sleeps after 15 min inactivity
  - 750 hours/month
  - Wakes on request (~30s delay)

- **Vercel Free Tier**:
  - 100 GB bandwidth/month
  - Unlimited static requests
  - Serverless function execution limits

- **Supabase Free Tier**:
  - 500 MB database
  - 1 GB file storage
  - 50k monthly active users

---

## Production Recommendations

1. **Upgrade Render to Starter ($7/mo)**: No sleep, better performance
2. **Enable SSL**: Automatic on Render/Vercel
3. **Set up monitoring**: Sentry for error tracking
4. **Regular backups**: Supabase auto-backups on paid plan
5. **CDN**: Vercel includes automatically

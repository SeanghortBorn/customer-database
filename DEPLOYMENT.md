# Deployment Guide

This guide walks you through deploying your Customer Database application to production using:
- **Frontend:** Vercel
- **Backend:** Render
- **Database:** Supabase

---

## 📋 Prerequisites

1. GitHub account with this repository pushed
2. Accounts created on:
   - [Vercel](https://vercel.com) (free tier available)
   - [Render](https://render.com) (free tier available)
   - [Supabase](https://supabase.com) (free tier available)

---

## 🗄️ Step 1: Setup Supabase Database

### 1.1 Create a New Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Name:** customer-database
   - **Database Password:** (save this - you'll need it!)
   - **Region:** Choose closest to your users
4. Click **"Create new project"** (takes ~2 minutes)

### 1.2 Get Database Connection String

1. In your Supabase project, go to **Settings** → **Database**
2. Scroll to **Connection string** section
3. Copy the **Connection pooling** URI (starts with `postgresql://`)
4. Replace `[YOUR-PASSWORD]` with your database password
5. Save this URL - you'll need it for Render

**Example:**
```
postgresql://postgres.xxxxxxxxxxxx:your-password@aws-0-us-west-1.pooler.supabase.com:5432/postgres
```

### 1.3 Configure Database (Optional)

If you want to enable Row Level Security (RLS):
1. Go to **SQL Editor** in Supabase
2. You can run your migration files manually, or let the backend do it automatically

---

## 🚀 Step 2: Deploy Backend to Render

### 2.1 Create New Web Service

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your `customer-database` repository

### 2.2 Configure Web Service

Fill in the following settings:

| Field | Value |
|-------|-------|
| **Name** | `customer-database-backend` |
| **Region** | Choose closest to your users |
| **Branch** | `main` |
| **Root Directory** | `backend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` (or paid if needed) |

### 2.3 Add Environment Variables

Click **"Advanced"** → **"Add Environment Variable"** and add:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Your Supabase connection string |
| `SECRET_KEY` | Generate a random key (e.g., `openssl rand -hex 32`) |
| `FRONTEND_URL` | `https://your-app.vercel.app` (add this after deploying frontend) |
| `PYTHONUNBUFFERED` | `1` |

### 2.4 Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes)
3. Once deployed, copy your backend URL (e.g., `https://customer-database-backend.onrender.com`)
4. Test it: Visit `https://your-backend-url.onrender.com/health` - should return `{"status":"ok"}`

---

## 🌐 Step 3: Deploy Frontend to Vercel

### 3.1 Import Project

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. Select `customer-database` repository

### 3.2 Configure Project

| Field | Value |
|-------|-------|
| **Framework Preset** | `Next.js` (should auto-detect) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` (auto-detected) |
| **Output Directory** | `.next` (auto-detected) |

### 3.3 Add Environment Variables

Click **"Environment Variables"** and add:

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | Your Render backend URL (e.g., `https://customer-database-backend.onrender.com`) |

### 3.4 Deploy

1. Click **"Deploy"**
2. Wait for deployment (~2-3 minutes)
3. Once deployed, Vercel will give you a URL (e.g., `https://your-app.vercel.app`)
4. Visit your app and test it!

### 3.5 Update Backend CORS

Go back to Render and update the `FRONTEND_URL` environment variable with your Vercel URL:
- Go to Render Dashboard → Your Web Service → Environment
- Update `FRONTEND_URL` to `https://your-app.vercel.app`
- Render will automatically redeploy

---

## ✅ Step 4: Verify Deployment

### 4.1 Test Backend
```bash
curl https://your-backend.onrender.com/health
# Expected: {"status":"ok"}
```

### 4.2 Test Frontend
1. Visit `https://your-app.vercel.app`
2. Click **"Register"** and create an account
3. Try creating a person or property
4. Verify everything works!

### 4.3 Check Database
1. Go to Supabase Dashboard
2. Click **"Table Editor"**
3. You should see your tables (`organizations`, `users`, `people`, `properties`, etc.)
4. Verify data is being saved

---

## 🔧 Step 5: Configure Custom Domain (Optional)

### For Vercel (Frontend)
1. Go to your project → **Settings** → **Domains**
2. Add your custom domain (e.g., `app.yourdomain.com`)
3. Follow DNS configuration instructions

### For Render (Backend)
1. Go to your web service → **Settings** → **Custom Domain**
2. Add your API subdomain (e.g., `api.yourdomain.com`)
3. Follow DNS configuration instructions

---

## 🔐 Step 6: Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Update `DATABASE_URL` password to something strong
- [ ] Enable Supabase database backups (Settings → Database → Backups)
- [ ] Add your production domain to CORS settings if needed
- [ ] Set up SSL certificates (auto-configured by Vercel/Render)
- [ ] Review and restrict database permissions
- [ ] Enable Supabase Row Level Security (RLS) policies

---

## 📊 Monitoring & Logs

### Vercel Logs
- Dashboard → Your Project → **Deployments** → Click deployment → **Functions**

### Render Logs
- Dashboard → Your Service → **Logs** tab
- View real-time backend logs and errors

### Supabase Logs
- Dashboard → Your Project → **Logs** → **Postgres Logs**

---

## 🐛 Troubleshooting

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Check CORS settings in `backend/app/main.py`
- Ensure `FRONTEND_URL` is set in Render

### Database connection errors
- Verify `DATABASE_URL` format is correct
- Check Supabase project is active
- Ensure database password is correct
- Try connection pooler URL instead of direct connection

### Migrations not running
- SSH into Render: Dashboard → Service → **Shell**
- Run manually: `alembic upgrade head`
- Check logs for migration errors

### Free tier limitations
- **Supabase Free:** 500MB database, 1GB file storage
- **Render Free:** Service sleeps after 15 min inactivity (cold starts)
- **Vercel Free:** 100GB bandwidth/month, unlimited deployments

---

## 🔄 Continuous Deployment

Both Vercel and Render auto-deploy when you push to `main`:

```bash
git add .
git commit -m "Update feature"
git push origin main
```

- Vercel will auto-deploy frontend
- Render will auto-deploy backend
- Migrations run automatically on backend deploy

---

## 💰 Cost Estimate

### Free Tier (Good for testing/small apps)
- Supabase: Free
- Render: Free (with cold starts)
- Vercel: Free

### Paid Tier (Production apps)
- Supabase Pro: $25/month (8GB database, better performance)
- Render Starter: $7/month (always on, no cold starts)
- Vercel Pro: $20/month (team features, analytics)

**Total:** $0/month (free tier) or ~$52/month (paid tier)

---

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Render Documentation](https://render.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

---

## 🎉 You're Done!

Your app is now deployed to production! 

**Your URLs:**
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.onrender.com`
- Database: Managed by Supabase

Need help? Check the logs in each service's dashboard.

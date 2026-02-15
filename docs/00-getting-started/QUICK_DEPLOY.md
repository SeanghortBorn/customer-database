# Quick Deployment Reference

## 🚀 Deploy in 5 Minutes

### 1. Neon.tech Setup (2 min)
```bash
# Go to https://neon.tech
# Create project → Get pooled connection string (port 6543)
# Copy: postgresql://user:pass@hostname.neon.tech:6543/neondb?sslmode=require
```

### 2. Backend Environment (Render)
```env
DATABASE_URL=postgresql://...@hostname.neon.tech:6543/neondb?sslmode=require
JWT_SECRET_KEY=<generate-long-random-string-here>
REDIS_URL=redis://...
FRONTEND_URL=https://your-frontend.vercel.app
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Frontend Environment (Vercel)
```env
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com/api/v1
```

### 4. Run Migrations
```bash
cd backend
alembic upgrade head
```

### 5. Test It! ✅
- Visit frontend URL
- Sign up a new user
- Create a workspace
- Done!

## 📋 Environment Variables Checklist

### Backend (4 required)
- [ ] `DATABASE_URL` - Neon.tech connection string (pooled, port 6543)
- [ ] `JWT_SECRET_KEY` - Random string for JWT signing
- [ ] `REDIS_URL` - Redis connection (optional for now)
- [ ] `FRONTEND_URL` - Your Vercel frontend URL

### Frontend (1 required)
- [ ] `NEXT_PUBLIC_API_URL` - Your Render backend URL

## ⚠️ Common Issues

### "Database connection failed"
- ✅ Use pooled connection (port **6543**, not 5432)
- ✅ Include `?sslmode=require` at the end
- ✅ Verify URL is correct from Neon.tech dashboard

### "JWT validation failed"
- ✅ Check `JWT_SECRET_KEY` is set
- ✅ Don't change the secret after deploying
- ✅ Verify it's the same in all instances

### "CORS error"
- ✅ Set correct `FRONTEND_URL` in backend
- ✅ No trailing slash in URLs

## 🔗 Quick Links

- Neon.tech: https://neon.tech
- Render: https://render.com
- Vercel: https://vercel.com
- Full Guide: See MIGRATION_SUMMARY.md

## 📞 Need Help?

See detailed guides:
- `SETUP.md` - Complete setup instructions
- `MIGRATION_SUMMARY.md` - Full migration details
- `docs/05-operations/NEON_DATABASE_SETUP.md` - Neon.tech guide

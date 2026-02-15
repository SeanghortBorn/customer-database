# Neon.tech Database Setup Guide

## Overview

This guide will help you set up your Neon.tech PostgreSQL database for the Customer Database System.

## What is Neon.tech?

Neon.tech is a serverless PostgreSQL database platform that offers:
- **Instant provisioning**: Database ready in seconds
- **Autoscaling**: Scales to zero when not in use
- **Branching**: Create database branches like Git
- **Built-in connection pooling**: Optimized for serverless
- **Free tier**: Generous limits for development

## Setup Steps

### 1. Create a Neon.tech Account

1. Go to [https://neon.tech](https://neon.tech)
2. Sign up with GitHub, Google, or email
3. Verify your email if required

### 2. Create a New Project

1. Click **"Create Project"** or **"New Project"**
2. Choose a project name (e.g., "customer-database")
3. Select a region closest to your users
4. Click **"Create Project"**

Your database will be ready in a few seconds!

### 3. Get Your Connection String

After project creation:

1. You'll see the connection details page
2. Look for **"Connection string"** section
3. You'll see different connection strings:
   - **Direct connection** (port 5432)
   - **Pooled connection** (port 6543) - **Use this for Render!**

**For Render deployment, always use the pooled connection string.**

Example connection string:
```
postgresql://username:password@ep-cool-recipe-123456.us-east-2.aws.neon.tech:6543/neondb?sslmode=require
```

### 4. Configure Your Backend

#### Local Development

1. Create/edit `backend/.env`:
```env
DATABASE_URL=postgresql://username:password@your-hostname.neon.tech:6543/neondb?sslmode=require
JWT_SECRET_KEY=your-secret-key-change-this-to-random-string
REDIS_URL=redis://localhost:6379
FRONTEND_URL=http://localhost:3000
```

2. Run migrations:
```bash
cd backend
alembic upgrade head
```

#### Production (Render)

1. Go to your Render dashboard
2. Select your backend service
3. Go to **Environment** tab
4. Add/update environment variable:
   - Key: `DATABASE_URL`
   - Value: Your Neon.tech pooled connection string

## Important Notes

### Connection Pooling

- **For Render**: Always use port **6543** (pooled connection)
- **For local dev**: Either port works, but 6543 is recommended
- Connection pooling prevents "too many connections" errors

### SSL Mode

Neon.tech requires SSL. Always include `?sslmode=require` in your connection string.

### Database Branching (Optional)

Neon.tech offers Git-like branching for databases:

1. Go to your project in Neon.tech
2. Click **"Branches"** tab
3. Create a new branch for testing/staging
4. Each branch has its own connection string

This is useful for:
- Testing migrations before production
- Having separate staging/production databases
- Safe experimentation

## Troubleshooting

### Connection Refused

- **Check region**: Ensure your Render service is in a compatible region
- **Use pooled connection**: Port 6543 instead of 5432
- **Verify SSL**: Include `?sslmode=require` in connection string

### Too Many Connections

- **Use connection pooling**: Port 6543 (pooled connection)
- **Check your code**: Ensure database connections are properly closed
- **Review pool settings**: Check `pool_size` and `max_overflow` in `database.py`

### Slow Queries

- **Check indexes**: Add indexes for frequently queried columns
- **Optimize queries**: Use SQLAlchemy's query optimization features
- **Monitor performance**: Use Neon.tech's dashboard to identify slow queries

### Database Not Found

- **Check database name**: Default is usually `neondb`
- **Verify connection string**: Copy it exactly from Neon.tech dashboard
- **Check project**: Ensure you're looking at the correct project

## Monitoring and Maintenance

### View Metrics

1. Go to your Neon.tech project
2. Click **"Monitoring"** tab
3. View:
   - Connection count
   - Query performance
   - Storage usage
   - Autoscaling activity

### Backups

Neon.tech automatically handles backups:
- **Point-in-time recovery**: Restore to any point within retention period
- **Free tier**: 7 days retention
- **Paid tiers**: Up to 30 days retention

To restore:
1. Go to **"Branches"** tab
2. Click **"Restore"**
3. Select the timestamp
4. Create a new branch from that point

## Best Practices

1. **Use environment variables**: Never hardcode connection strings
2. **Use pooled connections**: Port 6543 for production
3. **Enable SSL**: Always include `?sslmode=require`
4. **Monitor usage**: Check your usage in Neon.tech dashboard
5. **Use branches**: Create separate branches for staging/testing
6. **Close connections**: Ensure all database connections are properly closed

## Migration from Supabase

If you're migrating from Supabase:

1. Export your data from Supabase (if any)
2. Create Neon.tech project
3. Update `DATABASE_URL` in your environment
4. Run migrations: `alembic upgrade head`
5. Import data if needed
6. Test your application
7. Update production environment variables

## Free Tier Limits

Neon.tech free tier includes:
- 10 GB storage
- Unlimited compute hours (scales to zero)
- 1 concurrent project
- Connection pooling
- Autoscaling

Perfect for development and small production deployments!

## Support

- **Documentation**: https://neon.tech/docs
- **Discord**: https://discord.gg/neon
- **GitHub**: https://github.com/neondatabase

---

**Next Steps:**
- [Backend Setup](../../SETUP.md)
- [Deployment Guide](./PRODUCTION_VERIFICATION.md)
- [Troubleshooting](./INDEX.md)

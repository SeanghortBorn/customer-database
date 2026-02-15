# Customer Database System - Setup Guide

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL database (Neon.tech recommended)
- Conda (recommended) or virtualenv

## Backend Setup

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create and activate Conda environment
```bash
conda create -n cds python=3.11
conda activate cds
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=postgresql://user:password@hostname.neon.tech:6543/neondb?sslmode=require
JWT_SECRET_KEY=your-secret-key-change-in-production
FRONTEND_URL=http://localhost:3000
REDIS_URL=redis://localhost:6379
```

### 5. Run database migrations
```bash
alembic upgrade head
```

### 6. Start the backend server
```bash
# Development
python api_gateway/main.py

# Or with uvicorn
uvicorn api_gateway.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## Frontend Setup

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment variables
Create a `.env.local` file in the `frontend` directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

For production, set this to your Render backend URL.

### 4. Start the development server
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Neon.tech Database Setup

### 1. Create a Neon.tech project
Go to [neon.tech](https://neon.tech) and create a new project

### 2. Get your connection string
- Go to your project dashboard
- Click on "Connection Details"
- Copy the connection string (it will look like: `postgresql://username:password@hostname.neon.tech:5432/database`)

### 3. Configure your backend
Add the connection string to your `backend/.env` file as `DATABASE_URL`

### 4. Run migrations
```bash
cd backend
alembic upgrade head
```

This will create all necessary tables in your Neon.tech database.

## Testing the Application

### 1. Sign up for an account
Navigate to http://localhost:3000 and click "Sign Up"

### 2. Create a workspace
After logging in, click "Create Workspace"

### 3. Create a list
Inside a workspace, click "Create List"

### 4. Add columns
In a list, click "Add Column" to define your data structure

### 5. Add items
Once you have columns, click "Add Item" to start adding data

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── api_gateway/          # Main FastAPI application
├── services/             # Domain services
│   ├── workspace/       # Workspace & membership logic
│   ├── list/            # List & column logic
│   ├── item/            # Item & comment logic
│   ├── relationship/    # Relationship logic
│   └── audit/           # Audit log queries
├── shared/              # Shared code
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── database.py      # Database connection
│   └── auth.py          # Auth middleware
├── alembic/             # Database migrations
└── tests/               # Test files

frontend/
├── app/                 # Next.js 13+ app directory
│   ├── login/          # Login page
│   ├── signup/         # Signup page
│   ├── dashboard/      # Dashboard with workspaces
│   └── workspace/      # Workspace and list pages
└── lib/                # Shared utilities
    ├── api.ts          # API client
    ├── auth.ts         # Authentication service
    └── utils.ts        # Helper functions
```

## Troubleshooting

### Backend won't start
- Check DATABASE_URL is correct
- Ensure database is accessible (Neon.tech should always be up)
- Verify migrations are up to date: `alembic upgrade head`
- Check JWT_SECRET_KEY is set

### Frontend can't connect to API
- Verify NEXT_PUBLIC_API_URL in .env.local
- Check backend is running on port 8000
- Check browser console for CORS errors

### Authentication not working
- Verify JWT_SECRET_KEY is set in backend .env
- Check that user exists in database
- Ensure passwords meet minimum requirements (6+ characters)
- Check browser console and backend logs for errors

## Development Commands

### Backend
```bash
# Run tests
pytest tests/ -v

# Create a new migration
alembic revision --autogenerate -m "description"

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current
```

### Frontend
```bash
# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build

# Start production server
npm start
```

## Production Deployment

### Backend (Render)
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set environment variables in Render dashboard
4. Deploy

### Frontend (Vercel)
1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push to main

### Database (Neon.tech)
- Use Neon.tech managed PostgreSQL (recommended)
- Free tier includes 10GB storage and connection pooling
- See docs/05-operations/NEON_DATABASE_SETUP.md for details

## Support

For issues and questions, refer to the documentation in `/docs/` or create an issue on GitHub.

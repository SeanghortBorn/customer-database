# Customer Database System - Setup Guide

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL database (or Supabase account)
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
DATABASE_URL=postgresql://user:password@localhost:5432/customer_db
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
FRONTEND_URL=http://localhost:3000
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
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### 4. Start the development server
```bash
npm run dev
```

The app will be available at http://localhost:3000

## Supabase Setup

### 1. Create a Supabase project
Go to [supabase.com](https://supabase.com) and create a new project

### 2. Get your credentials
- Project URL: Settings → API → Project URL
- Anon Key: Settings → API → Project API keys → anon public

### 3. Enable Email Auth
- Go to Authentication → Providers
- Enable Email provider
- Configure email templates (optional)

### 4. Database Connection
Use the Supabase connection string for your DATABASE_URL, or use an external PostgreSQL database.

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
    ├── supabase.ts     # Supabase client
    └── utils.ts        # Helper functions
```

## Troubleshooting

### Backend won't start
- Check DATABASE_URL is correct
- Ensure PostgreSQL is running
- Verify migrations are up to date: `alembic upgrade head`

### Frontend can't connect to API
- Verify NEXT_PUBLIC_API_URL in .env.local
- Check backend is running on port 8000
- Check browser console for CORS errors

### Authentication not working
- Verify Supabase credentials are correct
- Check email auth is enabled in Supabase
- Ensure SUPABASE_URL and SUPABASE_ANON_KEY match in both backend and frontend

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

### Database (Supabase)
- Use Supabase managed PostgreSQL
- Or deploy your own PostgreSQL instance

## Support

For issues and questions, refer to the documentation in `/docs/` or create an issue on GitHub.

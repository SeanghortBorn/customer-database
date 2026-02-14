#!/bin/bash
# Deployment Readiness Checker

echo "==================================="
echo "   Deployment Readiness Check"
echo "==================================="
echo ""

# Check if Git repo is initialized
echo "✓ Checking Git repository..."
if [ -d .git ]; then
    echo "  ✅ Git repository found"
    CURRENT_BRANCH=$(git branch --show-current)
    echo "  📍 Current branch: $CURRENT_BRANCH"
else
    echo "  ❌ No Git repository found. Run: git init"
    exit 1
fi

# Check if remote is set
echo ""
echo "✓ Checking Git remote..."
REMOTE=$(git remote -v | grep origin | head -1)
if [ -n "$REMOTE" ]; then
    echo "  ✅ Remote configured: $REMOTE"
else
    echo "  ⚠️  No remote configured. Add GitHub remote:"
    echo "     git remote add origin https://github.com/YOUR_USERNAME/customer-database.git"
fi

# Check if code is committed
echo ""
echo "✓ Checking uncommitted changes..."
if git diff-index --quiet HEAD --; then
    echo "  ✅ No uncommitted changes"
else
    echo "  ⚠️  You have uncommitted changes. Commit them:"
    echo "     git add ."
    echo "     git commit -m 'Prepare for deployment'"
fi

# Check required files
echo ""
echo "✓ Checking deployment configuration files..."
FILES=(
    "vercel.json"
    "render.yaml"
    "DEPLOYMENT.md"
    "frontend/package.json"
    "backend/requirements.txt"
    "backend/alembic.ini"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file not found"
    fi
done

# Check backend dependencies
echo ""
echo "✓ Checking backend requirements..."
if grep -q "fastapi" backend/requirements.txt; then
    echo "  ✅ FastAPI found in requirements.txt"
else
    echo "  ❌ FastAPI not found in requirements.txt"
fi

if grep -q "psycopg2" backend/requirements.txt || grep -q "psycopg2-binary" backend/requirements.txt; then
    echo "  ✅ PostgreSQL driver found"
else
    echo "  ⚠️  PostgreSQL driver (psycopg2-binary) not found"
fi

# Check frontend dependencies
echo ""
echo "✓ Checking frontend dependencies..."
if grep -q "next" frontend/package.json; then
    echo "  ✅ Next.js found in package.json"
else
    echo "  ❌ Next.js not found in package.json"
fi

# Summary
echo ""
echo "==================================="
echo "        Next Steps"
echo "==================================="
echo ""
echo "1. 📖 Read DEPLOYMENT.md for detailed instructions"
echo ""
echo "2. 🗄️  Create Supabase project:"
echo "   → https://app.supabase.com"
echo ""
echo "3. 🚀 Deploy backend to Render:"
echo "   → https://dashboard.render.com"
echo ""
echo "4. 🌐 Deploy frontend to Vercel:"
echo "   → https://vercel.com/new"
echo ""
echo "5. ✅ Test your deployment!"
echo ""
echo "==================================="

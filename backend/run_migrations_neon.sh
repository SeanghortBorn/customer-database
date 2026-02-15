#!/bin/bash
# Run database migrations on Neon.tech database
# Usage: ./run_migrations_neon.sh

echo "🔧 Running database migrations on Neon.tech..."
echo ""
echo "Make sure you have set DATABASE_URL to your Neon connection string in .env"
echo ""

# Check if alembic is installed
if ! command -v alembic &> /dev/null; then
    echo "❌ Alembic not found. Installing..."
    pip install alembic
fi

# Navigate to backend directory
cd "$(dirname "$0")"

# Run migrations
echo "📦 Running migrations..."
alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migrations completed successfully!"
    echo ""
    echo "Next steps:"
    echo "1. Update Render environment variables with Neon DATABASE_URL"
    echo "2. Redeploy your backend on Render"
else
    echo "❌ Migration failed. Check the error above."
    echo ""
    echo "Common fixes:"
    echo "- Verify DATABASE_URL is correct in .env"
    echo "- Make sure you're using the pooled connection from Neon"
    echo "- Check that the database is accessible"
fi

#!/usr/bin/env python3
"""Test database connection and run migrations"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL environment variable not set")
    print("Please set DATABASE_URL in your .env file")
    print("Example: DATABASE_URL=postgresql://user:password@hostname:5432/database")
    exit(1)

print("Testing database connection...")
print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'hidden'}")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        
        # Check if tables exist
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result]
        
        if tables:
            print(f"\n✅ Found {len(tables)} existing tables:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("\n⚠️  No tables found yet. You need to run migrations:")
            print("   cd backend && alembic upgrade head")
            
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTroubleshooting:")
    print("1. Check your DATABASE_URL is correct")
    print("2. Ensure your database is accessible from this network")
    print("3. Verify your credentials are correct")

#!/usr/bin/env python3
"""Test database connection and run migrations"""
import os
from sqlalchemy import create_engine, text

# URL-encoded password for special characters
DATABASE_URL = "postgresql://postgres:-sA%21%3FWN%3E%2C025@db.pbbkfqitjsaquaelwbsu.supabase.co:5432/postgres"

print("Testing database connection...")
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
            print("\n⚠️  No tables found yet. You need to run migrations.")
            
except Exception as e:
    print(f"❌ Connection failed: {e}")

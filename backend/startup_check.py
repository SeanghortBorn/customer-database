#!/usr/bin/env python3
"""
Startup checks for backend deployment
Run this to verify environment before starting the server
"""
import os
import sys
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

def check_env_var(name, required=True):
    """Check if environment variable is set"""
    value = os.getenv(name)
    if value:
        # Show partial value for security
        if 'SECRET' in name or 'PASSWORD' in name or 'KEY' in name:
            display = f"{value[:10]}..." if len(value) > 10 else "***"
        elif 'URL' in name:
            # Show host part only
            if '@' in value:
                parts = value.split('@')
                display = f"***@{parts[1]}" if len(parts) > 1 else "***"
            else:
                display = value
        else:
            display = value[:50] + "..." if len(value) > 50 else value
        
        print(f"  ✅ {name}: {display}")
        return True
    else:
        if required:
            print(f"  ❌ {name}: NOT SET (REQUIRED)")
            return False
        else:
            print(f"  ⚠️  {name}: NOT SET (optional)")
            return True

def check_database_connection():
    """Test database connection"""
    try:
        from sqlalchemy import create_engine, text
        DATABASE_URL = os.getenv('DATABASE_URL')
        if not DATABASE_URL:
            print("  ❌ Cannot test database: DATABASE_URL not set")
            return False
        
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("  ✅ Database connection successful")
        return True
    except Exception as e:
        print(f"  ❌ Database connection failed: {str(e)}")
        return False

def main():
    print("=" * 60)
    print("🔍 Backend Startup Checks")
    print("=" * 60)
    
    all_ok = True
    
    print("\n📋 Environment Variables:")
    all_ok &= check_env_var("DATABASE_URL", required=True)
    all_ok &= check_env_var("JWT_SECRET_KEY", required=True)
    all_ok &= check_env_var("FRONTEND_URL", required=False)
    all_ok &= check_env_var("REDIS_URL", required=False)
    
    print("\n🗄️  Database Connection:")
    all_ok &= check_database_connection()
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✅ All checks passed! Ready to start server.")
        print("=" * 60)
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())

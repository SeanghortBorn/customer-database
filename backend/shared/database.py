from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from shared.base import Base

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Validate DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Clean up the URL (remove any accidental prefixes or quotes)
DATABASE_URL = DATABASE_URL.strip().strip("'").strip('"')
if DATABASE_URL.startswith('psql '):
    DATABASE_URL = DATABASE_URL[5:].strip().strip("'").strip('"')

# Configure connection pool for cloud environments (Render)
# pool_pre_ping: Check connection health before using
# pool_recycle: Recycle connections every 5 minutes (300 seconds)
# pool_size: Number of permanent connections
# max_overflow: Additional connections when needed
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=10,
    connect_args={"connect_timeout": 10}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#!/bin/bash
# Test script to validate Supabase connection strings
# Run this locally to verify connection string formats

echo "Testing Supabase Connection Strings..."
echo ""

# Your Supabase details
PROJECT_REF="pbbkfqitjsaquaelwbsu"
PASSWORD="-sA!?WN>,025"
PASSWORD_ENCODED="-sA%21%3FWN%3E%2C025"

echo "=== Option 1: AWS Pooler (Transaction Mode) ==="
echo "postgresql://postgres.$PROJECT_REF:$PASSWORD_ENCODED@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
echo ""

echo "=== Option 2: AWS Pooler with simple user (Transaction Mode) ==="  
echo "postgresql://postgres.${PROJECT_REF}:$PASSWORD_ENCODED@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
echo ""

echo "=== Option 3: AWS Pooler (Session Mode) ==="
echo "postgresql://postgres.${PROJECT_REF}:$PASSWORD_ENCODED@aws-0-us-east-1.pooler.supabase.com:5432/postgres"
echo ""

echo "=== Option 4: Direct with pooler port ==="
echo "postgresql://postgres:$PASSWORD_ENCODED@db.$PROJECT_REF.supabase.co:6543/postgres"
echo ""

echo "==========================================
"
echo "To test locally (requires direct access):"
echo ""
echo "cd backend"
echo "export DATABASE_URL='<connection-string-above>'"
echo "python -c 'from shared.database import engine; engine.connect(); print(\"✓ Connected successfully!\")'"
echo ""
echo "==========================================
"
echo "For Render, copy one of the connection strings above into:"
echo "Render Dashboard → customer-db-api → Environment → DATABASE_URL"

"""Seed the DB with a default organization and user (development only)."""
from app.db.session import engine, SessionLocal
from app.db import models
from app.core.security import get_password_hash


def seed():
    db = SessionLocal()
    try:
        org = db.query(models.Organization).filter(models.Organization.name == 'Zoneer Demo').first()
        if not org:
            org = models.Organization(name='Zoneer Demo')
            db.add(org)
            db.commit()
            db.refresh(org)
        user = db.query(models.User).filter(models.User.email == 'admin@example.com').first()
        if not user:
            user = models.User(org_id=org.id, email='admin@example.com', name='Admin', role='owner', hashed_password=get_password_hash('password'))
            db.add(user)
            db.commit()
        print('Seeded org:', org.id)
    finally:
        db.close()


if __name__ == '__main__':
    seed()

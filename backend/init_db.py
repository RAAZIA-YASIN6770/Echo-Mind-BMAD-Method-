"""
============================================
EchoMind AI - Database Initialization
Sprint 1: Create Tables for Users and Safety Logs
============================================

This script creates the initial database schema.
Run this after setting up PostgreSQL.

Usage:
    python init_db.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from models import Base, User, UserProfile, SafetyLog
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_database():
    """
    Initialize database schema
    Creates all tables defined in models.py
    """
    try:
        logger.info("=" * 60)
        logger.info("🗄️  EchoMind AI - Database Initialization")
        logger.info("=" * 60)
        
        # Create engine
        # Note: Using sync engine for initialization (async will be used in production)
        db_url = settings.DATABASE_URL.replace('+asyncpg', '')  # Remove async driver for init
        logger.info(f"📡 Connecting to database...")
        logger.info(f"   URL: {db_url.split('@')[1] if '@' in db_url else 'localhost'}")  # Hide credentials
        
        engine = create_engine(
            db_url,
            echo=settings.DEBUG,
            pool_pre_ping=True
        )
        
        # Test connection
        with engine.connect() as conn:
            logger.info("✅ Database connection successful")
        
        # Create all tables
        logger.info("\n📋 Creating tables...")
        logger.info("   - users")
        logger.info("   - user_profiles")
        logger.info("   - safety_logs")
        
        Base.metadata.create_all(engine)
        
        logger.info("\n✅ Database schema created successfully!")
        logger.info("=" * 60)
        
        # Print table info
        logger.info("\n📊 Created Tables:")
        for table_name in Base.metadata.tables.keys():
            table = Base.metadata.tables[table_name]
            logger.info(f"\n   Table: {table_name}")
            logger.info(f"   Columns: {len(table.columns)}")
            for column in table.columns:
                logger.info(f"      - {column.name}: {column.type}")
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Database initialization complete!")
        logger.info("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"\n❌ Database initialization failed: {str(e)}")
        logger.error("   Please check your database connection settings in .env")
        return False


def drop_all_tables():
    """
    Drop all tables (DANGEROUS - use only in development)
    """
    logger.warning("⚠️  WARNING: This will drop all tables!")
    confirm = input("Type 'YES' to confirm: ")
    
    if confirm != "YES":
        logger.info("❌ Aborted")
        return
    
    try:
        db_url = settings.DATABASE_URL.replace('+asyncpg', '')
        engine = create_engine(db_url)
        
        logger.info("🗑️  Dropping all tables...")
        Base.metadata.drop_all(engine)
        logger.info("✅ All tables dropped")
        
    except Exception as e:
        logger.error(f"❌ Error dropping tables: {str(e)}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="EchoMind AI Database Initialization")
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop all tables before creating (DANGEROUS)"
    )
    
    args = parser.parse_args()
    
    if args.drop:
        drop_all_tables()
    
    init_database()

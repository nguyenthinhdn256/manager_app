# Kết nối và cấu hình database
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
import sqlite3
import os
from utils.logger import logger

# Khởi tạo SQLAlchemy instance
db = SQLAlchemy()

def init_db():
    """Khởi tạo database và tạo các bảng"""
    try:
        # Debug: in ra database URI
        from flask import current_app
        logger.info(f"Database URI: {current_app.config['SQLALCHEMY_DATABASE_URI']}")
        
        # Tạo tất cả bảng
        db.create_all()
        logger.info("✅ Database tables created successfully")
        
        # Tạo dữ liệu mẫu nếu cần
        create_sample_data()
        
    except Exception as e:
        logger.error(f"❌ Error initializing database: {str(e)}")
        raise

def create_sample_data():
    """Tạo dữ liệu mẫu cho development"""
    from config.env import is_development
    
    if not is_development():
        return
    
    try:
        from models.User import User
        from models.AppData import AppData
        import bcrypt
        
        # Kiểm tra xem đã có dữ liệu chưa
        if User.query.first():
            logger.info("Sample data already exists")
            return
        
        # Tạo admin user
        admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password=admin_password
        )
        admin_user.save()
        
        # Tạo test user
        test_password = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        test_user = User(
            username='testuser',
            email='test@example.com',
            password=test_password
        )
        test_user.save()
        
        # Tạo sample data cho test user
        sample_data = [
            {
                'type': 'note',
                'title': 'Welcome Note',
                'content': 'This is a sample note to test the app'
            },
            {
                'type': 'task',
                'title': 'Sample Task',
                'content': 'Complete the backend development'
            },
            {
                'type': 'memo',
                'title': 'Important Memo',
                'content': 'Remember to test all API endpoints'
            }
        ]
        
        for data in sample_data:
            app_data = AppData(
                user_id=test_user.id,
                type=data['type'],
                title=data['title'],
                content=data['content']
            )
            app_data.save()
        
        logger.info("✅ Sample data created successfully")
        logger.info("📝 Admin user: admin / admin123")
        logger.info("📝 Test user: testuser / test123")
        
    except Exception as e:
        logger.error(f"❌ Error creating sample data: {str(e)}")

def configure_sqlite():
    """Cấu hình đặc biệt cho SQLite"""
    
    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        """Set SQLite pragmas for better performance"""
        if 'sqlite' in str(dbapi_connection):
            cursor = dbapi_connection.cursor()
            
            # Enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys=ON")
            
            # Set journal mode to WAL for better concurrency
            cursor.execute("PRAGMA journal_mode=WAL")
            
            # Set synchronous mode
            cursor.execute("PRAGMA synchronous=NORMAL")
            
            # Set cache size (negative value = KB)
            cursor.execute("PRAGMA cache_size=-64000")  # 64MB
            
            # Set temp store to memory
            cursor.execute("PRAGMA temp_store=MEMORY")
            
            cursor.close()

def backup_database(backup_path=None):
    """Backup SQLite database"""
    from config.env import Config
    
    if 'sqlite' not in Config.SQLALCHEMY_DATABASE_URI:
        logger.warning("Database backup only supported for SQLite")
        return False
    
    try:
        # Extract database path from URI
        db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        
        if not os.path.exists(db_path):
            logger.error(f"Database file not found: {db_path}")
            return False
        
        # Generate backup filename if not provided
        if not backup_path:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = f"backup_database_{timestamp}.db"
        
        # Create backup directory if needed
        backup_dir = os.path.dirname(backup_path)
        if backup_dir and not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # Perform backup
        import shutil
        shutil.copy2(db_path, backup_path)
        
        logger.info(f"✅ Database backed up to: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database backup failed: {str(e)}")
        return False

def restore_database(backup_path):
    """Restore SQLite database from backup"""
    from config.env import Config
    
    if 'sqlite' not in Config.SQLALCHEMY_DATABASE_URI:
        logger.warning("Database restore only supported for SQLite")
        return False
    
    try:
        if not os.path.exists(backup_path):
            logger.error(f"Backup file not found: {backup_path}")
            return False
        
        # Extract database path from URI
        db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        
        # Backup current database before restore
        if os.path.exists(db_path):
            backup_current = f"{db_path}.backup_before_restore"
            import shutil
            shutil.copy2(db_path, backup_current)
            logger.info(f"Current database backed up to: {backup_current}")
        
        # Restore from backup
        import shutil
        shutil.copy2(backup_path, db_path)
        
        logger.info(f"✅ Database restored from: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database restore failed: {str(e)}")
        return False

def get_database_info():
    """Get database information"""
    try:
        from config.env import Config
        
        # Basic info
        info = {
            'database_uri': Config.SQLALCHEMY_DATABASE_URI,
            'database_type': 'sqlite' if 'sqlite' in Config.SQLALCHEMY_DATABASE_URI else 'other',
            'track_modifications': Config.SQLALCHEMY_TRACK_MODIFICATIONS
        }
        
        # SQLite specific info
        if 'sqlite' in Config.SQLALCHEMY_DATABASE_URI:
            db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
            if os.path.exists(db_path):
                stat = os.stat(db_path)
                info.update({
                    'database_size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'last_modified': stat.st_mtime
                })
        
        # Table info
        try:
            with db.engine.connect() as conn:
                if 'sqlite' in Config.SQLALCHEMY_DATABASE_URI:
                    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
                    tables = [row[0] for row in result]
                    info['tables'] = tables
                    info['table_count'] = len(tables)
        except Exception:
            pass
        
        return info
        
    except Exception as e:
        logger.error(f"Error getting database info: {str(e)}")
        return {}

def check_database_health():
    """Check database health"""
    try:
        # Test connection
        with db.engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        # Check if tables exist
        from models.User import User
        from models.AppData import AppData
        
        user_count = User.query.count()
        data_count = AppData.query.count()
        
        health_info = {
            'status': 'healthy',
            'connection': 'ok',
            'tables_exist': True,
            'user_count': user_count,
            'data_count': data_count
        }
        
        logger.info(f"Database health check: {health_info}")
        return health_info
        
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return {
            'status': 'unhealthy',
            'connection': 'failed',
            'error': str(e)
        }

def cleanup_old_data(days=30):
    """Cleanup dữ liệu cũ (có thể chạy định kỳ)"""
    try:
        from datetime import datetime, timedelta
        from models.AppData import AppData
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Query old data
        old_data = AppData.query.filter(AppData.created_at < cutoff_date).all()
        
        deleted_count = 0
        for item in old_data:
            db.session.delete(item)
            deleted_count += 1
        
        db.session.commit()
        
        logger.info(f"Cleaned up {deleted_count} old data items (older than {days} days)")
        return deleted_count
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error cleaning up old data: {str(e)}")
        return 0

def optimize_database():
    """Optimize database performance"""
    try:
        from config.env import Config
        
        if 'sqlite' in Config.SQLALCHEMY_DATABASE_URI:
            with db.engine.connect() as conn:
                # Run VACUUM to optimize SQLite
                conn.execute(text("VACUUM"))
                
                # Analyze tables for better query planning
                conn.execute(text("ANALYZE"))
            
            logger.info("✅ Database optimized successfully")
            return True
        else:
            logger.info("Database optimization only supported for SQLite")
            return False
            
    except Exception as e:
        logger.error(f"❌ Database optimization failed: {str(e)}")
        return False

# Configure SQLite on import
configure_sqlite()

# Export functions
__all__ = [
    'db', 'init_db', 'backup_database', 'restore_database', 
    'get_database_info', 'check_database_health', 'cleanup_old_data', 'optimize_database'
]
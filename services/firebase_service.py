# Service tích hợp Firebase (tùy chọn) - COMPLETELY DISABLED FOR NOW
import os
import json

# Import logger safely
try:
    from utils.logger import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

# Completely disable Firebase to avoid all import issues
FIREBASE_AVAILABLE = False

# Mock all Firebase modules to prevent errors
class MockFirebase:
    def __init__(self):
        pass
    
    def __getattr__(self, name):
        return lambda *args, **kwargs: None

firebase_admin = MockFirebase()
credentials = MockFirebase()
firestore = MockFirebase()
messaging = MockFirebase()
auth = MockFirebase()

logger.info("Firebase features completely disabled - no import attempts")

class FirebaseService:
    """Service tích hợp với Firebase - DISABLED"""
    
    def __init__(self):
        self.app = None
        self.db = None
        self.is_initialized = False
        logger.info("FirebaseService initialized in disabled mode")
    
    def is_available(self):
        """Kiểm tra Firebase có sẵn sàng không"""
        return False
    
    def sync_to_firestore(self, user_id, data):
        """Đồng bộ dữ liệu lên Firestore - DISABLED"""
        logger.info(f"Firebase sync disabled - would sync user {user_id}")
        return False
    
    def get_from_firestore(self, user_id):
        """Lấy dữ liệu từ Firestore - DISABLED"""
        logger.info(f"Firebase get disabled - would get data for user {user_id}")
        return None
    
    def send_push_notification(self, user_token, title, body, data=None):
        """Gửi push notification - DISABLED"""
        logger.info(f"Push notification disabled - would send: {title}")
        return False
    
    def send_data_update_notification(self, user_token, data_type, action):
        """Gửi thông báo cập nhật dữ liệu - DISABLED"""
        logger.info(f"Data notification disabled - would notify: {action} {data_type}")
        return False
    
    def create_custom_token(self, user_id):
        """Tạo custom token cho user - DISABLED"""
        logger.info(f"Custom token disabled - would create for user {user_id}")
        return None
    
    def backup_user_data(self, user_id, data):
        """Backup dữ liệu user - DISABLED"""
        logger.info(f"User backup disabled - would backup user {user_id}")
        return False
    
    def get_user_backup(self, user_id):
        """Lấy backup dữ liệu user - DISABLED"""
        logger.info(f"Get backup disabled - would get backup for user {user_id}")
        return None
    
    def cleanup_old_backups(self, days_old=30):
        """Dọn dẹp backup cũ - DISABLED"""
        logger.info(f"Cleanup disabled - would clean backups older than {days_old} days")
        return False

# Singleton instance
firebase_service = FirebaseService()
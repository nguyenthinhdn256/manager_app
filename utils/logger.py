# Các hàm tiện ích chung
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    """Custom logger cho ứng dụng"""
    
    def __init__(self, name='backend_app'):
        self.logger = logging.getLogger(name)
        self.setup_logger()
    
    def setup_logger(self):
        """Thiết lập cấu hình logger"""
        
        # Nếu logger đã được setup thì không setup lại
        if self.logger.handlers:
            return
        
        # Set level
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        self.logger.setLevel(getattr(logging, log_level, logging.INFO))
        
        # Tạo formatter
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (nếu cần)
        if os.getenv('LOG_TO_FILE', 'False').lower() == 'true':
            self.setup_file_handler(formatter)
        
        # Ngăn log duplicate
        self.logger.propagate = False
    
    def setup_file_handler(self, formatter):
        """Thiết lập file handler cho logging"""
        try:
            # Tạo thư mục logs nếu chưa có
            log_dir = 'logs'
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            # File handler với rotation
            log_file = os.path.join(log_dir, 'app.log')
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            
            # Error file handler riêng
            error_file = os.path.join(log_dir, 'error.log')
            error_handler = RotatingFileHandler(
                error_file,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            self.logger.addHandler(error_handler)
            
        except Exception as e:
            self.logger.warning(f"Could not setup file logging: {str(e)}")
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self.logger.critical(message)
    
    def log_request(self, method, path, status_code, duration_ms, user_id=None):
        """Log request với format chuẩn"""
        user_info = f" - User: {user_id}" if user_id else ""
        self.info(f"Request: {method} {path} - Status: {status_code} - Duration: {duration_ms:.2f}ms{user_info}")
    
    def log_database_operation(self, operation, table, record_id=None, user_id=None):
        """Log database operations"""
        record_info = f" - ID: {record_id}" if record_id else ""
        user_info = f" - User: {user_id}" if user_id else ""
        self.info(f"DB Operation: {operation} on {table}{record_info}{user_info}")
    
    def log_sync_operation(self, user_id, operation, count=0, duration_ms=0):
        """Log sync operations"""
        self.info(f"Sync: {operation} - User: {user_id} - Count: {count} - Duration: {duration_ms:.2f}ms")
    
    def log_authentication(self, username, action, success=True, ip_address=None):
        """Log authentication events"""
        status = "SUCCESS" if success else "FAILED"
        ip_info = f" - IP: {ip_address}" if ip_address else ""
        self.info(f"Auth: {action} - User: {username} - Status: {status}{ip_info}")
    
    def log_error_with_context(self, error, context=None):
        """Log error với context"""
        context_info = f" - Context: {context}" if context else ""
        self.error(f"Error: {str(error)}{context_info}")
    
    def log_performance_warning(self, operation, duration_ms, threshold_ms=1000):
        """Log performance warning khi operation chậm"""
        if duration_ms > threshold_ms:
            self.warning(f"Performance Warning: {operation} took {duration_ms:.2f}ms (threshold: {threshold_ms}ms)")

class RequestLogger:
    """Logger đặc biệt cho request tracking"""
    
    def __init__(self):
        self.logger = Logger('request_logger')
    
    def log_api_call(self, method, endpoint, status_code, duration_ms, user_id=None, ip_address=None):
        """Log API call với đầy đủ thông tin"""
        user_info = f"User: {user_id}" if user_id else "Anonymous"
        ip_info = f"IP: {ip_address}" if ip_address else "Unknown IP"
        
        self.logger.info(
            f"API Call - {method} {endpoint} - "
            f"Status: {status_code} - "
            f"Duration: {duration_ms:.2f}ms - "
            f"{user_info} - {ip_info}"
        )
    
    def log_slow_query(self, query_type, duration_ms, details=None):
        """Log slow database queries"""
        details_info = f" - Details: {details}" if details else ""
        self.logger.warning(f"Slow Query: {query_type} - Duration: {duration_ms:.2f}ms{details_info}")

class SecurityLogger:
    """Logger cho security events"""
    
    def __init__(self):
        self.logger = Logger('security_logger')
    
    def log_failed_login(self, username, ip_address, reason=None):
        """Log failed login attempts"""
        reason_info = f" - Reason: {reason}" if reason else ""
        self.logger.warning(f"Failed Login: {username} from {ip_address}{reason_info}")
    
    def log_suspicious_activity(self, activity, user_id=None, ip_address=None, details=None):
        """Log suspicious activities"""
        user_info = f" - User: {user_id}" if user_id else ""
        ip_info = f" - IP: {ip_address}" if ip_address else ""
        details_info = f" - Details: {details}" if details else ""
        
        self.logger.warning(f"Suspicious Activity: {activity}{user_info}{ip_info}{details_info}")
    
    def log_rate_limit_exceeded(self, ip_address, endpoint):
        """Log rate limit violations"""
        self.logger.warning(f"Rate Limit Exceeded: {ip_address} on {endpoint}")
    
    def log_invalid_token(self, token_info, ip_address):
        """Log invalid token usage"""
        self.logger.warning(f"Invalid Token: {token_info} from {ip_address}")

class SyncLogger:
    """Logger cho sync operations"""
    
    def __init__(self):
        self.logger = Logger('sync_logger')
    
    def log_sync_start(self, user_id, sync_type):
        """Log bắt đầu sync"""
        self.logger.info(f"Sync Started: User {user_id} - Type: {sync_type}")
    
    def log_sync_complete(self, user_id, sync_type, items_count, duration_ms):
        """Log hoàn thành sync"""
        self.logger.info(f"Sync Completed: User {user_id} - Type: {sync_type} - Items: {items_count} - Duration: {duration_ms:.2f}ms")
    
    def log_sync_error(self, user_id, sync_type, error):
        """Log lỗi sync"""
        self.logger.error(f"Sync Error: User {user_id} - Type: {sync_type} - Error: {str(error)}")
    
    def log_conflict_detected(self, user_id, item_id, conflict_type):
        """Log conflict trong sync"""
        self.logger.warning(f"Sync Conflict: User {user_id} - Item: {item_id} - Type: {conflict_type}")

# Tạo các instance logger global
logger = Logger()
request_logger = RequestLogger()
security_logger = SecurityLogger()
sync_logger = SyncLogger()

# Utility functions
def log_function_call(func_name, args=None, kwargs=None):
    """Decorator để log function calls"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.utcnow()
            
            # Log function start
            logger.debug(f"Function Call: {func_name} started")
            
            try:
                result = func(*args, **kwargs)
                
                # Log function success
                duration = (datetime.utcnow() - start_time).total_seconds() * 1000
                logger.debug(f"Function Call: {func_name} completed in {duration:.2f}ms")
                
                return result
                
            except Exception as e:
                # Log function error
                duration = (datetime.utcnow() - start_time).total_seconds() * 1000
                logger.error(f"Function Call: {func_name} failed after {duration:.2f}ms - Error: {str(e)}")
                raise
        
        return wrapper
    return decorator

def setup_logging():
    """Setup logging cho toàn bộ ứng dụng"""
    # Disable werkzeug logging trong production
    if os.getenv('FLASK_ENV') == 'production':
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(logging.WARNING)
    
    logger.info("Logging system initialized")

# Auto setup khi import module
setup_logging()
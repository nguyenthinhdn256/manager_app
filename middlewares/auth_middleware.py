# Xác thực, log, etc.
from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.User import User
from utils.logger import logger
from utils.response_wrapper import ResponseWrapper
from datetime import datetime, timedelta

def token_required(f):
    """Decorator để yêu cầu JWT token hợp lệ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Verify JWT token
            verify_jwt_in_request()
            
            # Lấy user ID từ token
            current_user_id = get_jwt_identity()
            
            if not current_user_id:
                response = ResponseWrapper()
                return response.error(
                    message="Token không hợp lệ",
                    status_code=401
                )
            
            # Tìm user trong database
            current_user = User.find_by_id(current_user_id)
            
            if not current_user:
                response = ResponseWrapper()
                return response.error(
                    message="Người dùng không tồn tại",
                    status_code=401
                )
            
            # Log request với user info
            logger.info(f"Authenticated request: {request.method} {request.path} - User: {current_user.username}")
            
            # Truyền current_user vào function
            return f(current_user, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            response = ResponseWrapper()
            return response.error(
                message="Lỗi xác thực",
                status_code=401
            )
    
    return decorated_function

def admin_required(f):
    """Decorator yêu cầu quyền admin (nếu có hệ thống role)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            
            current_user_id = get_jwt_identity()
            current_user = User.find_by_id(current_user_id)
            
            if not current_user:
                response = ResponseWrapper()
                return response.error(
                    message="Người dùng không tồn tại",
                    status_code=401
                )
            
            # Kiểm tra role admin (có thể mở rộng thêm field role trong User model)
            # Hiện tại chỉ kiểm tra user_id = 1 là admin
            if current_user.id != 1:
                response = ResponseWrapper()
                return response.error(
                    message="Không có quyền truy cập",
                    status_code=403
                )
            
            logger.info(f"Admin request: {request.method} {request.path} - User: {current_user.username}")
            
            return f(current_user, *args, **kwargs)
            
        except Exception as e:
            logger.error(f"Admin authentication error: {str(e)}")
            response = ResponseWrapper()
            return response.error(
                message="Lỗi xác thực admin",
                status_code=403
            )
    
    return decorated_function

def optional_auth(f):
    """Decorator cho authentication tùy chọn (không bắt buộc)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user = None
        
        try:
            # Thử verify JWT token
            verify_jwt_in_request(optional=True)
            
            current_user_id = get_jwt_identity()
            if current_user_id:
                current_user = User.find_by_id(current_user_id)
                
                if current_user:
                    logger.info(f"Optional auth request: {request.method} {request.path} - User: {current_user.username}")
                else:
                    logger.info(f"Optional auth request: {request.method} {request.path} - Invalid user ID: {current_user_id}")
            else:
                logger.info(f"Optional auth request: {request.method} {request.path} - Anonymous user")
                
        except Exception as e:
            # Nếu có lỗi authentication, vẫn cho phép tiếp tục với current_user = None
            logger.info(f"Optional auth request: {request.method} {request.path} - Anonymous user (auth failed)")
        
        # Truyền current_user (có thể là None) vào function
        return f(current_user, *args, **kwargs)
    
    return decorated_function

def rate_limit_middleware(max_requests=100, per_minutes=60):
    """Middleware giới hạn số request (đơn giản)"""
    request_counts = {}
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            from datetime import datetime, timedelta
            
            # Lấy IP address
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            current_time = datetime.utcnow()
            
            # Làm sạch dữ liệu cũ
            cutoff_time = current_time - timedelta(minutes=per_minutes)
            request_counts[client_ip] = [
                req_time for req_time in request_counts.get(client_ip, [])
                if req_time > cutoff_time
            ]
            
            # Kiểm tra số lượng request
            if len(request_counts.get(client_ip, [])) >= max_requests:
                response = ResponseWrapper()
                return response.error(
                    message=f"Quá nhiều request. Giới hạn {max_requests} request/{per_minutes} phút",
                    status_code=429
                )
            
            # Thêm request hiện tại
            if client_ip not in request_counts:
                request_counts[client_ip] = []
            request_counts[client_ip].append(current_time)
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def cors_middleware():
    """Middleware xử lý CORS (nếu cần custom logic)"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Custom CORS logic có thể thêm ở đây
            # Flask-CORS đã xử lý cơ bản rồi
            
            response = f(*args, **kwargs)
            
            # Thêm custom headers nếu cần
            if hasattr(response, 'headers'):
                response.headers['X-API-Version'] = '1.0'
                response.headers['X-Powered-By'] = 'Flask-Python-Backend'
            
            return response
        
        return decorated_function
    return decorator

def validate_json_middleware(required_fields=None):
    """Middleware validate JSON input"""
    if required_fields is None:
        required_fields = []
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Kiểm tra Content-Type
            if request.content_type != 'application/json':
                response = ResponseWrapper()
                return response.error(
                    message="Content-Type phải là application/json",
                    status_code=400
                )
            
            # Kiểm tra JSON hợp lệ
            try:
                data = request.get_json()
                if data is None:
                    response = ResponseWrapper()
                    return response.error(
                        message="JSON không hợp lệ",
                        status_code=400
                    )
            except Exception as e:
                response = ResponseWrapper()
                return response.error(
                    message="JSON không hợp lệ",
                    status_code=400
                )
            
            # Kiểm tra required fields
            missing_fields = []
            for field in required_fields:
                if field not in data or data[field] is None:
                    missing_fields.append(field)
            
            if missing_fields:
                response = ResponseWrapper()
                return response.error(
                    message=f"Thiếu các trường bắt buộc: {', '.join(missing_fields)}",
                    status_code=400
                )
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator

def log_request_middleware(f):
    """Middleware log tất cả request"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = datetime.utcnow()
        
        # Log request info
        logger.info(f"Request: {request.method} {request.path} - IP: {request.remote_addr}")
        
        # Execute function
        response = f(*args, **kwargs)
        
        # Log response info
        end_time = datetime.utcnow()
        duration = (end_time - start_time).total_seconds() * 1000  # milliseconds
        
        logger.info(f"Response: {request.method} {request.path} - Duration: {duration:.2f}ms")
        
        return response
    
    return decorated_function
# Xử lý lỗi tập trung
from flask import jsonify, request
from werkzeug.exceptions import HTTPException, NotFound, BadRequest, Unauthorized, Forbidden, InternalServerError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from utils.logger import logger
from utils.response_wrapper import ResponseWrapper
import traceback

def register_error_handlers(app):
    """Đăng ký các error handler cho Flask app"""
    
    @app.errorhandler(400)
    def bad_request_error(error):
        """Xử lý lỗi Bad Request (400)"""
        logger.warning(f"Bad Request: {request.method} {request.path} - {str(error)}")
        
        response = ResponseWrapper()
        return response.error(
            message="Yêu cầu không hợp lệ",
            error=str(error.description) if hasattr(error, 'description') else str(error),
            status_code=400
        )
    
    @app.errorhandler(401)
    def unauthorized_error(error):
        """Xử lý lỗi Unauthorized (401)"""
        logger.warning(f"Unauthorized: {request.method} {request.path} - {str(error)}")
        
        response = ResponseWrapper()
        return response.error(
            message="Không có quyền truy cập",
            error="Token không hợp lệ hoặc đã hết hạn",
            status_code=401
        )
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Xử lý lỗi Forbidden (403)"""
        logger.warning(f"Forbidden: {request.method} {request.path} - {str(error)}")
        
        response = ResponseWrapper()
        return response.error(
            message="Bị cấm truy cập",
            error="Không đủ quyền để thực hiện hành động này",
            status_code=403
        )
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Xử lý lỗi Not Found (404)"""
        logger.warning(f"Not Found: {request.method} {request.path}")
        
        response = ResponseWrapper()
        return response.error(
            message="Không tìm thấy tài nguyên",
            error=f"Endpoint {request.path} không tồn tại",
            status_code=404
        )
    
    @app.errorhandler(405)
    def method_not_allowed_error(error):
        """Xử lý lỗi Method Not Allowed (405)"""
        logger.warning(f"Method Not Allowed: {request.method} {request.path}")
        
        response = ResponseWrapper()
        return response.error(
            message="Phương thức không được phép",
            error=f"Phương thức {request.method} không được hỗ trợ cho endpoint này",
            status_code=405
        )
    
    @app.errorhandler(429)
    def rate_limit_error(error):
        """Xử lý lỗi Rate Limit (429)"""
        logger.warning(f"Rate Limited: {request.method} {request.path} - IP: {request.remote_addr}")
        
        response = ResponseWrapper()
        return response.error(
            message="Quá nhiều yêu cầu",
            error="Bạn đã vượt quá giới hạn số request cho phép",
            status_code=429
        )
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Xử lý lỗi Internal Server Error (500)"""
        logger.error(f"Internal Server Error: {request.method} {request.path} - {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        response = ResponseWrapper()
        return response.error(
            message="Lỗi máy chủ nội bộ",
            error="Có lỗi xảy ra trên máy chủ. Vui lòng thử lại sau.",
            status_code=500
        )
    
    @app.errorhandler(SQLAlchemyError)
    def database_error(error):
        """Xử lý lỗi database SQLAlchemy"""
        logger.error(f"Database Error: {request.method} {request.path} - {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        response = ResponseWrapper()
        
        # Kiểm tra loại lỗi database cụ thể
        if isinstance(error, IntegrityError):
            return response.error(
                message="Lỗi tính toàn vẹn dữ liệu",
                error="Dữ liệu vi phạm ràng buộc của database",
                status_code=400
            )
        else:
            return response.error(
                message="Lỗi cơ sở dữ liệu",
                error="Có lỗi xảy ra khi truy cập cơ sở dữ liệu",
                status_code=500
            )
    
    @app.errorhandler(KeyError)
    def key_error(error):
        """Xử lý lỗi KeyError (thiếu key trong dict)"""
        logger.error(f"Key Error: {request.method} {request.path} - Missing key: {str(error)}")
        
        response = ResponseWrapper()
        return response.error(
            message="Thiếu thông tin bắt buộc",
            error=f"Thiếu trường: {str(error)}",
            status_code=400
        )
    
    @app.errorhandler(ValueError)
    def value_error(error):
        """Xử lý lỗi ValueError (giá trị không hợp lệ)"""
        logger.error(f"Value Error: {request.method} {request.path} - {str(error)}")
        
        response = ResponseWrapper()
        return response.error(
            message="Giá trị không hợp lệ",
            error=str(error),
            status_code=400
        )
    
    @app.errorhandler(TypeError)
    def type_error(error):
        """Xử lý lỗi TypeError"""
        logger.error(f"Type Error: {request.method} {request.path} - {str(error)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        response = ResponseWrapper()
        return response.error(
            message="Lỗi kiểu dữ liệu",
            error="Kiểu dữ liệu không phù hợp",
            status_code=400
        )
    
    @app.errorhandler(Exception)
    def general_exception_handler(error):
        """Xử lý tất cả các exception chưa được catch"""
        logger.error(f"Unhandled Exception: {request.method} {request.path} - {str(error)}")
        logger.error(f"Exception type: {type(error).__name__}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        
        response = ResponseWrapper()
        
        # Trong môi trường development, trả về chi tiết lỗi
        if app.config.get('DEBUG', False):
            return response.error(
                message="Lỗi hệ thống",
                error=f"{type(error).__name__}: {str(error)}",
                status_code=500
            )
        else:
            # Trong môi trường production, ẩn chi tiết lỗi
            return response.error(
                message="Có lỗi xảy ra",
                error="Vui lòng thử lại sau hoặc liên hệ hỗ trợ",
                status_code=500
            )

class APIException(Exception):
    """Custom exception cho API"""
    
    def __init__(self, message, status_code=400, error_code=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

class ValidationError(APIException):
    """Exception cho lỗi validation"""
    
    def __init__(self, message, field=None):
        super().__init__(message, status_code=400)
        self.field = field

class AuthenticationError(APIException):
    """Exception cho lỗi authentication"""
    
    def __init__(self, message="Lỗi xác thực"):
        super().__init__(message, status_code=401)

class AuthorizationError(APIException):
    """Exception cho lỗi authorization"""
    
    def __init__(self, message="Không có quyền truy cập"):
        super().__init__(message, status_code=403)

class ResourceNotFoundError(APIException):
    """Exception cho lỗi không tìm thấy resource"""
    
    def __init__(self, message="Không tìm thấy tài nguyên"):
        super().__init__(message, status_code=404)

class DatabaseError(APIException):
    """Exception cho lỗi database"""
    
    def __init__(self, message="Lỗi cơ sở dữ liệu"):
        super().__init__(message, status_code=500)

def handle_api_exception(app):
    """Đăng ký handler cho các custom exception"""
    
    @app.errorhandler(APIException)
    def api_exception_handler(error):
        """Xử lý các custom API exception"""
        logger.error(f"API Exception: {request.method} {request.path} - {error.message}")
        
        response = ResponseWrapper()
        return response.error(
            message=error.message,
            error_code=error.error_code,
            status_code=error.status_code
        )
    
    @app.errorhandler(ValidationError)
    def validation_error_handler(error):
        """Xử lý validation error"""
        logger.warning(f"Validation Error: {request.method} {request.path} - {error.message}")
        
        response = ResponseWrapper()
        return response.error(
            message=error.message,
            error_code="VALIDATION_ERROR",
            status_code=400
        )

# Đăng ký tất cả error handlers
def setup_error_handlers(app):
    """Setup tất cả error handlers"""
    register_error_handlers(app)
    handle_api_exception(app)
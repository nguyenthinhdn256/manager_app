# Response wrapper để chuẩn hóa API response
from flask import jsonify
from datetime import datetime
import json

class ResponseWrapper:
    """Class để chuẩn hóa response format"""
    
    def __init__(self):
        pass
    
    def success(self, data=None, message="Thành công", status_code=200, meta=None):
        """Tạo success response"""
        response_data = {
            "success": True,
            "status_code": status_code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        # Thêm metadata nếu có
        if meta:
            response_data["meta"] = meta
        
        return jsonify(response_data), status_code
    
    def error(self, message="Có lỗi xảy ra", error=None, status_code=400, error_code=None):
        """Tạo error response"""
        response_data = {
            "success": False,
            "status_code": status_code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "error": error
        }
        
        # Thêm error code nếu có
        if error_code:
            response_data["error_code"] = error_code
        
        return jsonify(response_data), status_code
    
    def paginated_success(self, data, page, per_page, total, message="Lấy dữ liệu thành công"):
        """Tạo success response với pagination"""
        total_pages = (total + per_page - 1) // per_page  # Ceiling division
        
        meta = {
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
        }
        
        return self.success(data=data, message=message, meta=meta)
    
    def created(self, data=None, message="Tạo thành công"):
        """Tạo response cho resource được tạo (201)"""
        return self.success(data=data, message=message, status_code=201)
    
    def no_content(self, message="Thành công"):
        """Tạo response không có content (204)"""
        return self.success(data=None, message=message, status_code=204)
    
    def validation_error(self, errors, message="Dữ liệu không hợp lệ"):
        """Tạo response cho validation errors"""
        return self.error(
            message=message,
            error=errors,
            status_code=400,
            error_code="VALIDATION_ERROR"
        )
    
    def unauthorized(self, message="Không có quyền truy cập"):
        """Tạo response cho unauthorized (401)"""
        return self.error(
            message=message,
            status_code=401,
            error_code="UNAUTHORIZED"
        )
    
    def forbidden(self, message="Bị cấm truy cập"):
        """Tạo response cho forbidden (403)"""
        return self.error(
            message=message,
            status_code=403,
            error_code="FORBIDDEN"
        )
    
    def not_found(self, message="Không tìm thấy tài nguyên"):
        """Tạo response cho not found (404)"""
        return self.error(
            message=message,
            status_code=404,
            error_code="NOT_FOUND"
        )
    
    def conflict(self, message="Xung đột dữ liệu", error=None):
        """Tạo response cho conflict (409)"""
        return self.error(
            message=message,
            error=error,
            status_code=409,
            error_code="CONFLICT"
        )
    
    def rate_limit_exceeded(self, message="Quá nhiều yêu cầu"):
        """Tạo response cho rate limit (429)"""
        return self.error(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED"
        )
    
    def internal_server_error(self, message="Lỗi máy chủ nội bộ", error=None):
        """Tạo response cho server error (500)"""
        return self.error(
            message=message,
            error=error,
            status_code=500,
            error_code="INTERNAL_SERVER_ERROR"
        )

class ApiResponse:
    """Utility class cho các response patterns phổ biến"""
    
    @staticmethod
    def login_success(user_data, access_token):
        """Response cho login thành công"""
        response = ResponseWrapper()
        return response.success(
            data={
                "user": user_data,
                "access_token": access_token,
                "token_type": "Bearer"
            },
            message="Đăng nhập thành công"
        )
    
    @staticmethod
    def logout_success():
        """Response cho logout thành công"""
        response = ResponseWrapper()
        return response.success(message="Đăng xuất thành công")
    
    @staticmethod
    def registration_success(user_data):
        """Response cho đăng ký thành công"""
        response = ResponseWrapper()
        return response.created(
            data=user_data,
            message="Đăng ký tài khoản thành công"
        )
    
    @staticmethod
    def sync_success(sync_data, sync_type="full"):
        """Response cho sync thành công"""
        response = ResponseWrapper()
        return response.success(
            data=sync_data,
            message=f"Đồng bộ {sync_type} thành công"
        )
    
    @staticmethod
    def data_created(data):
        """Response cho tạo dữ liệu thành công"""
        response = ResponseWrapper()
        return response.created(
            data=data,
            message="Tạo dữ liệu thành công"
        )
    
    @staticmethod
    def data_updated(data):
        """Response cho cập nhật dữ liệu thành công"""
        response = ResponseWrapper()
        return response.success(
            data=data,
            message="Cập nhật dữ liệu thành công"
        )
    
    @staticmethod
    def data_deleted():
        """Response cho xóa dữ liệu thành công"""
        response = ResponseWrapper()
        return response.success(message="Xóa dữ liệu thành công")
    
    @staticmethod
    def invalid_credentials():
        """Response cho thông tin đăng nhập sai"""
        response = ResponseWrapper()
        return response.unauthorized(message="Tên đăng nhập hoặc mật khẩu không đúng")
    
    @staticmethod
    def token_expired():
        """Response cho token hết hạn"""
        response = ResponseWrapper()
        return response.unauthorized(message="Token đã hết hạn")
    
    @staticmethod
    def invalid_token():
        """Response cho token không hợp lệ"""
        response = ResponseWrapper()
        return response.unauthorized(message="Token không hợp lệ")
    
    @staticmethod
    def user_not_found():
        """Response cho không tìm thấy user"""
        response = ResponseWrapper()
        return response.not_found(message="Người dùng không tồn tại")
    
    @staticmethod
    def data_not_found():
        """Response cho không tìm thấy dữ liệu"""
        response = ResponseWrapper()
        return response.not_found(message="Dữ liệu không tồn tại")
    
    @staticmethod
    def username_exists():
        """Response cho username đã tồn tại"""
        response = ResponseWrapper()
        return response.conflict(message="Tên đăng nhập đã tồn tại")
    
    @staticmethod
    def email_exists():
        """Response cho email đã tồn tại"""
        response = ResponseWrapper()
        return response.conflict(message="Email đã được sử dụng")

class ResponseFormatter:
    """Helper class để format response data"""
    
    @staticmethod
    def format_user_data(user, include_sensitive=False):
        """Format user data cho response"""
        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email if include_sensitive else None,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        
        # Loại bỏ các field None
        return {k: v for k, v in user_data.items() if v is not None}
    
    @staticmethod
    def format_app_data(data_item):
        """Format app data cho response"""
        return {
            "id": data_item.id,
            "type": data_item.type,
            "title": data_item.title,
            "content": data_item.content,
            "created_at": data_item.created_at.isoformat() if data_item.created_at else None,
            "updated_at": data_item.updated_at.isoformat() if data_item.updated_at else None
        }
    
    @staticmethod
    def format_sync_data(data_items):
        """Format sync data cho response"""
        return [
            ResponseFormatter.format_app_data(item) 
            for item in data_items
        ]
    
    @staticmethod
    def sanitize_error_message(error_message, is_production=True):
        """Làm sạch error message cho production"""
        if is_production:
            # Trong production, ẩn chi tiết technical errors
            generic_messages = {
                "database": "Lỗi cơ sở dữ liệu",
                "connection": "Lỗi kết nối",
                "timeout": "Hết thời gian chờ",
                "internal": "Lỗi hệ thống"
            }
            
            error_lower = error_message.lower()
            for key, message in generic_messages.items():
                if key in error_lower:
                    return message
            
            return "Có lỗi xảy ra, vui lòng thử lại"
        else:
            # Trong development, hiển thị chi tiết
            return error_message

# Export các class chính
__all__ = ['ResponseWrapper', 'ApiResponse', 'ResponseFormatter']
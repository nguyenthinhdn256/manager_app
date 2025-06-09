# Xử lý logic nghiệp vụ cho người dùng
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt
from models.User import User
from config.db import db
from utils.response_wrapper import ResponseWrapper
from utils.logger import logger
import bcrypt

class UserController:
    def __init__(self):
        self.response = ResponseWrapper()

    def register(self):
        """Đăng ký tài khoản mới"""
        try:
            data = request.get_json()
            
            # Validate input
            if not data or not all(k in data for k in ('username', 'email', 'password')):
                return self.response.error(
                    message="Thiếu thông tin bắt buộc (username, email, password)"
                )
            
            username = data['username']
            email = data['email']
            password = data['password']
            
            # Kiểm tra user đã tồn tại
            if User.query.filter_by(username=username).first():
                return self.response.error(message="Tên đăng nhập đã tồn tại")
            
            if User.query.filter_by(email=email).first():
                return self.response.error(message="Email đã được sử dụng")
            
            # Hash password
            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            # Tạo user mới
            new_user = User(
                username=username,
                email=email,
                password=hashed_password
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"New user registered: {username}")
            
            return self.response.success(
                data={
                    'user_id': new_user.id,
                    'username': new_user.username,
                    'email': new_user.email
                },
                message="Đăng ký thành công"
            )
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            return self.response.error(
                message="Lỗi khi đăng ký",
                error=str(e)
            )

    def login(self):
        """Đăng nhập"""
        try:
            data = request.get_json()
            
            if not data or not all(k in data for k in ('username', 'password')):
                return self.response.error(
                    message="Thiếu username hoặc password"
                )
            
            username = data['username']
            password = data['password']
            
            # Tìm user
            user = User.query.filter_by(username=username).first()
            
            if not user:
                return self.response.error(message="Tài khoản không tồn tại")
            
            # Verify password
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return self.response.error(message="Mật khẩu không đúng")
            
            # Tạo JWT token
            access_token = create_access_token(identity=user.id)
            
            logger.info(f"User logged in: {username}")
            
            return self.response.success(
                data={
                    'access_token': access_token,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email
                    }
                },
                message="Đăng nhập thành công"
            )
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return self.response.error(
                message="Lỗi khi đăng nhập",
                error=str(e)
            )

    def get_profile(self, current_user):
        """Lấy thông tin profile"""
        try:
            return self.response.success(
                data={
                    'id': current_user.id,
                    'username': current_user.username,
                    'email': current_user.email,
                    'created_at': current_user.created_at.isoformat() if current_user.created_at else None
                },
                message="Lấy thông tin profile thành công"
            )
            
        except Exception as e:
            logger.error(f"Get profile error: {str(e)}")
            return self.response.error(
                message="Lỗi khi lấy thông tin profile",
                error=str(e)
            )

    def update_profile(self, current_user):
        """Cập nhật profile"""
        try:
            data = request.get_json()
            
            if not data:
                return self.response.error(message="Không có dữ liệu để cập nhật")
            
            # Cập nhật các field được phép
            if 'email' in data:
                # Kiểm tra email đã tồn tại
                existing_user = User.query.filter_by(email=data['email']).first()
                if existing_user and existing_user.id != current_user.id:
                    return self.response.error(message="Email đã được sử dụng")
                current_user.email = data['email']
            
            if 'password' in data:
                # Hash password mới
                hashed_password = bcrypt.hashpw(
                    data['password'].encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                current_user.password = hashed_password
            
            db.session.commit()
            
            logger.info(f"User profile updated: {current_user.username}")
            
            return self.response.success(
                data={
                    'id': current_user.id,
                    'username': current_user.username,
                    'email': current_user.email
                },
                message="Cập nhật profile thành công"
            )
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Update profile error: {str(e)}")
            return self.response.error(
                message="Lỗi khi cập nhật profile",
                error=str(e)
            )

    def logout(self, current_user):
        """Đăng xuất"""
        try:
            # Trong JWT, logout thường chỉ cần client xóa token
            # Có thể implement blacklist token nếu cần
            
            logger.info(f"User logged out: {current_user.username}")
            
            return self.response.success(
                message="Đăng xuất thành công"
            )
            
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            return self.response.error(
                message="Lỗi khi đăng xuất",
                error=str(e)
            )

    def delete_account(self, current_user):
        """Xóa tài khoản"""
        try:
            # Xóa tất cả data của user trước
            from models.AppData import AppData
            AppData.query.filter_by(user_id=current_user.id).delete()
            
            # Xóa user
            db.session.delete(current_user)
            db.session.commit()
            
            logger.info(f"User account deleted: {current_user.username}")
            
            return self.response.success(
                message="Xóa tài khoản thành công"
            )
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Delete account error: {str(e)}")
            return self.response.error(
                message="Lỗi khi xóa tài khoản",
                error=str(e)
            )
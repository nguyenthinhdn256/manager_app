# API người dùng
from flask import Blueprint
from controllers.user_controller import UserController
from middlewares.auth_middleware import token_required

# Tạo blueprint
user_bp = Blueprint('user', __name__)

# Khởi tạo controller
user_controller = UserController()

# POST /api/user/register - Đăng ký
@user_bp.route('/register', methods=['POST'])
def register():
    return user_controller.register()

# POST /api/user/login - Đăng nhập
@user_bp.route('/login', methods=['POST'])
def login():
    return user_controller.login()

# GET /api/user/profile - Lấy thông tin profile
@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return user_controller.get_profile(current_user)

# PUT /api/user/profile - Cập nhật profile
@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    return user_controller.update_profile(current_user)

# POST /api/user/logout - Đăng xuất
@user_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    return user_controller.logout(current_user)

# DELETE /api/user/account - Xóa tài khoản
@user_bp.route('/account', methods=['DELETE'])
@token_required
def delete_account(current_user):
    return user_controller.delete_account(current_user)
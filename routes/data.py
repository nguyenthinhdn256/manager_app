# API dữ liệu app
from flask import Blueprint
from controllers.data_controller import DataController
from middlewares.auth_middleware import token_required

# Tạo blueprint
data_bp = Blueprint('data', __name__)

# Khởi tạo controller
data_controller = DataController()

# GET /api/data - Lấy tất cả dữ liệu của user
@data_bp.route('/', methods=['GET'])
@token_required
def get_all_data(current_user):
    return data_controller.get_all_data(current_user)

# GET /api/data/<id> - Lấy dữ liệu theo ID
@data_bp.route('/<int:data_id>', methods=['GET'])
@token_required
def get_data_by_id(current_user, data_id):
    return data_controller.get_data_by_id(current_user, data_id)

# POST /api/data - Tạo dữ liệu mới
@data_bp.route('/', methods=['POST'])
@token_required
def create_data(current_user):
    return data_controller.create_data(current_user)

# PUT /api/data/<id> - Cập nhật dữ liệu
@data_bp.route('/<int:data_id>', methods=['PUT'])
@token_required
def update_data(current_user, data_id):
    return data_controller.update_data(current_user, data_id)

# DELETE /api/data/<id> - Xóa dữ liệu
@data_bp.route('/<int:data_id>', methods=['DELETE'])
@token_required
def delete_data(current_user, data_id):
    return data_controller.delete_data(current_user, data_id)

# GET /api/data/type/<type> - Lấy dữ liệu theo loại
@data_bp.route('/type/<string:data_type>', methods=['GET'])
@token_required
def get_data_by_type(current_user, data_type):
    return data_controller.get_data_by_type(current_user, data_type)
# API cho đồng bộ realtime
from flask import Blueprint
from controllers.sync_controller import SyncController
from middlewares.auth_middleware import token_required

# Tạo blueprint
sync_bp = Blueprint('sync', __name__)

# Khởi tạo controller
sync_controller = SyncController()

# GET /api/sync - Lấy dữ liệu đồng bộ
@sync_bp.route('/', methods=['GET'])
@token_required
def get_sync_data(current_user):
    return sync_controller.get_sync_data(current_user)

# POST /api/sync - Gửi dữ liệu để đồng bộ
@sync_bp.route('/', methods=['POST'])
@token_required
def sync_data(current_user):
    return sync_controller.sync_data(current_user)

# GET /api/sync/status - Kiểm tra trạng thái đồng bộ
@sync_bp.route('/status', methods=['GET'])
@token_required
def get_sync_status(current_user):
    return sync_controller.get_sync_status(current_user)

# POST /api/sync/force - Buộc đồng bộ toàn bộ
@sync_bp.route('/force', methods=['POST'])
@token_required
def force_sync(current_user):
    return sync_controller.force_sync(current_user)
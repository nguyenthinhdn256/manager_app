# Xử lý logic nghiệp vụ cho đồng bộ realtime
from flask import request, jsonify, current_app
from services.sync_service import SyncService
from utils.response_wrapper import ResponseWrapper
from utils.logger import logger

class SyncController:
    def __init__(self):
        self.sync_service = SyncService()
        self.response = ResponseWrapper()

    def get_sync_data(self, current_user):
        """Lấy dữ liệu đồng bộ của user"""
        try:
            # Lấy timestamp từ query params (nếu có)
            last_sync = request.args.get('last_sync')
            
            # Gọi service để lấy data
            sync_data = self.sync_service.get_user_sync_data(
                user_id=current_user.id,
                last_sync=last_sync
            )
            
            logger.info(f"User {current_user.id} requested sync data")
            
            return self.response.success(
                data=sync_data,
                message="Lấy dữ liệu đồng bộ thành công"
            )
            
        except Exception as e:
            logger.error(f"Error getting sync data: {str(e)}")
            return self.response.error(
                message="Lỗi khi lấy dữ liệu đồng bộ",
                error=str(e)
            )

    def sync_data(self, current_user):
        """Đồng bộ dữ liệu từ client lên server"""
        try:
            # Lấy data từ request body
            sync_payload = request.get_json()
            
            if not sync_payload:
                return self.response.error(message="Dữ liệu đồng bộ không hợp lệ")
            
            # Xử lý đồng bộ
            result = self.sync_service.process_sync_data(
                user_id=current_user.id,
                sync_data=sync_payload
            )
            
            # Phát broadcast đến các client khác
            if current_app.socketio:
                current_app.socketio.emit(
                    'data_updated',
                    {
                        'user_id': current_user.id,
                        'data': result['updated_data'],
                        'timestamp': result['timestamp']
                    },
                    room=f"user_{current_user.id}"
                )
            
            logger.info(f"User {current_user.id} synced data successfully")
            
            return self.response.success(
                data=result,
                message="Đồng bộ dữ liệu thành công"
            )
            
        except Exception as e:
            logger.error(f"Error syncing data: {str(e)}")
            return self.response.error(
                message="Lỗi khi đồng bộ dữ liệu",
                error=str(e)
            )

    def get_sync_status(self, current_user):
        """Kiểm tra trạng thái đồng bộ"""
        try:
            status = self.sync_service.get_sync_status(current_user.id)
            
            return self.response.success(
                data=status,
                message="Lấy trạng thái đồng bộ thành công"
            )
            
        except Exception as e:
            logger.error(f"Error getting sync status: {str(e)}")
            return self.response.error(
                message="Lỗi khi lấy trạng thái đồng bộ",
                error=str(e)
            )

    def force_sync(self, current_user):
        """Buộc đồng bộ toàn bộ dữ liệu"""
        try:
            # Thực hiện force sync
            result = self.sync_service.force_full_sync(current_user.id)
            
            # Broadcast thông báo force sync
            if current_app.socketio:
                current_app.socketio.emit(
                    'force_sync_completed',
                    {
                        'user_id': current_user.id,
                        'timestamp': result['timestamp']
                    },
                    room=f"user_{current_user.id}"
                )
            
            logger.info(f"User {current_user.id} performed force sync")
            
            return self.response.success(
                data=result,
                message="Đồng bộ bắt buộc hoàn thành"
            )
            
        except Exception as e:
            logger.error(f"Error in force sync: {str(e)}")
            return self.response.error(
                message="Lỗi khi thực hiện đồng bộ bắt buộc",
                error=str(e)
            )
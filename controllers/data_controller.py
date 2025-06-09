# Xử lý logic nghiệp vụ cho dữ liệu app
from flask import request, jsonify, current_app
from models.AppData import AppData
from config.db import db
from utils.response_wrapper import ResponseWrapper
from utils.logger import logger
from datetime import datetime

class DataController:
    def __init__(self):
        self.response = ResponseWrapper()

    def get_all_data(self, current_user):
        """Lấy tất cả dữ liệu của user"""
        try:
            # Lấy query parameters
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            data_type = request.args.get('type')
            
            # Query cơ bản
            query = AppData.query.filter_by(user_id=current_user.id)
            
            # Filter theo type nếu có
            if data_type:
                query = query.filter_by(type=data_type)
            
            # Order by created_at desc
            query = query.order_by(AppData.created_at.desc())
            
            # Pagination
            paginated_data = query.paginate(
                page=page, 
                per_page=per_page, 
                error_out=False
            )
            
            # Serialize data
            data_list = []
            for item in paginated_data.items:
                data_list.append({
                    'id': item.id,
                    'type': item.type,
                    'title': item.title,
                    'content': item.content,
                    'created_at': item.created_at.isoformat() if item.created_at else None,
                    'updated_at': item.updated_at.isoformat() if item.updated_at else None
                })
            
            return self.response.success(
                data={
                    'items': data_list,
                    'pagination': {
                        'page': page,
                        'per_page': per_page,
                        'total': paginated_data.total,
                        'pages': paginated_data.pages
                    }
                },
                message="Lấy dữ liệu thành công"
            )
            
        except Exception as e:
            logger.error(f"Get all data error: {str(e)}")
            return self.response.error(
                message="Lỗi khi lấy dữ liệu",
                error=str(e)
            )

    def get_data_by_id(self, current_user, data_id):
        """Lấy dữ liệu theo ID"""
        try:
            data_item = AppData.query.filter_by(
                id=data_id, 
                user_id=current_user.id
            ).first()
            
            if not data_item:
                return self.response.error(
                    message="Không tìm thấy dữ liệu",
                    status_code=404
                )
            
            return self.response.success(
                data={
                    'id': data_item.id,
                    'type': data_item.type,
                    'title': data_item.title,
                    'content': data_item.content,
                    'created_at': data_item.created_at.isoformat() if data_item.created_at else None,
                    'updated_at': data_item.updated_at.isoformat() if data_item.updated_at else None
                },
                message="Lấy dữ liệu thành công"
            )
            
        except Exception as e:
            logger.error(f"Get data by ID error: {str(e)}")
            return self.response.error(
                message="Lỗi khi lấy dữ liệu",
                error=str(e)
            )

    def create_data(self, current_user):
        """Tạo dữ liệu mới"""
        try:
            data = request.get_json()
            
            if not data or not all(k in data for k in ('type', 'content')):
                return self.response.error(
                    message="Thiếu thông tin bắt buộc (type, content)"
                )
            
            # Tạo data mới
            new_data = AppData(
                user_id=current_user.id,
                type=data['type'],
                title=data.get('title', ''),
                content=data['content']
            )
            
            db.session.add(new_data)
            db.session.commit()
            
            # Emit realtime update
            if current_app.socketio:
                current_app.socketio.emit(
                    'data_created',
                    {
                        'id': new_data.id,
                        'type': new_data.type,
                        'title': new_data.title,
                        'user_id': current_user.id
                    },
                    room=f"user_{current_user.id}"
                )
            
            logger.info(f"New data created by user {current_user.id}: {new_data.id}")
            
            return self.response.success(
                data={
                    'id': new_data.id,
                    'type': new_data.type,
                    'title': new_data.title,
                    'content': new_data.content,
                    'created_at': new_data.created_at.isoformat()
                },
                message="Tạo dữ liệu thành công"
            )
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Create data error: {str(e)}")
            return self.response.error(
                message="Lỗi khi tạo dữ liệu",
                error=str(e)
            )

    def update_data(self, current_user, data_id):
        """Cập nhật dữ liệu"""
        try:
            data_item = AppData.query.filter_by(
                id=data_id, 
                user_id=current_user.id
            ).first()
            
            if not data_item:
                return self.response.error(
                    message="Không tìm thấy dữ liệu",
                    status_code=404
                )
            
            update_data = request.get_json()
            if not update_data:
                return self.response.error(message="Không có dữ liệu để cập nhật")
            
            # Cập nhật các field
            if 'type' in update_data:
                data_item.type = update_data['type']
            if 'title' in update_data:
                data_item.title = update_data['title']
            if 'content' in update_data:
                data_item.content = update_data['content']
            
            data_item.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            # Emit realtime update
            if current_app.socketio:
                current_app.socketio.emit(
                    'data_updated',
                    {
                        'id': data_item.id,
                        'type': data_item.type,
                        'title': data_item.title,
                        'user_id': current_user.id
                    },
                    room=f"user_{current_user.id}"
                )
            
            logger.info(f"Data updated by user {current_user.id}: {data_id}")
            
            return self.response.success(
                data={
                    'id': data_item.id,
                    'type': data_item.type,
                    'title': data_item.title,
                    'content': data_item.content,
                    'updated_at': data_item.updated_at.isoformat()
                },
                message="Cập nhật dữ liệu thành công"
            )
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Update data error: {str(e)}")
            return self.response.error(
                message="Lỗi khi cập nhật dữ liệu",
                error=str(e)
            )

    def delete_data(self, current_user, data_id):
        """Xóa dữ liệu"""
        try:
            data_item = AppData.query.filter_by(
                id=data_id, 
                user_id=current_user.id
            ).first()
            
            if not data_item:
                return self.response.error(
                    message="Không tìm thấy dữ liệu",
                    status_code=404
                )
            
            db.session.delete(data_item)
            db.session.commit()
            
            # Emit realtime update
            if current_app.socketio:
                current_app.socketio.emit(
                    'data_deleted',
                    {
                        'id': data_id,
                        'user_id': current_user.id
                    },
                    room=f"user_{current_user.id}"
                )
            
            logger.info(f"Data deleted by user {current_user.id}: {data_id}")
            
            return self.response.success(
                message="Xóa dữ liệu thành công"
            )
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Delete data error: {str(e)}")
            return self.response.error(
                message="Lỗi khi xóa dữ liệu",
                error=str(e)
            )

    def get_data_by_type(self, current_user, data_type):
        """Lấy dữ liệu theo loại"""
        try:
            data_items = AppData.query.filter_by(
                user_id=current_user.id,
                type=data_type
            ).order_by(AppData.created_at.desc()).all()
            
            data_list = []
            for item in data_items:
                data_list.append({
                    'id': item.id,
                    'type': item.type,
                    'title': item.title,
                    'content': item.content,
                    'created_at': item.created_at.isoformat() if item.created_at else None,
                    'updated_at': item.updated_at.isoformat() if item.updated_at else None
                })
            
            return self.response.success(
                data=data_list,
                message=f"Lấy dữ liệu loại '{data_type}' thành công"
            )
            
        except Exception as e:
            logger.error(f"Get data by type error: {str(e)}")
            return self.response.error(
                message="Lỗi khi lấy dữ liệu theo loại",
                error=str(e)
            )
# Các service hỗ trợ (Realtime, socket, email, etc.)
from models.AppData import AppData
from models.User import User
from config.db import db
from datetime import datetime, timedelta
from utils.logger import logger
import json

class SyncService:
    """Service xử lý đồng bộ realtime"""
    
    def __init__(self):
        pass
    
    def get_user_sync_data(self, user_id, last_sync=None):
        """Lấy dữ liệu đồng bộ của user"""
        try:
            # Nếu có last_sync, chỉ lấy data được update sau thời điểm đó
            if last_sync:
                try:
                    last_sync_datetime = datetime.fromisoformat(last_sync.replace('Z', '+00:00'))
                    data_items = AppData.find_by_user_since(user_id, last_sync_datetime)
                except ValueError:
                    # Nếu parse datetime thất bại, lấy tất cả
                    data_items = AppData.find_by_user_id(user_id)
            else:
                # Lấy tất cả data của user
                data_items = AppData.find_by_user_id(user_id)
            
            # Chuyển đổi thành dict để sync
            sync_data = []
            for item in data_items:
                sync_data.append(item.to_sync_dict())
            
            return {
                'data': sync_data,
                'timestamp': datetime.utcnow().isoformat(),
                'count': len(sync_data),
                'user_id': user_id
            }
            
        except Exception as e:
            logger.error(f"Error getting sync data for user {user_id}: {str(e)}")
            raise e
    
    def process_sync_data(self, user_id, sync_data):
        """Xử lý dữ liệu đồng bộ từ client"""
        try:
            updated_items = []
            created_items = []
            errors = []
            
            # Lấy danh sách data từ payload
            data_items = sync_data.get('data', [])
            
            for item_data in data_items:
                try:
                    item_id = item_data.get('id')
                    
                    if item_id:
                        # Update existing item
                        existing_item = AppData.find_by_id(item_id)
                        if existing_item and existing_item.is_owned_by(user_id):
                            # Cập nhật
                            existing_item.update(
                                type=item_data.get('type', existing_item.type),
                                title=item_data.get('title', existing_item.title),
                                content=item_data.get('content', existing_item.content)
                            )
                            updated_items.append(existing_item.to_sync_dict())
                        else:
                            errors.append(f"Item {item_id} not found or not owned by user")
                    else:
                        # Create new item
                        new_item = AppData(
                            user_id=user_id,
                            type=item_data.get('type'),
                            title=item_data.get('title'),
                            content=item_data.get('content')
                        )
                        new_item.save()
                        created_items.append(new_item.to_sync_dict())
                        
                except Exception as item_error:
                    errors.append(f"Error processing item: {str(item_error)}")
                    continue
            
            sync_result = {
                'updated_data': updated_items + created_items,
                'created_count': len(created_items),
                'updated_count': len(updated_items),
                'errors': errors,
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Sync completed for user {user_id}: {len(created_items)} created, {len(updated_items)} updated")
            
            return sync_result
            
        except Exception as e:
            logger.error(f"Error processing sync data for user {user_id}: {str(e)}")
            raise e
    
    def get_sync_status(self, user_id):
        """Lấy trạng thái đồng bộ của user"""
        try:
            # Đếm tổng số data
            total_count = AppData.get_user_data_count(user_id)
            
            # Lấy data gần đây nhất
            recent_data = AppData.query.filter_by(user_id=user_id)\
                                    .order_by(AppData.updated_at.desc())\
                                    .first()
            
            last_activity = None
            if recent_data:
                last_activity = recent_data.updated_at.isoformat()
            
            # Thống kê theo type
            type_stats = {}
            all_data = AppData.find_by_user_id(user_id)
            for item in all_data:
                if item.type in type_stats:
                    type_stats[item.type] += 1
                else:
                    type_stats[item.type] = 1
            
            return {
                'user_id': user_id,
                'total_items': total_count,
                'last_activity': last_activity,
                'type_statistics': type_stats,
                'sync_status': 'active' if total_count > 0 else 'empty',
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting sync status for user {user_id}: {str(e)}")
            raise e
    
    def force_full_sync(self, user_id):
        """Buộc đồng bộ toàn bộ dữ liệu"""
        try:
            # Lấy tất cả data của user
            all_data = AppData.find_by_user_id(user_id)
            
            # Chuyển đổi thành sync format
            sync_data = []
            for item in all_data:
                sync_data.append(item.to_sync_dict())
            
            # Cập nhật timestamp cho tất cả items
            for item in all_data:
                item.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            result = {
                'data': sync_data,
                'total_synced': len(sync_data),
                'sync_type': 'force_full',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            logger.info(f"Force full sync completed for user {user_id}: {len(sync_data)} items")
            
            return result
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in force full sync for user {user_id}: {str(e)}")
            raise e
    
    def get_sync_conflicts(self, user_id, client_data):
        """Kiểm tra xung đột đồng bộ"""
        try:
            conflicts = []
            
            for client_item in client_data:
                item_id = client_item.get('id')
                if item_id:
                    server_item = AppData.find_by_id(item_id)
                    if server_item and server_item.is_owned_by(user_id):
                        # So sánh timestamp
                        client_updated = client_item.get('updated_at')
                        if client_updated:
                            try:
                                client_datetime = datetime.fromisoformat(client_updated.replace('Z', '+00:00'))
                                if server_item.updated_at > client_datetime:
                                    conflicts.append({
                                        'item_id': item_id,
                                        'server_version': server_item.to_sync_dict(),
                                        'client_version': client_item,
                                        'conflict_type': 'timestamp_mismatch'
                                    })
                            except ValueError:
                                continue
            
            return {
                'conflicts': conflicts,
                'conflict_count': len(conflicts),
                'has_conflicts': len(conflicts) > 0
            }
            
        except Exception as e:
            logger.error(f"Error checking sync conflicts for user {user_id}: {str(e)}")
            raise e
    
    def cleanup_old_data(self, days_old=30):
        """Dọn dẹp dữ liệu cũ (có thể chạy định kỳ)"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            
            old_items = AppData.query.filter(AppData.created_at < cutoff_date).all()
            
            deleted_count = 0
            for item in old_items:
                item.delete()
                deleted_count += 1
            
            logger.info(f"Cleaned up {deleted_count} old data items (older than {days_old} days)")
            
            return {
                'deleted_count': deleted_count,
                'cutoff_date': cutoff_date.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {str(e)}")
            raise e
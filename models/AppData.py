# Mô hình dữ liệu App Data
from config.db import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class AppData(db.Model):
    """Model cho bảng app_data"""
    __tablename__ = 'app_data'
    
    # Các cột
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # Loại dữ liệu: note, task, message, etc.
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=False)  # Nội dung chính (JSON string hoặc text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, user_id, type, content, title=None):
        """Khởi tạo AppData"""
        self.user_id = user_id
        self.type = type
        self.title = title
        self.content = content
    
    def __repr__(self):
        """String representation"""
        return f'<AppData {self.id}: {self.type}>'
    
    def to_dict(self):
        """Chuyển đổi object thành dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_sync_dict(self):
        """Chuyển đổi object cho đồng bộ (không bao gồm user_id)"""
        return {
            'id': self.id,
            'type': self.type,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def find_by_id(cls, data_id):
        """Tìm data theo ID"""
        return cls.query.get(data_id)
    
    @classmethod
    def find_by_user_id(cls, user_id):
        """Tìm tất cả data của user"""
        return cls.query.filter_by(user_id=user_id).order_by(cls.created_at.desc()).all()
    
    @classmethod
    def find_by_user_and_type(cls, user_id, data_type):
        """Tìm data theo user và type"""
        return cls.query.filter_by(user_id=user_id, type=data_type)\
                      .order_by(cls.created_at.desc()).all()
    
    @classmethod
    def find_by_user_since(cls, user_id, since_datetime):
        """Tìm data của user từ thời điểm cụ thể"""
        return cls.query.filter(
            cls.user_id == user_id,
            cls.updated_at > since_datetime
        ).order_by(cls.updated_at.desc()).all()
    
    @classmethod
    def get_user_data_count(cls, user_id):
        """Đếm số lượng data của user"""
        return cls.query.filter_by(user_id=user_id).count()
    
    @classmethod
    def get_user_data_by_type_count(cls, user_id, data_type):
        """Đếm số lượng data của user theo type"""
        return cls.query.filter_by(user_id=user_id, type=data_type).count()
    
    def save(self):
        """Lưu data vào database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update(self, **kwargs):
        """Cập nhật data"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key) and key not in ['id', 'user_id', 'created_at']:
                    setattr(self, key, value)
            
            self.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Xóa data"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def is_owned_by(self, user_id):
        """Kiểm tra data có thuộc về user không"""
        return self.user_id == user_id
    
    def get_age_in_minutes(self):
        """Lấy tuổi của data tính bằng phút"""
        if self.created_at:
            delta = datetime.utcnow() - self.created_at
            return delta.total_seconds() / 60
        return 0
    
    def is_recent(self, minutes=60):
        """Kiểm tra data có được tạo trong vòng x phút không"""
        return self.get_age_in_minutes() <= minutes
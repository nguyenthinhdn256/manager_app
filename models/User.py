# Mô hình dữ liệu User (MongoDB/Mongoose hoặc Sequelize/PostgreSQL)
from config.db import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class User(db.Model):
    """Model cho bảng users"""
    __tablename__ = 'users'
    
    # Các cột
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    app_data = relationship("AppData", backref="user", lazy=True, cascade="all, delete-orphan")
    
    def __init__(self, username, email, password):
        """Khởi tạo User"""
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        """String representation"""
        return f'<User {self.username}>'
    
    def to_dict(self):
        """Chuyển đổi object thành dictionary"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_public_dict(self):
        """Chuyển đổi object thành dictionary (public info only)"""
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    @classmethod
    def find_by_username(cls, username):
        """Tìm user theo username"""
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_email(cls, email):
        """Tìm user theo email"""
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def find_by_id(cls, user_id):
        """Tìm user theo ID"""
        return cls.query.get(user_id)
    
    def save(self):
        """Lưu user vào database"""
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def update(self, **kwargs):
        """Cập nhật thông tin user"""
        try:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            
            self.updated_at = datetime.utcnow()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def delete(self):
        """Xóa user"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def get_data_count(self):
        """Lấy số lượng dữ liệu của user"""
        return len(self.app_data)
    
    def get_recent_data(self, limit=5):
        """Lấy dữ liệu gần đây của user"""
        from models.AppData import AppData
        return AppData.query.filter_by(user_id=self.id)\
                          .order_by(AppData.created_at.desc())\
                          .limit(limit).all()
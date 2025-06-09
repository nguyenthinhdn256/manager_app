# Khởi chạy server
import os
from app import app, socketio
from utils.logger import logger

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    logger.info(f"🚀 Server đang khởi động tại http://localhost:{port}")
    logger.info(f"📱 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"🔗 API Base URL: http://localhost:{port}/api")
    
    # Chạy với SocketIO
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=port, 
        debug=debug,
        allow_unsafe_werkzeug=True
    )

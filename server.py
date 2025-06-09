# Khởi chạy server
import os
from app import app, socketio
from utils.logger import logger

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    is_production = os.environ.get('FLASK_ENV') == 'production'

    # Production URL
    if is_production:
        base_url = f"https://manager-app-744c.onrender.com"
    else:
        base_url = f"http://localhost:{port}"
    
    logger.info(f"🚀 Server đang khởi động tại {base_url}")
    logger.info(f"📱 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    logger.info(f"🔗 API Base URL: {base_url}/api")
    
    # Chạy với SocketIO
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=port, 
        debug=debug,
        allow_unsafe_werkzeug=True
    )

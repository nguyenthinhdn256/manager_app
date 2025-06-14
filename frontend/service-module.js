<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dịch vụ - SpaViet</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
        }

        /* Header styles */
        .header {
            background: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .logo-section {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .logo {
            width: 24px;
            height: 24px;
            background: linear-gradient(135deg, #2563eb, #10b981);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }

        .app-name {
            font-size: 16px;
            font-weight: 700;
            color: #1f2937;
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .notification-btn, .message-btn {
            background: none;
            border: none;
            font-size: 16px;
            color: #6b7280;
            cursor: pointer;
            padding: 6px;
            border-radius: 6px;
            transition: background-color 0.2s;
        }

        .notification-btn:hover, .message-btn:hover {
            background-color: #f3f4f6;
        }

        /* Service group buttons - AUTO SIZE */
        .service-group-btn {
            background: white !important;
            color: #3b82f6 !important;
            border: 1px solid #3b82f6 !important;
            border-radius: 15px !important;
            padding: 6px 12px !important;
            font-size: 12px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            margin: 6px !important;
            height: auto !important;
            width: auto !important;
            min-width: auto !important;
            max-width: none !important;
            display: inline-block !important;
            white-space: nowrap !important;
            box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1) !important;
        }

        .service-group-btn:hover {
            background: #eff6ff !important;
            transform: translateY(-1px);
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
        }

        .service-group-btn:active {
            transform: scale(0.98);
        }

        /* Action buttons */
        .action-btn {
            background: linear-gradient(135deg, #4F46E5, #7C3AED);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
            transition: all 0.3s ease;
        }

        .action-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);
        }

        /* Bottom navigation */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            border-top: 1px solid #e5e7eb;
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            padding: 6px 0;
        }

        .nav-item {
            text-align: center;
            padding: 4px;
            color: #6b7280;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 2px;
            font-size: 10px;
            cursor: pointer;
            height: 50px;
        }

        .nav-item.active {
            color: #2563eb;
        }

        .nav-icon {
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div style="min-height: 100vh; background: #f5f5f5;">
        <!-- Header -->
        <div class="header">
            <div class="logo-section">
                <div class="logo">S</div>
                <div class="app-name">SpaViet</div>
            </div>
            <div class="header-right">
                <button class="notification-btn" onclick="alert('🔔 Thông báo!')">🔔</button>
                <button class="message-btn" onclick="alert('✉️ Tin nhắn!')">✉️</button>
            </div>
        </div>

        <!-- Service Page Content -->
        <div style="padding: 20px; padding-bottom: 80px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                <h1 style="font-size: 24px; font-weight: 700; color: #1f2937; margin: 0;">Dịch vụ</h1>
                
                <!-- Service Actions Buttons -->
                <div style="display: flex; gap: 15px;">
                    <button class="action-btn" onclick="alert('Tạo Nhóm DV')">Tạo Nhóm DV</button>
                    <button class="action-btn" onclick="alert('Tạo DV')">Tạo DV</button>
                </div>
            </div>

            <!-- Service Groups Grid -->
            <div style="display: flex; flex-wrap: wrap; gap: 8px; justify-content: flex-start; margin-top: 20px;">
                <button class="service-group-btn" onclick="selectGroup('GỘI ĐẦU')">GỘI ĐẦU</button>
                <button class="service-group-btn" onclick="selectGroup('SỨC KHỎE')">SỨC KHỎE</button>
                <button class="service-group-btn" onclick="selectGroup('CHĂM SÓC MẶT')">CHĂM SÓC MẶT</button>
                <button class="service-group-btn" onclick="selectGroup('CHĂM SÓC TÓC')">CHĂM SÓC TÓC</button>
                <button class="service-group-btn" onclick="selectGroup('COMBO PH SỨC KHỎE')">COMBO PH SỨC KHỎE</button>
            </div>

            <!-- Description -->
            <div style="text-align: center; margin-top: 40px; color: #6b7280; font-size: 14px; line-height: 1.6;">
                <p><strong>Tạo Nhóm DV:</strong> Tạo nhóm dịch vụ mới</p>
                <p><strong>Tạo DV:</strong> Thêm dịch vụ mới vào hệ thống</p>
                <p style="margin-top: 10px;"><em>Click vào nhóm dịch vụ để xem chi tiết</em></p>
            </div>
        </div>

        <!-- Bottom Navigation -->
        <div class="bottom-nav">
            <div class="nav-item" onclick="alert('Tổng quan')">
                <div class="nav-icon">🏠</div>
                <div>Tổng quan</div>
            </div>
            <div class="nav-item" onclick="alert('Khách hàng')">
                <div class="nav-icon">👥</div>
                <div>Khách hàng</div>
            </div>
            <div class="nav-item active">
                <div class="nav-icon">💆‍♀️</div>
                <div>Dịch vụ</div>
            </div>
            <div class="nav-item" onclick="alert('Hóa đơn')">
                <div class="nav-icon">📋</div>
                <div>Hóa đơn</div>
            </div>
            <div class="nav-item" onclick="alert('Nhiều hơn')">
                <div class="nav-icon">☰</div>
                <div>Nhiều hơn</div>
            </div>
        </div>
    </div>

    <script>
        function selectGroup(groupName) {
            alert(`Đã chọn nhóm: ${groupName}`);
            
            // Add visual feedback
            const button = event.target;
            const originalBg = button.style.background;
            button.style.background = '#dbeafe';
            
            setTimeout(() => {
                button.style.background = originalBg;
            }, 200);
        }
    </script>
</body>
</html>

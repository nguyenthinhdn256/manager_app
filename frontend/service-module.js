// ===== SERVICE MODULE =====
// Module xử lý toàn bộ logic giao diện dịch vụ

const ServiceModule = (function() {
    'use strict';

    // ===== PRIVATE VARIABLES =====
    let services = [];

    // ===== UI RENDERING =====
    function showServicePage() {
        console.log('💆‍♀️ Showing service page');
        
        document.body.innerHTML = `
            <div style="
                min-height: 100vh;
                background: #f5f5f5;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            ">
                <!-- Header -->
                <div class="header">
                    <div class="logo-section">
                        <div class="logo">S</div>
                        <div class="app-name">SpaViet</div>
                    </div>
                    <div class="header-right">
                        <button class="notification-btn" onclick="showNotifications()">🔔</button>
                        <button class="message-btn" onclick="showMessages()">✉️</button>
                    </div>
                </div>

                <!-- Service Page Content -->
                <div style="padding: 20px; padding-bottom: 80px;">
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 30px;
                    ">
                        <h1 style="font-size: 24px; font-weight: 700; color: #1f2937; margin: 0;">Dịch vụ</h1>
                        
                        <!-- Service Actions Buttons -->
                        <div style="display: flex; gap: 15px; margin-left: auto;">
                            <!-- Menu DV Button -->
                            <button onclick="ServiceModule.showMenuDV()" style="
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
                            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 10px 25px rgba(79, 70, 229, 0.3)'" 
                               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(79, 70, 229, 0.2)'">
                                Menu DV
                            </button>

                            <!-- Tạo DV Button -->
                            <button onclick="ServiceModule.showCreateDV()" style="
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
                            " onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 10px 25px rgba(79, 70, 229, 0.3)'" 
                               onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 2px 4px rgba(79, 70, 229, 0.2)'">
                                Tạo DV
                            </button>
                        </div>
                    </div>

                    <!-- Description -->
                    <div style="
                        text-align: center;
                        margin-top: 40px;
                        color: #6b7280;
                        font-size: 14px;
                        line-height: 1.6;
                    ">
                        <p><strong>Menu DV:</strong> Xem danh sách tất cả dịch vụ có sẵn</p>
                        <p><strong>Tạo DV:</strong> Thêm dịch vụ mới vào hệ thống</p>
                    </div>
                </div>

                <!-- Bottom Navigation -->
                <div class="bottom-nav">
                    <div class="nav-item" onclick="showSection('overview')">
                        <div class="nav-icon">🏠</div>
                        <div>Tổng quan</div>
                    </div>
                    <div class="nav-item" onclick="showSection('customers')">
                        <div class="nav-icon">👥</div>
                        <div>Khách hàng</div>
                    </div>
                    <div class="nav-item active" onclick="showSection('services')">
                        <div class="nav-icon">💆‍♀️</div>
                        <div>Dịch vụ</div>
                    </div>
                    <div class="nav-item" onclick="showSection('orders')">
                        <div class="nav-icon">📋</div>
                        <div>Hóa đơn</div>
                    </div>
                    <div class="nav-item" onclick="showSection('more')">
                        <div class="nav-icon">☰</div>
                        <div>Nhiều hơn</div>
                    </div>
                </div>
            </div>
        `;
    }

    // ===== SERVICE ACTIONS =====
    function showMenuDV() {
        console.log('📋 Menu DV clicked');
        // Placeholder for future implementation
        if (typeof showAlert !== 'undefined') {
            showAlert('Chức năng "Menu DV" đang được phát triển...', 'Menu Dịch vụ', '📋');
        } else {
            alert('Chức năng "Menu DV" đang được phát triển...');
        }
    }

    function showCreateDV() {
        console.log('➕ Tạo DV clicked');
        // Placeholder for future implementation
        if (typeof showAlert !== 'undefined') {
            showAlert('Chức năng "Tạo DV" đang được phát triển...', 'Tạo Dịch vụ', '➕');
        } else {
            alert('Chức năng "Tạo DV" đang được phát triển...');
        }
    }

    // ===== INITIALIZATION =====
    function init() {
        services = []; // Initialize empty services array
        console.log('🎯 Service Module initialized');
    }

    // ===== PUBLIC API =====
    return {
        // Initialization
        init: init,
        
        // Main functions
        showServicePage: showServicePage,
        
        // Service actions
        showMenuDV: showMenuDV,
        showCreateDV: showCreateDV,
        
        // Data access (for future use)
        getServices: () => [...services], // Return copy
        getServiceCount: () => services.length
    };
})();

// ===== AUTO INITIALIZATION =====
// Initialize module when loaded
ServiceModule.init();

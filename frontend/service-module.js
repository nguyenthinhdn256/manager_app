// ===== SERVICE MODULE =====
// Module xử lý toàn bộ logic giao diện dịch vụ

const ServiceModule = (function() {
    'use strict';

    // ===== PRIVATE VARIABLES =====
    let services = [];
    let serviceGroups = [
        { id: 1, name: 'GỘI ĐẦU' },
        { id: 2, name: 'SỨC KHỎE' },
        { id: 3, name: 'CHĂM SÓC MẶT' },
        { id: 4, name: 'CHĂM SÓC TÓC' },
        { id: 5, name: 'COMBO PH SỨC KHỎE' }
    ];

    // ===== UI RENDERING =====
    function renderServiceGroups() {
        return serviceGroups.map(group => `
            <button onclick="ServiceModule.selectServiceGroup(${group.id})" style="
                background: white;
                color: #3b82f6;
                border: 1px solid #3b82f6;
                border-radius: 6px;
                padding: 3px 8px;
                font-size: 10px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                margin: 4px;
                height: 20px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                white-space: nowrap;
                box-shadow: 0 1px 2px rgba(59, 130, 246, 0.1);
                width: auto;
                min-width: fit-content;
            " onmouseover="this.style.background='#eff6ff'; this.style.transform='translateY(-1px)'" 
               onmouseout="this.style.background='white'; this.style.transform='translateY(0)'"
               onmousedown="this.style.transform='scale(0.98)'"
               onmouseup="this.style.transform='scale(1)'">
                ${group.name}
            </button>
        `).join('');
    }

    function showServicePage() {
        console.log('💆‍♀️ Showing service page');
        
        const serviceGroupsHTML = renderServiceGroups();
        
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
                            <!-- Tạo Nhóm DV Button -->
                            <button onclick="ServiceModule.showCreateGroupModal()" style="
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
                                Tạo Nhóm DV
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

                    <!-- Service Groups Grid -->
                    <div style="
                        display: flex;
                        flex-wrap: wrap;
                        gap: 12px;
                        justify-content: flex-start;
                        margin-top: 20px;
                    ">
                        ${serviceGroupsHTML}
                    </div>

                    <!-- Description -->
                    <div style="
                        text-align: center;
                        margin-top: 40px;
                        color: #6b7280;
                        font-size: 14px;
                        line-height: 1.6;
                    ">
                        <p><strong>Tạo Nhóm DV:</strong> Tạo nhóm dịch vụ mới</p>
                        <p><strong>Tạo DV:</strong> Thêm dịch vụ mới vào hệ thống</p>
                        <p style="margin-top: 10px;"><em>Click vào nhóm dịch vụ để xem chi tiết</em></p>
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
    function showCreateGroupModal() {
        console.log('📋 Tạo Nhóm DV clicked');
        // Placeholder for future implementation
        if (typeof showAlert !== 'undefined') {
            showAlert('Chức năng "Tạo Nhóm DV" đang được phát triển...', 'Tạo Nhóm Dịch vụ', '📋');
        } else {
            alert('Chức năng "Tạo Nhóm DV" đang được phát triển...');
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

    function selectServiceGroup(groupId) {
        const group = serviceGroups.find(g => g.id === groupId);
        console.log('🎯 Service group selected:', group.name);
        
        // Add flash effect
        const buttonElement = event.target;
        buttonElement.style.animation = 'flash 0.3s ease-in-out';
        
        // Remove animation after it completes
        setTimeout(() => {
            buttonElement.style.animation = '';
        }, 300);
        
        // Show group details
        if (typeof showAlert !== 'undefined') {
            showAlert(`Đã chọn nhóm dịch vụ: "${group.name}"\n\nChức năng xem chi tiết nhóm đang được phát triển...`, 'Nhóm Dịch vụ', '💆‍♀️');
        } else {
            alert(`Đã chọn nhóm: ${group.name}`);
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
        showCreateGroupModal: showCreateGroupModal,
        showCreateDV: showCreateDV,
        selectServiceGroup: selectServiceGroup,
        
        // Data access (for future use)
        getServices: () => [...services], // Return copy
        getServiceCount: () => services.length
    };
})();

// ===== AUTO INITIALIZATION =====
// Initialize module when loaded
ServiceModule.init();

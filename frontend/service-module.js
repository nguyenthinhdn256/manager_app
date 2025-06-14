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

    // ===== DATA MANAGEMENT =====
    function loadServiceGroups() {
        // In the future, this could load from API or localStorage
        // For now, return the default groups
        const saved = localStorage.getItem('serviceGroups');
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (error) {
                console.warn('Error parsing saved service groups:', error);
            }
        }
        return [...serviceGroups]; // Return copy of default groups
    }

    function saveServiceGroups() {
        localStorage.setItem('serviceGroups', JSON.stringify(serviceGroups));
    }

    function loadServices() {
        const saved = localStorage.getItem('services');
        if (saved) {
            try {
                return JSON.parse(saved);
            } catch (error) {
                console.warn('Error parsing saved services:', error);
            }
        }
        return []; // Return empty array if no saved services
    }

    function saveServices() {
        localStorage.setItem('services', JSON.stringify(services));
    }

    function findServiceGroupById(groupId) {
        return serviceGroups.find(g => g.id == groupId);
    }

    function generateNewGroupId() {
        return serviceGroups.length > 0 ? Math.max(...serviceGroups.map(g => g.id)) + 1 : 1;
    }

    // ===== UI RENDERING =====
    function renderServiceGroups() {
        return serviceGroups.map(group => `
            <button onclick="ServiceModule.selectServiceGroup(${group.id})" style="
                background: white;
                color: #3b82f6;
                border: 1px solid #3b82f6;
                border-radius: 15px;
                padding: 6px 12px;
                font-size: 12px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                margin: 6px;
                height: auto;
                width: auto;
                min-width: auto;
                max-width: none;
                display: inline-block;
                white-space: nowrap;
                box-shadow: 0 1px 3px rgba(59, 130, 246, 0.1);
            " onmouseover="this.style.background='#eff6ff'; this.style.transform='translateY(-1px)'; this.style.boxShadow='0 2px 8px rgba(59, 130, 246, 0.2)'" 
               onmouseout="this.style.background='white'; this.style.transform='translateY(0)'; this.style.boxShadow='0 1px 3px rgba(59, 130, 246, 0.1)'"
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
            <div style="min-height: 100vh; background: #f5f5f5;">
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
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                        <h1 style="font-size: 24px; font-weight: 700; color: #1f2937; margin: 0;">Dịch vụ</h1>
                        
                        <div style="display: flex; gap: 15px;">
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
                            ">Tạo Nhóm DV</button>
                            <button onclick="ServiceModule.showCreateServiceModal()" style="
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
                            ">Tạo DV</button>
                        </div>
                    </div>

                    <!-- Service Groups Grid -->
                    <div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: flex-start; margin-top: 20px;">
                        ${serviceGroupsHTML}
                    </div>

                    <!-- Description -->
                    <div style="text-align: center; margin-top: 40px; color: #6b7280; font-size: 14px; line-height: 1.6;">
                        <p><strong>Tạo Nhóm DV:</strong> Tạo nhóm dịch vụ mới</p>
                        <p><strong>Tạo DV:</strong> Thêm dịch vụ mới vào hệ thống</p>
                        <p style="margin-top: 10px;"><em>Click vào nhóm dịch vụ để xem chi tiết</em></p>
                        
                        <!-- Statistics -->
                        <div style="margin-top: 20px; padding: 15px; background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);">
                            <div style="display: flex; justify-content: space-around; text-align: center;">
                                <div>
                                    <div style="font-size: 24px; font-weight: 700; color: #3b82f6;">${serviceGroups.length}</div>
                                    <div style="font-size: 12px; color: #6b7280;">Nhóm dịch vụ</div>
                                </div>
                                <div>
                                    <div style="font-size: 24px; font-weight: 700; color: #10b981;">${services.length}</div>
                                    <div style="font-size: 12px; color: #6b7280;">Dịch vụ</div>
                                </div>
                            </div>
                        </div>
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

    // ===== MODAL FUNCTIONS =====
    function showCreateGroupModal() {
        console.log('📋 Tạo Nhóm DV clicked');
        
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal">
                <h2 class="modal-title">Tạo nhóm dịch vụ mới</h2>
                <form id="createGroupForm">
                    <div class="form-group">
                        <label class="form-label">Tên nhóm dịch vụ</label>
                        <input type="text" id="groupName" class="form-input" placeholder="Nhập tên nhóm dịch vụ" required>
                    </div>
                    <div class="modal-buttons">
                        <button type="button" class="btn-cancel" onclick="ServiceModule.closeCreateGroupModal()">Hủy</button>
                        <button type="submit" class="btn-add">Tạo nhóm</button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Focus on first input
        setTimeout(() => {
            document.getElementById('groupName').focus();
        }, 100);
        
        // Handle form submission
        document.getElementById('createGroupForm').addEventListener('submit', function(e) {
            e.preventDefault();
            createNewGroup();
        });
        
        // Close modal when clicking overlay
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeCreateGroupModal();
            }
        });
    }

    function closeCreateGroupModal() {
        const modal = document.querySelector('.modal-overlay');
        if (modal) {
            modal.remove();
        }
    }

    function showCreateServiceModal() {
        console.log('➕ Tạo DV clicked');
        
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal">
                <h2 class="modal-title">Tạo dịch vụ mới</h2>
                <form id="createServiceForm">
                    <div class="form-group">
                        <label class="form-label">Tên dịch vụ</label>
                        <input type="text" id="serviceName" class="form-input" placeholder="Nhập tên dịch vụ" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Nhóm dịch vụ</label>
                        <select id="serviceGroup" class="form-input" required>
                            <option value="">Chọn nhóm dịch vụ</option>
                            ${serviceGroups.map(group => `<option value="${group.id}">${group.name}</option>`).join('')}
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Giá (VNĐ)</label>
                        <input type="number" id="servicePrice" class="form-input" placeholder="Nhập giá dịch vụ" min="0">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Mô tả</label>
                        <textarea id="serviceDescription" class="form-input" placeholder="Mô tả dịch vụ" rows="3" style="resize: vertical; min-height: 80px;"></textarea>
                    </div>
                    <div class="modal-buttons">
                        <button type="button" class="btn-cancel" onclick="ServiceModule.closeCreateServiceModal()">Hủy</button>
                        <button type="submit" class="btn-add">Tạo dịch vụ</button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Focus on first input
        setTimeout(() => {
            document.getElementById('serviceName').focus();
        }, 100);
        
        // Handle form submission
        document.getElementById('createServiceForm').addEventListener('submit', function(e) {
            e.preventDefault();
            createNewService();
        });
        
        // Close modal when clicking overlay
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeCreateServiceModal();
            }
        });
    }

    function closeCreateServiceModal() {
        const modal = document.querySelector('.modal-overlay');
        if (modal) {
            modal.remove();
        }
    }

    // ===== SERVICE ACTIONS =====
    function createNewGroup() {
        const name = document.getElementById('groupName').value.trim();
        
        if (!name) {
            if (typeof showAlert === 'function') {
                showAlert('Vui lòng nhập tên nhóm dịch vụ!', 'Lỗi', '⚠️');
            } else {
                alert('Vui lòng nhập tên nhóm dịch vụ!');
            }
            return;
        }
        
        // Check if group name already exists
        if (serviceGroups.some(group => group.name.toLowerCase() === name.toLowerCase())) {
            if (typeof showAlert === 'function') {
                showAlert('Tên nhóm dịch vụ đã tồn tại!', 'Lỗi', '⚠️');
            } else {
                alert('Tên nhóm dịch vụ đã tồn tại!');
            }
            return;
        }
        
        // Create new group
        const newGroup = {
            id: generateNewGroupId(),
            name: name.toUpperCase()
    })();

// ===== AUTO INITIALIZATION =====
// Initialize module when loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if not already initialized
    if (!ServiceModule._initialized) {
        ServiceModule.init();
        ServiceModule._initialized = true;
    }
});

// Also initialize immediately if DOM already loaded
if (document.readyState === 'loading') {
    // DOM hasn't finished loading yet
    console.log('🔄 ServiceModule: Waiting for DOM...');
} else {
    // DOM is already loaded
    if (!ServiceModule._initialized) {
        ServiceModule.init();
        ServiceModule._initialized = true;
    }
}

console.log('📦 ServiceModule loaded successfully');
        
        serviceGroups.push(newGroup);
        saveServiceGroups();
        
        console.log('✅ New service group created:', newGroup);
        
        // Close modal
        closeCreateGroupModal();
        
        // Refresh service page
        showServicePage();
        
        // Show success message
        setTimeout(() => {
            if (typeof showAlert === 'function') {
                showAlert(`Đã tạo thành công nhóm dịch vụ: ${name}`, 'Thành công', '✅');
            } else {
                alert(`Đã tạo thành công nhóm dịch vụ: ${name}`);
            }
        }, 300);
    }

    function createNewService() {
        const name = document.getElementById('serviceName').value.trim();
        const groupId = parseInt(document.getElementById('serviceGroup').value);
        const price = parseFloat(document.getElementById('servicePrice').value) || 0;
        const description = document.getElementById('serviceDescription').value.trim();
        
        if (!name) {
            if (typeof showAlert === 'function') {
                showAlert('Vui lòng nhập tên dịch vụ!', 'Lỗi', '⚠️');
            } else {
                alert('Vui lòng nhập tên dịch vụ!');
            }
            return;
        }
        
        if (!groupId) {
            if (typeof showAlert === 'function') {
                showAlert('Vui lòng chọn nhóm dịch vụ!', 'Lỗi', '⚠️');
            } else {
                alert('Vui lòng chọn nhóm dịch vụ!');
            }
            return;
        }
        
        // Create new service
        const newService = {
            id: services.length > 0 ? Math.max(...services.map(s => s.id)) + 1 : 1,
            name: name,
            groupId: groupId,
            price: price,
            description: description || 'Không có mô tả',
            createdAt: new Date().toISOString()
        };
        
        services.push(newService);
        saveServices();
        
        console.log('✅ New service created:', newService);
        
        // Close modal
        closeCreateServiceModal();
        
        // Refresh service page
        showServicePage();
        
        // Show success message
        setTimeout(() => {
            const group = findServiceGroupById(groupId);
            if (typeof showAlert === 'function') {
                showAlert(`Đã tạo thành công dịch vụ: ${name}\nNhóm: ${group ? group.name : 'Không xác định'}`, 'Thành công', '✅');
            } else {
                alert(`Đã tạo thành công dịch vụ: ${name}`);
            }
        }, 300);
    }

    function selectServiceGroup(groupId) {
        const group = findServiceGroupById(groupId);
        const groupServices = services.filter(s => s.groupId == groupId);
        
        console.log('🎯 Service group selected:', group.name);
        
        // Add visual feedback
        const buttonElement = event.target;
        const originalBg = buttonElement.style.background;
        buttonElement.style.background = '#dbeafe';
        
        setTimeout(() => {
            buttonElement.style.background = originalBg;
        }, 200);
        
        // Show group details
        let message = `Nhóm dịch vụ: "${group.name}"\n`;
        message += `Số lượng dịch vụ: ${groupServices.length}\n\n`;
        
        if (groupServices.length > 0) {
            message += `Danh sách dịch vụ:\n`;
            groupServices.forEach((service, index) => {
                message += `${index + 1}. ${service.name}`;
                if (service.price > 0) {
                    message += ` - ${service.price.toLocaleString('vi-VN')} VNĐ`;
                }
                message += `\n`;
            });
        } else {
            message += `Chưa có dịch vụ nào trong nhóm này.`;
        }
        
        if (typeof showAlert === 'function') {
            showAlert(message, 'Thông tin nhóm dịch vụ', '💆‍♀️');
        } else {
            alert(message);
        }
    }

    // ===== INITIALIZATION =====
    function init() {
        serviceGroups = loadServiceGroups();
        services = loadServices();
        console.log('🎯 Service Module initialized');
        console.log(`📊 Service groups: ${serviceGroups.length}, Services: ${services.length}`);
        
        // Check if running in standalone mode (without main app)
        if (typeof showAlert !== 'function') {
            console.warn('⚠️ Service Module running without main app utilities');
        }
    }

    // ===== PUBLIC API =====
    return {
        // Initialization
        init: init,
        
        // Main functions
        showServicePage: showServicePage,
        
        // Modal functions
        showCreateGroupModal: showCreateGroupModal,
        closeCreateGroupModal: closeCreateGroupModal,
        showCreateServiceModal: showCreateServiceModal,
        closeCreateServiceModal: closeCreateServiceModal,
        
        // Service actions
        selectServiceGroup: selectServiceGroup,
        createNewGroup: createNewGroup,
        createNewService: createNewService,
        
        // Data access
        getServices: () => [...services],
        getServiceGroups: () => [...serviceGroups],
        getServiceCount: () => services.length,
        getGroupCount: () => serviceGroups.length,
        getServicesByGroup: (groupId) => services.filter(s => s.groupId == groupId),
        
        // Direct data manipulation (for API integration later)
        addServiceGroup: (groupData) => {
            const newGroup = {
                id: generateNewGroupId(),
                ...groupData
            };
            serviceGroups.push(newGroup);
            saveServiceGroups();
            return newGroup;
        },
        
        addService: (serviceData) => {
            const newService = {
                id: services.length > 0 ? Math.max(...services.map(s => s.id)) + 1 : 1,
                ...serviceData,
                createdAt: new Date().toISOString()
            };
            services.push(newService);
            saveServices();
            return newService;
        },
        
        updateService: (serviceId, updates) => {
            const serviceIndex = services.findIndex(s => s.id == serviceId);
            if (serviceIndex !== -1) {
                services[serviceIndex] = { ...services[serviceIndex], ...updates };
                saveServices();
                return services[serviceIndex];
            }
            return null;
        },
        
        removeService: (serviceId) => {
            const initialLength = services.length;
            services = services.filter(s => s.id != serviceId);
            saveServices();
            return services.length < initialLength;
        }
    };

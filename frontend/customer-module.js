// ===== CUSTOMER MODULE =====
// Module xử lý toàn bộ logic giao diện khách hàng

const CustomerModule = (function() {
    'use strict';

    // ===== PRIVATE VARIABLES =====
    let customers = [];

    // ===== UTILITY FUNCTIONS =====
    function formatTime(isoString) {
        const date = new Date(isoString);
        const now = new Date();
        
        // Format: HH:MM DD/MM/YYYY
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();
        
        // Check if it's today
        const isToday = date.toDateString() === now.toDateString();
        
        if (isToday) {
            return `${hours}:${minutes} hôm nay`;
        } else {
            return `${hours}:${minutes} ${day}/${month}/${year}`;
        }
    }

    function formatTimeDetailed(isoString) {
        const date = new Date(isoString);
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();
        
        return `${hours}:${minutes}:${seconds} - ${day}/${month}/${year}`;
    }

    function getInitials(name) {
        return name.split(' ').map(word => word[0]).join('').toUpperCase().slice(0, 2);
    }

    // ===== DATA MANAGEMENT =====
    function loadCustomers() {
        const saved = localStorage.getItem('customers');
        if (saved) {
            return JSON.parse(saved);
        }
        // Default customers if no saved data
        return [
            {
                id: 1,
                name: 'Nguyễn Văn An',
                phone: '0901234567',
                features: 'Khách VIP, thích massage',
                createdAt: new Date('2025-06-10T10:30:25').toISOString()
            },
            {
                id: 2,
                name: 'Trần Thị Bình',
                phone: '0912345678',
                features: 'Da nhạy cảm',
                createdAt: new Date('2025-06-11T14:15:42').toISOString()
            },
            {
                id: 3,
                name: 'Lê Hoàng Cường',
                phone: '0923456789',
                features: 'Thể thao, cần thư giãn',
                createdAt: new Date('2025-06-12T09:45:18').toISOString()
            },
            {
                id: 4,
                name: 'Phạm Thị Dung',
                phone: '0934567890',
                features: 'Chăm sóc da mặt',
                createdAt: new Date('2025-06-13T16:20:33').toISOString()
            },
            {
                id: 5,
                name: 'Hoàng Văn Em',
                phone: '0945678901',
                features: 'Khách thường xuyên',
                createdAt: new Date('2025-06-14T11:00:07').toISOString()
            }
        ];
    }

    function saveCustomers() {
        localStorage.setItem('customers', JSON.stringify(customers));
    }

    function findCustomerById(customerId) {
        return customers.find(c => c.id == customerId);
    }

    function generateNewId() {
        return customers.length > 0 ? Math.max(...customers.map(c => c.id)) + 1 : 1;
    }

    // ===== UI RENDERING =====
    function renderCustomerList() {
        return customers.map(customer => `
            <div class="customer-item" onclick="CustomerModule.viewCustomer('${customer.id}')">
                <div class="customer-avatar">${getInitials(customer.name)}</div>
                <div class="customer-info">
                    <div class="customer-name">${customer.name}</div>
                    <div class="customer-details">${customer.features}</div>
                    <div class="customer-phone">${customer.phone}</div>
                </div>
                <div class="customer-time">${formatTime(customer.createdAt)}</div>
            </div>
        `).join('');
    }

    function showCustomerPage() {
        console.log('👥 Showing customer page');
        
        const customerListHTML = renderCustomerList();
        
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
    
                <!-- Customer Page Content -->
                <div style="padding: 20px; padding-bottom: 80px;">
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        margin-bottom: 20px;
                    ">
                        <h1 style="font-size: 24px; font-weight: 700; color: #1f2937; margin: 0;">Khách hàng</h1>
                        <button onclick="CustomerModule.showAddCustomerModal()" style="
                            background: linear-gradient(135deg, #4F46E5, #7C3AED);
                            color: white;
                            border: none;
                            border-radius: 12px;
                            padding: 12px 20px;
                            font-size: 14px;
                            font-weight: 600;
                            cursor: pointer;
                            box-shadow: 0 2px 4px rgba(79, 70, 229, 0.2);
                        ">Thêm khách hàng mới</button>
                    </div>
    
                    <!-- Customer List -->
                    <div style="
                        background: white;
                        border-radius: 16px;
                        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                    ">
                        ${customerListHTML}
                    </div>
                </div>
    
                <!-- Bottom Navigation -->
                <div class="bottom-nav">
                    <div class="nav-item" onclick="showSection('overview')">
                        <div class="nav-icon">🏠</div>
                        <div>Tổng quan</div>
                    </div>
                    <div class="nav-item active" onclick="showSection('customers')">
                        <div class="nav-icon">👥</div>
                        <div>Khách hàng</div>
                    </div>
                    <div class="nav-item" onclick="showSection('services')">
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
    function showAddCustomerModal() {
        console.log('🎯 showAddCustomerModal called');
        const modal = document.createElement('div');
        modal.className = 'modal-overlay';
        modal.innerHTML = `
            <div class="modal">
                <h2 class="modal-title">Thông tin khách hàng</h2>
                <form id="addCustomerForm">
                    <div class="form-group">
                        <label class="form-label">Tên KH</label>
                        <input type="text" id="customerName" class="form-input" placeholder="Nhập tên khách hàng" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Đặc điểm</label>
                        <input type="text" id="customerFeatures" class="form-input" placeholder="Nhập đặc điểm khách hàng">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Phone</label>
                        <input type="tel" id="customerPhone" class="form-input" placeholder="Nhập số điện thoại">
                    </div>
                    <div class="modal-buttons">
                        <button type="button" class="btn-cancel" onclick="CustomerModule.closeAddCustomerModal()">Hủy</button>
                        <button type="submit" class="btn-add">Thêm</button>
                    </div>
                </form>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Focus on first input
        setTimeout(() => {
            document.getElementById('customerName').focus();
        }, 100);
        
        // Handle form submission
        document.getElementById('addCustomerForm').addEventListener('submit', function(e) {
            e.preventDefault();
            addNewCustomer();
        });
        
        // Close modal when clicking overlay
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeAddCustomerModal();
            }
        });
    }

    function closeAddCustomerModal() {
        const modal = document.querySelector('.modal-overlay');
        if (modal) {
            modal.remove();
        }
    }

    function showCustomerInfoModal(customer) {
        // Remove existing modal if any
        const existingModal = document.querySelector('.alert-overlay');
        if (existingModal) {
            existingModal.remove();
        }

        const modalOverlay = document.createElement('div');
        modalOverlay.className = 'alert-overlay';
        modalOverlay.innerHTML = `
            <div class="alert-modal customer-info-modal">
                <button class="modal-close" onclick="CustomerModule.closeCustomerInfoModal()">×</button>
                <div class="alert-icon">👤</div>
                <div class="alert-title">Thông tin khách hàng</div>
                <div class="alert-message">Tên: ${customer.name}
Đặc điểm: ${customer.features}
Phone: ${customer.phone}
Tạo lúc: ${formatTimeDetailed(customer.createdAt)}</div>
                <div class="customer-modal-buttons">
                    <button class="customer-btn btn-add-service" onclick="CustomerModule.addService(${customer.id})">Thêm DV</button>
                    <button class="customer-btn btn-payment" onclick="CustomerModule.makePayment(${customer.id})">Thanh toán</button>
                    <button class="customer-btn btn-edit" onclick="CustomerModule.editCustomer(${customer.id})">Sửa</button>
                    <button class="customer-btn btn-delete" onclick="CustomerModule.deleteCustomer(${customer.id})">Xóa</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(modalOverlay);
        
        // Close modal when clicking overlay
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) {
                closeCustomerInfoModal();
            }
        });
    }

    function closeCustomerInfoModal() {
        const modalOverlay = document.querySelector('.alert-overlay');
        if (modalOverlay) {
            modalOverlay.remove();
        }
    }

    // ===== CUSTOMER ACTIONS =====
    function addNewCustomer() {
        const name = document.getElementById('customerName').value.trim();
        const features = document.getElementById('customerFeatures').value.trim();
        const phone = document.getElementById('customerPhone').value.trim();
        
        if (!name) {
            // Use global showAlert function
            if (typeof showAlert === 'function') {
                showAlert('Vui lòng nhập tên khách hàng!', 'Lỗi', '⚠️');
            } else {
                alert('Vui lòng nhập tên khách hàng!');
            }
            return;
        }
        
        // Create new customer with unique ID
        const newCustomer = {
            id: generateNewId(),
            name: name,
            phone: phone || 'Chưa có SĐT',
            features: features || 'Khách hàng mới',
            createdAt: new Date().toISOString()
        };
        
        // Add to customers array
        customers.unshift(newCustomer); // Add to beginning of array
        
        // Save to localStorage
        saveCustomers();
        
        console.log('✅ New customer added:', newCustomer);
        
        // Close modal
        closeAddCustomerModal();
        
        // Refresh customer page
        showCustomerPage();
        
        // Show success message
        setTimeout(() => {
            if (typeof showAlert === 'function') {
                showAlert(`Đã thêm thành công khách hàng: ${name}`, 'Thành công', '✅');
            } else {
                alert(`Đã thêm thành công khách hàng: ${name}`);
            }
        }, 300);
    }

    function viewCustomer(customerId) {
        const customer = findCustomerById(customerId);
        if (customer) {
            showCustomerInfoModal(customer);
        }
    }

    function addService(customerId) {
        closeCustomerInfoModal();
        if (typeof showAlert === 'function') {
            showAlert('Chức năng "Thêm dịch vụ" đang được phát triển...', 'Thêm dịch vụ', '💆‍♀️');
        } else {
            alert('Chức năng "Thêm dịch vụ" đang được phát triển...');
        }
    }

    function makePayment(customerId) {
        closeCustomerInfoModal();
        if (typeof showAlert === 'function') {
            showAlert('Chức năng "Thanh toán" đang được phát triển...', 'Thanh toán', '💳');
        } else {
            alert('Chức năng "Thanh toán" đang được phát triển...');
        }
    }

    function editCustomer(customerId) {
        closeCustomerInfoModal();
        if (typeof showAlert === 'function') {
            showAlert('Chức năng "Sửa thông tin" đang được phát triển...', 'Sửa thông tin', '✏️');
        } else {
            alert('Chức năng "Sửa thông tin" đang được phát triển...');
        }
    }

    function deleteCustomer(customerId) {
        const customer = findCustomerById(customerId);
        if (customer) {
            closeCustomerInfoModal();
            // Show custom confirm dialog
            if (typeof showConfirmDialog === 'function') {
                showConfirmDialog(
                    `Bạn có chắc muốn xóa khách hàng "${customer.name}"?`,
                    'Xác nhận xóa',
                    '🗑️',
                    function() {
                        // Confirm delete
                        customers = customers.filter(c => c.id != customerId);
                        saveCustomers();
                        showCustomerPage();
                        if (typeof showAlert === 'function') {
                            showAlert(`Đã xóa khách hàng "${customer.name}"`, 'Xóa thành công', '✅');
                        } else {
                            alert(`Đã xóa khách hàng "${customer.name}"`);
                        }
                    }
                );
            } else {
                // Fallback to browser confirm
                if (confirm(`Bạn có chắc muốn xóa khách hàng "${customer.name}"?`)) {
                    customers = customers.filter(c => c.id != customerId);
                    saveCustomers();
                    showCustomerPage();
                    alert(`Đã xóa khách hàng "${customer.name}"`);
                }
            }
        }
    }

    // ===== INITIALIZATION =====
    function init() {
        customers = loadCustomers();
        console.log('🎯 Customer Module initialized with', customers.length, 'customers');
        
        // Check if running in standalone mode (without main app)
        if (typeof showAlert !== 'function') {
            console.warn('⚠️ Customer Module running without main app utilities');
        }
    }

    // ===== PUBLIC API =====
    return {
        // Initialization
        init: init,
        
        // Main functions
        showCustomerPage: showCustomerPage,
        
        // Modal functions
        showAddCustomerModal: showAddCustomerModal,
        closeAddCustomerModal: closeAddCustomerModal,
        closeCustomerInfoModal: closeCustomerInfoModal,
        
        // Customer actions
        viewCustomer: viewCustomer,
        addService: addService,
        makePayment: makePayment,
        editCustomer: editCustomer,
        deleteCustomer: deleteCustomer,
        
        // Data access (if needed)
        getCustomers: () => [...customers], // Return copy
        getCustomerById: findCustomerById,
        getCustomerCount: () => customers.length,
        
        // Direct data manipulation (for API integration later)
        addCustomer: (customerData) => {
            const newCustomer = {
                id: generateNewId(),
                ...customerData,
                createdAt: new Date().toISOString()
            };
            customers.unshift(newCustomer);
            saveCustomers();
            return newCustomer;
        },
        
        updateCustomer: (customerId, updates) => {
            const customerIndex = customers.findIndex(c => c.id == customerId);
            if (customerIndex !== -1) {
                customers[customerIndex] = { ...customers[customerIndex], ...updates };
                saveCustomers();
                return customers[customerIndex];
            }
            return null;
        },
        
        removeCustomer: (customerId) => {
            const initialLength = customers.length;
            customers = customers.filter(c => c.id != customerId);
            saveCustomers();
            return customers.length < initialLength;
        }
    };
})();

// ===== AUTO INITIALIZATION =====
// Initialize module when loaded
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if not already initialized
    if (!CustomerModule._initialized) {
        CustomerModule.init();
        CustomerModule._initialized = true;
    }
});

// Also initialize immediately if DOM already loaded
if (document.readyState === 'loading') {
    // DOM hasn't finished loading yet
    console.log('🔄 CustomerModule: Waiting for DOM...');
} else {
    // DOM is already loaded
    if (!CustomerModule._initialized) {
        CustomerModule.init();
        CustomerModule._initialized = true;
    }
}

console.log('📦 CustomerModule loaded successfully');

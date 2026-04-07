/**
 * FIWARE Smart Store - UI Rendering Layer
 * Handles all DOM manipulation and UI updates
 */

const UI = {
  /**
   * Extract value from NGSI-LD format
   * @param {*} field - Field that might be NGSI-LD format or plain value
   * @returns {*} Extracted value
   */
  extractValue(field) {
    if (field === null || field === undefined) return '';
    if (typeof field === 'string' || typeof field === 'number' || typeof field === 'boolean') {
      return field;
    }
    if (field.value !== undefined) {
      return field.value;
    }
    return field;
  },

  /**
   * Show loading state
   * @param {string} elementId - Element to show loader
   */
  showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
      element.innerHTML = '<div class="loading-spinner">Cargando...</div>';
      element.classList.add(CONFIG.UI.LOADING_CLASS);
    }
  },

  /**
   * Show error message
   * @param {string} elementId - Element to show error
   * @param {string} message - Error message
   */
  showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
      element.innerHTML = `<div class="error-message">⚠️ ${message}</div>`;
      element.classList.add(CONFIG.UI.ERROR_CLASS);
    }
  },

  /**
   * Show success message
   * @param {string} message - Success message
   * @param {number} duration - Duration in ms (default 3000)
   */
  showSuccess(message, duration = 3000) {
    const notification = document.createElement('div');
    notification.className = 'success-notification';
    notification.innerHTML = `✅ ${message}`;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, duration);
  },

  /**
   * Update dashboard statistics
   * @param {object} stats - Statistics object with counts
   */
  updateStats(stats) {
    document.getElementById('store-count').textContent = stats.storeCount || 0;
    document.getElementById('product-count').textContent = stats.productCount || 0;
    document.getElementById('inventory-count').textContent = stats.inventoryCount || 0;
    document.getElementById('employee-count').textContent = stats.employeeCount || 0;
  },

  /**
   * Render products list
   * @param {array} products - Products array
   * @param {object} pagination - Pagination info
   */
  renderProducts(products, pagination = {}) {
    const container = document.getElementById('stores-list');
    if (!container) return;

    if (!products || products.length === 0) {
      container.innerHTML = '<p class="no-data">No hay productos disponibles</p>';
      return;
    }

    container.innerHTML = products.map(product => this.createProductCard(product)).join('');
  },

  /**
   * Create a single product card HTML
   * @param {object} product - Product object
   * @returns {string} HTML string
   */
  createProductCard(product) {
    const id = product.id || '';
    const name = this.extractValue(product.name) || 'Producto Sin Nombre';
    const price = this.extractValue(product.price) || 0;
    const description = this.extractValue(product.description) || '';
    const imageUrl = this.extractValue(product.image) || 'https://via.placeholder.com/200';

    return `
      <div class="product-card" data-product-id="${id}">
        <div class="product-image">
          <img src="${imageUrl}" alt="${name}" onerror="this.src='https://via.placeholder.com/200'">
        </div>
        <div class="product-info">
          <h3 class="product-name">${this.escapeHtml(name)}</h3>
          <p class="product-description">${this.escapeHtml(description)}</p>
          <div class="product-footer">
            <span class="price">€${parseFloat(price).toFixed(2)}</span>
            <button class="btn-details" data-product-id="${id}">Ver Detalles</button>
          </div>
        </div>
      </div>
    `;
  },

  /**
   * Render inventory table
   * @param {array} inventoryItems - Inventory items array
   */
  renderInventory(inventoryItems) {
    const tbody = document.querySelector('#inventory-table tbody');
    if (!tbody) return;

    if (!inventoryItems || inventoryItems.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" class="no-data">No hay items en el inventario</td></tr>';
      return;
    }

    tbody.innerHTML = inventoryItems.map(item => this.createInventoryRow(item)).join('');
  },

  /**
   * Create a single inventory table row HTML
   * @param {object} item - Inventory item
   * @returns {string} HTML string
   */
  createInventoryRow(item) {
    const id = item.id || '';
    const productName = this.extractValue(item.productName) || 'Desconocido';
    const storeName = this.extractValue(item.storeName) || 'Desconocida';
    const quantity = this.extractValue(item.quantity) || 0;
    const shelf = this.extractValue(item.shelf) || 'N/A';
    const isLowStock = parseInt(quantity) < CONFIG.UI.LOW_STOCK_THRESHOLD;
    const statusClass = isLowStock ? 'low-stock' : 'normal-stock';
    const statusText = isLowStock ? '⚠️ Stock Bajo' : '✅ Normal';

    return `
      <tr class="inventory-row" data-inventory-id="${id}">
        <td>${this.escapeHtml(productName)}</td>
        <td>${this.escapeHtml(storeName)}</td>
        <td class="quantity">${quantity}</td>
        <td>${shelf}</td>
        <td>
          <span class="status ${statusClass}">${statusText}</span>
        </td>
        <td>
          <button class="btn-buy" data-inventory-id="${id}" data-quantity="${quantity}" ${quantity === 0 ? 'disabled' : ''}>
            Comprar
          </button>
        </td>
      </tr>
    `;
  },

  /**
   * Render stores list
   * @param {array} stores - Stores array
   */
  renderStores(stores) {
    const container = document.querySelector('#stores-list');
    if (!container) return;

    // Update store filter
    const storeFilter = document.getElementById('filter-store');
    if (storeFilter && stores && stores.length > 0) {
      const options = stores.map(store => {
        const storeId = store.id || '';
        const storeName = this.extractValue(store.name) || 'Tienda Sin Nombre';
        return `<option value="${storeId}">${this.escapeHtml(storeName)}</option>`;
      }).join('');
      storeFilter.innerHTML = '<option value="">Todas las tiendas</option>' + options;
    }

    if (!stores || stores.length === 0) {
      if (container) container.innerHTML = '<p class="no-data">No hay tiendas disponibles</p>';
      return;
    }

    container.innerHTML = stores.map(store => this.createStoreCard(store)).join('');
  },

  /**
   * Create a single store card HTML
   * @param {object} store - Store object
   * @returns {string} HTML string
   */
  createStoreCard(store) {
    const id = store.id || '';
    const name = this.extractValue(store.name) || 'Tienda Sin Nombre';
    const address = this.extractValue(store.address) || '';
    const city = this.extractValue(store.city) || '';
    const country = this.extractValue(store.country) || '';
    const phone = this.extractValue(store.phone) || '';
    const email = this.extractValue(store.email) || '';

    return `
      <div class="store-card" data-store-id="${id}">
        <h3>${this.escapeHtml(name)}</h3>
        <p class="address">📍 ${this.escapeHtml(address)}</p>
        <p class="city">${this.escapeHtml(city)}, ${this.escapeHtml(country)}</p>
        <p class="contact">📞 ${phone}</p>
        <p class="email">✉️ ${email}</p>
      </div>
    `;
  },

  /**
   * Render employees list
   * @param {array} employees - Employees array
   */
  renderEmployees(employees) {
    const container = document.getElementById('employees-list');
    if (!container) return;

    if (!employees || employees.length === 0) {
      container.innerHTML = '<p class="no-data">No hay empleados disponibles</p>';
      return;
    }

    container.innerHTML = employees.map(employee => this.createEmployeeCard(employee)).join('');
  },

  /**
   * Create a single employee card HTML
   * @param {object} employee - Employee object
   * @returns {string} HTML string
   */
  createEmployeeCard(employee) {
    const id = employee.id || '';
    const name = this.extractValue(employee.name) || 'Empleado Sin Nombre';
    const email = this.extractValue(employee.email) || '';
    const role = this.extractValue(employee.role) || 'N/A';

    return `
      <div class="employee-card" data-employee-id="${id}">
        <h3>${this.escapeHtml(name)}</h3>
        <p class="role">📋 ${this.escapeHtml(role)}</p>
        <p class="email">✉️ ${email}</p>
      </div>
    `;
  },

  /**
   * Escape HTML special characters to prevent XSS
   * @param {string} text - Text to escape
   * @returns {string} Escaped text
   */
  escapeHtml(text) {
    const map = {
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#039;'
    };
    return String(text).replace(/[&<>"']/g, m => map[m]);
  },

  /**
   * Show buy dialog
   * @param {string} inventoryId - Inventory item ID
   * @param {number} maxQuantity - Maximum quantity available
   * @param {function} callback - Callback function when user buys
   */
  showBuyDialog(inventoryId, maxQuantity, callback) {
    const quantity = prompt(`¿Cuántas unidades desea comprar? (Máximo: ${maxQuantity})`, '1');
    
    if (quantity !== null) {
      const amount = parseInt(quantity);
      if (isNaN(amount) || amount <= 0 || amount > maxQuantity) {
        UI.showError('', `Por favor, ingrese una cantidad válida entre 1 y ${maxQuantity}`);
        return;
      }
      callback(amount);
    }
  }
};

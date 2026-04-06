/**
 * FIWARE Smart Store - Real-time Notifications
 * Socket.IO integration for real-time updates
 */

const Notifications = {
  socket: null,
  isConnected: false,

  /**
   * Initialize Socket.IO connection
   */
  init() {
    try {
      this.socket = io(CONFIG.SOCKET.URL, {
        reconnection: true,
        reconnectionDelay: CONFIG.SOCKET.RECONNECT_DELAY,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: 5
      });

      this.setupSocketListeners();
      console.log('Socket.IO initialized');
    } catch (error) {
      console.error('Socket.IO initialization error:', error);
    }
  },

  /**
   * Setup Socket.IO event listeners
   */
  setupSocketListeners() {
    if (!this.socket) return;

    // Connection events
    this.socket.on('connect', () => {
      this.isConnected = true;
      console.log('Connected to backend via Socket.IO');
      this.showNotification('Conectado al servidor', 'success');
    });

    this.socket.on('disconnect', () => {
      this.isConnected = false;
      console.log('Disconnected from backend');
      this.showNotification('Desconectado del servidor', 'info');
    });

    // Business events
    this.socket.on(CONFIG.SOCKET.EVENTS.PRICE_CHANGE, (data) => {
      this.handlePriceChange(data);
    });

    this.socket.on(CONFIG.SOCKET.EVENTS.LOW_STOCK, (data) => {
      this.handleLowStock(data);
    });

    this.socket.on(CONFIG.SOCKET.EVENTS.INVENTORY_UPDATE, (data) => {
      this.handleInventoryUpdate(data);
    });

    this.socket.on(CONFIG.SOCKET.EVENTS.NEW_SALE, (data) => {
      this.handleNewSale(data);
    });
  },

  /**
   * Handle price change event
   * @param {object} data - Event data
   */
  handlePriceChange(data) {
    console.log('Price change:', data);
    this.showNotification(
      `💰 Cambio de precio: ${data.productName} ahora €${data.newPrice}`,
      'info'
    );
    // Could refresh product list or update specific product
  },

  /**
   * Handle low stock event
   * @param {object} data - Event data
   */
  handleLowStock(data) {
    console.log('Low stock alert:', data);
    this.showNotification(
      `⚠️ Stock bajo: ${data.productName} en ${data.storeName} (${data.quantity} unidades)`,
      'warning'
    );
  },

  /**
   * Handle inventory update event
   * @param {object} data - Event data
   */
  handleInventoryUpdate(data) {
    console.log('Inventory update:', data);
    this.showNotification(
      `📦 Inventario actualizado: ${data.productName}`,
      'info'
    );
    // Could refresh inventory table if user is viewing it
    if (document.getElementById('inventory') && document.getElementById('inventory').style.display !== 'none') {
      App.loadInventory();
    }
  },

  /**
   * Handle new sale event
   * @param {object} data - Event data
   */
  handleNewSale(data) {
    console.log('New sale:', data);
    this.showNotification(
      `🛒 Nueva venta: ${data.quantity}x ${data.productName} en ${data.storeName}`,
      'success'
    );
  },

  /**
   * Show notification popup
   * @param {string} message - Notification message
   * @param {string} type - Notification type (info, success, warning, error)
   */
  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        ${message}
      </div>
      <button class="notification-close" onclick="this.parentElement.remove()">×</button>
    `;

    document.body.appendChild(notification);

    // Auto remove after 5 seconds
    setTimeout(() => {
      notification.remove();
    }, 5000);
  },

  /**
   * Emit event to backend
   * @param {string} eventName - Event name
   * @param {object} data - Event data
   */
  emit(eventName, data) {
    if (this.socket && this.isConnected) {
      this.socket.emit(eventName, data);
    }
  }
};

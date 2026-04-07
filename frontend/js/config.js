/**
 * FIWARE Smart Store - Frontend Configuration
 * Configuration centralized for easy management
 */

const CONFIG = {
  // Backend API Configuration
  API: {
    BASE_URL: '',  // Use relative URLs - Nginx will proxy to backend
    VERSION: 'v1',
    ENDPOINTS: {
      PRODUCTS: '/api/v1/products',
      STORES: '/api/v1/stores',
      INVENTORY: '/api/v1/inventory',
      EMPLOYEES: '/api/v1/employees'
    }
  },

  // Socket.IO Configuration
  SOCKET: {
    URL: window.location.origin,  // Use current host
    RECONNECT_DELAY: 3000,
    EVENTS: {
      PRICE_CHANGE: 'price_change',
      LOW_STOCK: 'low_stock',
      INVENTORY_UPDATE: 'inventory_update',
      NEW_SALE: 'new_sale'
    }
  },

  // UI Configuration
  UI: {
    ITEMS_PER_PAGE: 12,
    LOW_STOCK_THRESHOLD: 10,
    LOADING_CLASS: 'loading',
    ERROR_CLASS: 'error',
    SUCCESS_CLASS: 'success'
  },

  // Pagination
  PAGINATION: {
    DEFAULT_PAGE: 1,
    DEFAULT_LIMIT: 12
  }
};

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = CONFIG;
}

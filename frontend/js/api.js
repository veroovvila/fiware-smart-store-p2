/**
 * FIWARE Smart Store - API Layer
 * Handles all HTTP requests to the backend
 */

const API = {
  /**
   * Perform a fetch request with error handling
   * @param {string} url - The endpoint URL
   * @param {object} options - Fetch options
   * @returns {Promise<object>} Response data
   */
  async request(url, options = {}) {
    try {
      const defaultOptions = {
        headers: {
          'Content-Type': 'application/json'
        }
      };

      const response = await fetch(url, { ...defaultOptions, ...options });

      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('API Request Error:', error);
      throw error;
    }
  },

  /**
   * GET Products
   * @param {number} page - Page number
   * @param {number} limit - Items per page
   * @param {string} name - Filter by product name
   * @param {number} min_price - Filter by minimum price
   * @param {number} max_price - Filter by maximum price
   * @returns {Promise<object>} Products list with pagination
   */
  async getProducts(page = 1, limit = 12, name = '', min_price = null, max_price = null) {
    const params = new URLSearchParams();
    params.append('page', page);
    params.append('limit', limit);
    if (name) params.append('name', name);
    if (min_price !== null) params.append('min_price', min_price);
    if (max_price !== null) params.append('max_price', max_price);

    const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PRODUCTS}?${params.toString()}`;
    return this.request(url);
  },

  /**
   * GET single product
   * @param {string} productId - Product ID
   * @returns {Promise<object>} Product details
   */
  async getProduct(productId) {
    const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.PRODUCTS}/${productId}`;
    return this.request(url);
  },

  /**
   * GET Inventory items
   * @param {number} page - Page number
   * @param {number} limit - Items per page
   * @param {boolean} lowStock - Filter low stock items
   * @param {string} productId - Filter by product ID
   * @param {string} storeId - Filter by store ID
   * @returns {Promise<object>} Inventory list with pagination
   */
  async getInventory(page = 1, limit = 12, lowStock = false, productId = '', storeId = '') {
    const params = new URLSearchParams();
    params.append('page', page);
    params.append('limit', limit);
    if (lowStock) params.append('lowStock', 'true');
    if (productId) params.append('productId', productId);
    if (storeId) params.append('storeId', storeId);

    const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.INVENTORY}?${params.toString()}`;
    return this.request(url);
  },

  /**
   * GET single inventory item
   * @param {string} inventoryId - Inventory item ID
   * @returns {Promise<object>} Inventory item details
   */
  async getInventoryItem(inventoryId) {
    const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.INVENTORY}/${inventoryId}`;
    return this.request(url);
  },

  /**
   * BUY - Purchase inventory item (special endpoint)
   * @param {string} inventoryId - Inventory item ID
   * @param {number} quantity - Quantity to buy
   * @returns {Promise<object>} Transaction result
   */
  async buyInventoryItem(inventoryId, quantity) {
    const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.INVENTORY}/${inventoryId}/buy`;
    return this.request(url, {
      method: 'PATCH',
      body: JSON.stringify({ quantity })
    });
  },

  /**
   * GET Stores
   * @param {number} page - Page number
   * @param {number} limit - Items per page
   * @returns {Promise<object>} Stores list with pagination
   */
  async getStores(page = 1, limit = 12) {
    const params = new URLSearchParams();
    params.append('page', page);
    params.append('limit', limit);

    const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.STORES}?${params.toString()}`;
    return this.request(url);
  },

  /**
   * GET Employees
   * @param {number} page - Page number
   * @param {number} limit - Items per page
   * @returns {Promise<object>} Employees list with pagination
   */
  async getEmployees(page = 1, limit = 12) {
    const params = new URLSearchParams();
    params.append('page', page);
    params.append('limit', limit);

    const url = `${CONFIG.API.BASE_URL}${CONFIG.API.ENDPOINTS.EMPLOYEES}?${params.toString()}`;
    return this.request(url);
  }
};

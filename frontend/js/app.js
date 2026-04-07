/**
 * FIWARE Smart Store - Main Application
 * Orchestrates all modules and handles application flow
 */

const App = {
  // Current state
  currentPage: 1,
  products: [],
  inventory: [],
  stores: [],
  employees: [],

  /**
   * Initialize the application
   */
  async init() {
    console.log('Initializing FIWARE Smart Store Frontend...');

    try {
      // Initialize modules
      Events.init();
      Notifications.init();

      // Show initial section (dashboard)
      this.navigateToDashboard();

      console.log('Application initialized successfully');
    } catch (error) {
      console.error('Application initialization error:', error);
      UI.showError('app', 'Error al inicializar la aplicación');
    }
  },

  /**
   * Navigate to dashboard and load data
   */
  navigateToDashboard() {
    Events.navigateToSection('dashboard');
  },

  /**
   * Load dashboard data
   */
  async loadDashboard() {
    try {
      UI.showLoading('');
      
      // Fetch counts for statistics with timeout
      const timeout = 5000; // 5 seconds
      
      const results = await Promise.allSettled([
        this.withTimeout(API.getProducts(1, 1), timeout),
        this.withTimeout(API.getStores(1, 1), timeout),
        this.withTimeout(API.getInventory(1, 1), timeout),
        this.withTimeout(API.getEmployees(1, 1), timeout)
      ]);

      const stats = {
        productCount: results[0].status === 'fulfilled' ? results[0].value?.data?.total || 0 : 0,
        storeCount: results[1].status === 'fulfilled' ? results[1].value?.data?.total || 0 : 0,
        inventoryCount: results[2].status === 'fulfilled' ? results[2].value?.data?.total || 0 : 0,
        employeeCount: results[3].status === 'fulfilled' ? results[3].value?.data?.total || 0 : 0
      };

      UI.updateStats(stats);
    } catch (error) {
      console.error('Dashboard load error:', error);
      UI.showError('dashboard', 'Error al cargar el dashboard');
    }
  },

  /**
   * Execute promise with timeout
   */
  withTimeout(promise, ms) {
    return Promise.race([
      promise,
      new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout')), ms)
      )
    ]);
  },

  /**
   * Load and display products
   */
  async loadProducts() {
    try {
      UI.showLoading('stores-list');

      // Get filter values
      const searchInput = document.getElementById('search-products');
      const priceMinInput = document.getElementById('price-min');
      const priceMaxInput = document.getElementById('price-max');

      const name = searchInput ? searchInput.value : '';
      const minPrice = priceMinInput ? priceMinInput.value : null;
      const maxPrice = priceMaxInput ? priceMaxInput.value : null;

      // Fetch products
      const response = await API.getProducts(
        this.currentPage,
        CONFIG.UI.ITEMS_PER_PAGE,
        name,
        minPrice,
        maxPrice
      );

      if (response.success && response.data) {
        this.products = response.data.items || [];
        UI.renderProducts(this.products, response.data);
      } else {
        UI.showError('stores-list', 'No se pudieron cargar los productos');
      }
    } catch (error) {
      console.error('Products load error:', error);
      UI.showError('stores-list', 'Error al cargar productos: ' + error.message);
    }
  },

  /**
   * Load and display inventory
   */
  async loadInventory() {
    try {
      UI.showLoading('inventory-table');

      // Get filter values
      const searchInput = document.getElementById('search-inventory');
      const storeFilter = document.getElementById('filter-store');

      const productName = searchInput ? searchInput.value : '';
      const storeId = storeFilter ? storeFilter.value : '';

      // Fetch inventory
      const response = await API.getInventory(
        this.currentPage,
        CONFIG.UI.ITEMS_PER_PAGE,
        false,
        productName,
        storeId
      );

      if (response.success && response.data) {
        this.inventory = response.data.items || [];
        UI.renderInventory(this.inventory);
      } else {
        UI.showError('inventory-table', 'No se pudo cargar el inventario');
      }
    } catch (error) {
      console.error('Inventory load error:', error);
      const tbody = document.querySelector('#inventory-table tbody');
      if (tbody) {
        tbody.innerHTML = `<tr><td colspan="6" class="error">Error: ${error.message}</td></tr>`;
      }
    }
  },

  /**
   * Load and display stores
   */
  async loadStores() {
    try {
      UI.showLoading('stores-list');

      const response = await API.getStores(this.currentPage, CONFIG.UI.ITEMS_PER_PAGE);

      if (response.success && response.data) {
        this.stores = response.data.items || [];
        UI.renderStores(this.stores);
      } else {
        UI.showError('stores-list', 'No se pudieron cargar las tiendas');
      }
    } catch (error) {
      console.error('Stores load error:', error);
      UI.showError('stores-list', 'Error al cargar tiendas: ' + error.message);
    }
  },

  /**
   * Load and display employees
   */
  async loadEmployees() {
    try {
      UI.showLoading('employees-list');

      const response = await API.getEmployees(this.currentPage, CONFIG.UI.ITEMS_PER_PAGE);

      if (response.success && response.data) {
        this.employees = response.data.items || [];
        UI.renderEmployees(this.employees);
      } else {
        UI.showError('employees-list', 'No se pudieron cargar los empleados');
      }
    } catch (error) {
      console.error('Employees load error:', error);
      UI.showError('employees-list', 'Error al cargar empleados: ' + error.message);
    }
  },

  /**
   * Buy inventory item (call /buy endpoint)
   * @param {string} inventoryId - Inventory item ID
   * @param {number} quantity - Quantity to buy
   */
  async buyInventoryItem(inventoryId, quantity) {
    try {
      const response = await API.buyInventoryItem(inventoryId, quantity);

      if (response.success) {
        UI.showSuccess(`✅ Compra realizada: ${quantity} unidades`);
        // Refresh inventory
        this.loadInventory();
      } else {
        UI.showError('', response.message || 'Error en la compra');
      }
    } catch (error) {
      console.error('Buy error:', error);
      UI.showError('', 'Error al realizar la compra: ' + error.message);
    }
  }
};

/**
 * Initialize application when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});

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
    console.log('=== INITIALIZING FIWARE SMART STORE ===');

    try {
      // Initialize modules
      console.log('[App] Initializing Theme...');
      if (!Theme) {
        console.error('[App] Theme module not loaded!');
        return;
      }
      Theme.init();

      console.log('[App] Initializing I18N...');
      if (!I18N) {
        console.error('[App] I18N module not loaded!');
        return;
      }
      I18N.init();

      console.log('[App] Initializing Events...');
      Events.init();
      
      console.log('[App] Initializing Notifications...');
      Notifications.init();

      // Setup controls
      console.log('[App] Setting up controls...');
      this.setupControls();

      // Show initial section (dashboard)
      this.navigateToDashboard();

      console.log('=== APPLICATION READY ===');
    } catch (error) {
      console.error('=== INITIALIZATION ERROR ===', error);
      console.error('Stack:', error.stack);
    }
  },

  /**
   * Setup theme toggle and language selector
   */
  setupControls() {
    // Theme toggle button
    const themeBtn = document.getElementById('theme-toggle');
    console.log('[App] Theme button:', themeBtn ? 'FOUND' : 'NOT FOUND');
    
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        console.log('[App] Theme button clicked');
        Theme.toggle();
        this.updateThemeButton();
      });
      this.updateThemeButton();
    }

    // Language selector
    const langSelect = document.getElementById('language-select');
    console.log('[App] Language selector:', langSelect ? 'FOUND' : 'NOT FOUND');
    
    if (langSelect) {
      langSelect.value = I18N.getCurrentLanguage();
      langSelect.addEventListener('change', (e) => {
        console.log('[App] Language changed to:', e.target.value);
        I18N.setLanguage(e.target.value);
      });
    }
  },

  /**
   * Update theme button display
   */
  updateThemeButton() {
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
      const theme = Theme.getCurrentTheme();
      themeBtn.textContent = theme === 'dark' ? '☀️' : '🌙';
      console.log('[App] Theme button updated to:', themeBtn.textContent);
    }
  },

  /**
   * Reload current section (useful when language changes)
   */
  async reloadCurrentSection() {
    const activeSection = document.querySelector('.section[style="display: block"]');
    if (activeSection) {
      const sectionId = activeSection.id;
      
      if (sectionId === 'dashboard') {
        await this.loadDashboard();
      } else if (sectionId === 'inventory') {
        await this.loadInventory();
      } else if (sectionId === 'stores') {
        await this.loadStores();
      } else if (sectionId === 'employees') {
        await this.loadEmployees();
      }
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
      UI.showLoading('products-list');
      
      // Fetch counts for statistics
      const productsRes = await API.getProducts(1, 1);
      const storesRes = await API.getStores(1, 1);
      const inventoryRes = await API.getInventory(1, 1);
      const employeesRes = await API.getEmployees(1, 1);

      const stats = {
        productCount: productsRes.data?.total || 0,
        storeCount: storesRes.data?.total || 0,
        inventoryCount: inventoryRes.data?.total || 0,
        employeeCount: employeesRes.data?.total || 0
      };

      UI.updateStats(stats);
      
      // Also load and display products in the dashboard
      await this.loadProducts();
    } catch (error) {
      console.error('Dashboard load error:', error);
      UI.showError('products-list', 'Error al cargar el dashboard');
    }
  },

  /**
   * Load and display products
   */
  async loadProducts() {
    try {
      UI.showLoading('products-list');

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
        this.products = response.data.products || [];
        UI.renderProducts(this.products, response.data);
      } else {
        UI.showError('stores-list', 'No se pudieron cargar los productos');
      }
    } catch (error) {
      console.error('Products load error:', error);
      UI.showError('products-list', 'Error al cargar productos: ' + error.message);
    }
  },

  /**
   * Load and display inventory
   */
  async loadInventory() {
    try {
      UI.showLoading('inventory-table');

      // Get filter values
      const storeFilter = document.getElementById('filter-store');
      const storeId = storeFilter ? storeFilter.value : '';

      // Fetch inventory
      const response = await API.getInventory(
        this.currentPage,
        CONFIG.UI.ITEMS_PER_PAGE,
        false,
        '',  // productId (empty string)
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
        this.stores = response.data.stores || [];
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
        this.employees = response.data.employees || [];
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

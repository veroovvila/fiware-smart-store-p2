/**
 * FIWARE Smart Store - Internationalization (i18n)
 * Handles multiple language support for the application
 */

const I18N = {
  // Current language
  currentLanguage: 'es',

  // Supported languages
  languages: {
    es: 'Español',
    en: 'English'
  },

  // Translation dictionary
  translations: {
    es: {
      // Navigation
      dashboard: 'Dashboard',
      stores: 'Tiendas',
      inventory: 'Inventario',
      employees: 'Empleados',

      // Products Section
      availableProducts: 'Productos Disponibles',
      searchByName: 'Buscar por nombre...',
      minPrice: 'Precio mínimo:',
      maxPrice: 'Precio máximo:',
      seeDetails: 'Ver Detalles',
      noProductsAvailable: 'No hay productos disponibles',

      // Dashboard Stats
      dashboardTitle: 'Dashboard',
      activeStores: 'Tiendas Activas',
      products: 'Productos',
      totalInventory: 'Inventario Total',
      employees: 'Empleados',

      // Map Section
      storeLocations: 'Ubicación de Tiendas',

      // Stores Section
      storeManagement: 'Gestión de Tiendas',
      noStoresAvailable: 'No hay tiendas disponibles',

      // Inventory Section
      inventoryTitle: 'Inventario',
      searchProduct: 'Buscar producto...',
      allStores: 'Todas las tiendas',
      searchInventory: 'Buscar...',
      productName: 'Nombre del Producto',
      storeName: 'Tienda',
      quantity: 'Cantidad',
      shelf: 'Estante',
      status: 'Estado',
      lowStock: '⚠️ Stock Bajo',
      normalStock: '✅ Normal',
      buy: 'Comprar',
      noInventoryItems: 'No hay items en el inventario',

      // Employees Section
      employeeManagement: 'Gestión de Empleados',
      noEmployeesAvailable: 'No hay empleados disponibles',

      // Buttons and Common
      loading: 'Cargando...',
      error: 'Error',
      success: 'Éxito',
      noData: 'No hay datos disponibles',

      // Theme and Language
      language: 'Idioma',
      theme: 'Tema',
      darkMode: 'Modo Oscuro',
      lightMode: 'Modo Claro'
    },
    en: {
      // Navigation
      dashboard: 'Dashboard',
      stores: 'Stores',
      inventory: 'Inventory',
      employees: 'Employees',

      // Products Section
      availableProducts: 'Available Products',
      searchByName: 'Search by name...',
      minPrice: 'Minimum price:',
      maxPrice: 'Maximum price:',
      seeDetails: 'View Details',
      noProductsAvailable: 'No products available',

      // Dashboard Stats
      dashboardTitle: 'Dashboard',
      activeStores: 'Active Stores',
      products: 'Products',
      totalInventory: 'Total Inventory',
      employees: 'Employees',

      // Map Section
      storeLocations: 'Store Locations',

      // Stores Section
      storeManagement: 'Store Management',
      noStoresAvailable: 'No stores available',

      // Inventory Section
      inventoryTitle: 'Inventory',
      searchProduct: 'Search product...',
      allStores: 'All stores',
      searchInventory: 'Search...',
      productName: 'Product Name',
      storeName: 'Store',
      quantity: 'Quantity',
      shelf: 'Shelf',
      status: 'Status',
      lowStock: '⚠️ Low Stock',
      normalStock: '✅ Normal',
      buy: 'Buy',
      noInventoryItems: 'No inventory items',

      // Employees Section
      employeeManagement: 'Employee Management',
      noEmployeesAvailable: 'No employees available',

      // Buttons and Common
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      noData: 'No data available',

      // Theme and Language
      language: 'Language',
      theme: 'Theme',
      darkMode: 'Dark Mode',
      lightMode: 'Light Mode'
    }
  },

  /**
   * Initialize i18n system
   */
  init() {
    console.log('[I18N] Initializing internationalization system...');
    
    // Load saved language from localStorage or use default
    const savedLanguage = localStorage.getItem('language');
    if (savedLanguage && this.languages[savedLanguage]) {
      this.currentLanguage = savedLanguage;
      console.log('[I18N] Loaded saved language:', savedLanguage);
    } else {
      console.log('[I18N] Using default language: es');
    }

    // Update HTML lang attribute
    document.documentElement.lang = this.currentLanguage;

    // Translate page on load
    console.log('[I18N] Starting translation...');
    this.translate();
    console.log('[I18N] Translation complete');
  },

  /**
   * Get translation for a key
   * @param {string} key - Translation key
   * @returns {string} Translated text or key if not found
   */
  t(key) {
    const translated = this.translations[this.currentLanguage][key];
    if (!translated) {
      console.warn(`Translation key not found: ${key}`);
      return key;
    }
    return translated;
  },

  /**
   * Change current language
   * @param {string} lang - Language code (es, en)
   */
  setLanguage(lang) {
    if (!this.languages[lang]) {
      console.error(`Language not supported: ${lang}`);
      return;
    }

    this.currentLanguage = lang;
    localStorage.setItem('language', lang);
    document.documentElement.lang = lang;

    // Re-translate all elements
    this.translate();

    // Dispatch event for apps that need to know language changed
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: { language: lang } }));
  },

  /**
   * Translate all elements with data-i18n attributes
   */
  translate() {
    // Translate elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(element => {
      const key = element.dataset.i18n;
      if (key) {
        if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
          if (element.placeholder) {
            element.placeholder = this.t(key);
          }
          if (element.value && !element.value.trim()) {
            element.value = this.t(key);
          }
        } else if (element.tagName === 'OPTION') {
          element.textContent = this.t(key);
        } else {
          element.textContent = this.t(key);
        }
      }
    });

    // Translate elements with data-i18n-title attribute
    document.querySelectorAll('[data-i18n-title]').forEach(element => {
      const key = element.dataset.i18nTitle;
      if (key) {
        element.title = this.t(key);
      }
    });
  },

  /**
   * Get current language
   * @returns {string} Current language code
   */
  getCurrentLanguage() {
    return this.currentLanguage;
  },

  /**
   * Get all available languages
   * @returns {object} Languages object
   */
  getAvailableLanguages() {
    return this.languages;
  }
};

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = I18N;
}

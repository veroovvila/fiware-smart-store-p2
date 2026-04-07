// Internationalization Module
const I18N = {
  currentLanguage: localStorage.getItem('language') || 'es',
  
  translations: {
    es: {
      dashboard: 'Dashboard',
      stores: 'Tiendas',
      inventory: 'Inventario',
      employees: 'Empleados',
      availableProducts: 'Productos Disponibles',
      searchByName: 'Buscar por nombre...',
      minPrice: 'Precio mínimo:',
      maxPrice: 'Precio máximo:',
      seeDetails: 'Ver Detalles',
      noProductsAvailable: 'No hay productos disponibles',
      dashboardTitle: 'Dashboard',
      activeStores: 'Tiendas Activas',
      products: 'Productos',
      totalInventory: 'Inventario Total',
      storeLocations: 'Ubicación de Tiendas',
      storeManagement: 'Gestión de Tiendas',
      noStoresAvailable: 'No hay tiendas disponibles',
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
      employeeManagement: 'Gestión de Empleados',
      noEmployeesAvailable: 'No hay empleados disponibles',
      loading: 'Cargando...',
      error: 'Error',
      success: 'Éxito',
      noData: 'No hay datos disponibles',
      language: 'Idioma',
      theme: 'Tema',
      darkMode: 'Modo Oscuro',
      lightMode: 'Modo Claro'
    },
    en: {
      dashboard: 'Dashboard',
      stores: 'Stores',
      inventory: 'Inventory',
      employees: 'Employees',
      availableProducts: 'Available Products',
      searchByName: 'Search by name...',
      minPrice: 'Minimum price:',
      maxPrice: 'Maximum price:',
      seeDetails: 'View Details',
      noProductsAvailable: 'No products available',
      dashboardTitle: 'Dashboard',
      activeStores: 'Active Stores',
      products: 'Products',
      totalInventory: 'Total Inventory',
      storeLocations: 'Store Locations',
      storeManagement: 'Store Management',
      noStoresAvailable: 'No stores available',
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
      employeeManagement: 'Employee Management',
      noEmployeesAvailable: 'No employees available',
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      noData: 'No data available',
      language: 'Language',
      theme: 'Theme',
      darkMode: 'Dark Mode',
      lightMode: 'Light Mode'
    }
  },

  init() {
    console.log('[I18N] Init - Current language:', this.currentLanguage);
    document.documentElement.lang = this.currentLanguage;
    this.translate();
  },

  t(key) {
    return this.translations[this.currentLanguage][key] || key;
  },

  setLanguage(lang) {
    console.log('[I18N] Setting language to:', lang);
    if (!this.translations[lang]) {
      console.error('[I18N] Language not found:', lang);
      return;
    }
    this.currentLanguage = lang;
    localStorage.setItem('language', lang);
    document.documentElement.lang = lang;
    this.translate();
    console.log('[I18N] Language changed to:', lang);
  },

  getCurrentLanguage() {
    return this.currentLanguage;
  },

  translate() {
    console.log('[I18N] Translating page...');
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (key) {
        const text = this.t(key);
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          if (el.type === 'text' || el.type === 'number' || el.type === 'search') {
            el.placeholder = text;
          }
        } else if (el.tagName === 'OPTION') {
          el.textContent = text;
        } else {
          el.textContent = text;
        }
      }
    });
  }
};
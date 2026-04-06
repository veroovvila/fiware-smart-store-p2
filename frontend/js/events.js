/**
 * FIWARE Smart Store - Event Handlers
 * Manages all user interactions and DOM events
 */

const Events = {
  /**
   * Initialize all event listeners
   */
  init() {
    this.setupNavigation();
    this.setupProductFilters();
    this.setupInventoryFilters();
    this.setupProductListeners();
    this.setupInventoryListeners();
  },

  /**
   * Setup navigation click handlers
   */
  setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const sectionId = link.getAttribute('href').substring(1);
        this.navigateToSection(sectionId);
      });
    });
  },

  /**
   * Navigate to a specific section
   * @param {string} sectionId - Section ID to navigate to
   */
  navigateToSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
      section.style.display = 'none';
    });

    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
      targetSection.style.display = 'block';
      
      // Load data based on section
      if (sectionId === 'dashboard') {
        App.loadDashboard();
      } else if (sectionId === 'stores') {
        App.loadStores();
      } else if (sectionId === 'inventory') {
        App.loadInventory();
      } else if (sectionId === 'employees') {
        App.loadEmployees();
      }
    }
  },

  /**
   * Setup product filter handlers
   */
  setupProductFilters() {
    const searchInput = document.getElementById('search-products');
    const priceMinInput = document.getElementById('price-min');
    const priceMaxInput = document.getElementById('price-max');

    if (searchInput) {
      searchInput.addEventListener('input', () => {
        App.currentPage = 1;
        App.loadProducts();
      });
    }

    if (priceMinInput) {
      priceMinInput.addEventListener('change', () => {
        App.currentPage = 1;
        App.loadProducts();
      });
    }

    if (priceMaxInput) {
      priceMaxInput.addEventListener('change', () => {
        App.currentPage = 1;
        App.loadProducts();
      });
    }
  },

  /**
   * Setup inventory filter handlers
   */
  setupInventoryFilters() {
    const searchInput = document.getElementById('search-inventory');
    const storeFilter = document.getElementById('filter-store');

    if (searchInput) {
      searchInput.addEventListener('input', () => {
        App.currentPage = 1;
        App.loadInventory();
      });
    }

    if (storeFilter) {
      storeFilter.addEventListener('change', () => {
        App.currentPage = 1;
        App.loadInventory();
      });
    }
  },

  /**
   * Setup product card listeners
   */
  setupProductListeners() {
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('btn-details')) {
        const productId = e.target.dataset.productId;
        console.log('View product details:', productId);
        // Could show modal with details
      }
    });
  },

  /**
   * Setup inventory buy button listeners
   */
  setupInventoryListeners() {
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('btn-buy')) {
        const inventoryId = e.target.dataset.inventoryId;
        const maxQuantity = parseInt(e.target.dataset.quantity);
        
        UI.showBuyDialog(inventoryId, maxQuantity, async (quantity) => {
          await App.buyInventoryItem(inventoryId, quantity);
        });
      }
    });
  }
};

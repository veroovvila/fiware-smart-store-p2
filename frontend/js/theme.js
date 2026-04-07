/**
 * FIWARE Smart Store - Theme Management
 * Handles Dark and Light mode switching
 */

const Theme = {
  // Current theme
  currentTheme: 'light',

  // Supported themes
  themes: {
    light: { name: 'Light Mode', icon: '☀️' },
    dark: { name: 'Dark Mode', icon: '🌙' }
  },

  /**
   * Initialize theme system
   */
  init() {
    console.log('[THEME] Initializing theme system...');
    
    // Load saved theme from localStorage or use system preference
    const savedTheme = localStorage.getItem('theme');
    
    if (savedTheme && this.themes[savedTheme]) {
      this.currentTheme = savedTheme;
      console.log('[THEME] Loaded saved theme:', savedTheme);
    } else {
      // Check system preference
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        this.currentTheme = 'dark';
        console.log('[THEME] Using system preference: dark');
      } else {
        this.currentTheme = 'light';
        console.log('[THEME] Using default: light');
      }
    }

    // Apply theme
    this.applyTheme();

    // Listen for system theme changes
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
          this.currentTheme = e.matches ? 'dark' : 'light';
          this.applyTheme();
        }
      });
    }
  },

  /**
   * Apply current theme to document
   */
  applyTheme() {
    const html = document.documentElement;
    
    console.log('[THEME] Applying theme:', this.currentTheme);
    
    // Remove old theme classes
    html.classList.remove('theme-light', 'theme-dark');
    
    // Add new theme class
    html.classList.add(`theme-${this.currentTheme}`);
    
    // Set data attribute for CSS
    html.setAttribute('data-theme', this.currentTheme);
    
    console.log('[THEME] Classes applied:', html.className);
  },

  /**
   * Toggle between light and dark theme
   */
  toggle() {
    this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    console.log('[THEME] Toggling theme to:', this.currentTheme);
    localStorage.setItem('theme', this.currentTheme);
    this.applyTheme();

    // Dispatch event for apps that need to know theme changed
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: this.currentTheme } }));
  },

  /**
   * Set specific theme
   * @param {string} theme - Theme name (light or dark)
   */
  setTheme(theme) {
    if (!this.themes[theme]) {
      console.error(`Theme not supported: ${theme}`);
      return;
    }

    this.currentTheme = theme;
    localStorage.setItem('theme', theme);
    this.applyTheme();

    // Dispatch event
    window.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: theme } }));
  },

  /**
   * Get current theme
   * @returns {string} Current theme name
   */
  getCurrentTheme() {
    return this.currentTheme;
  },

  /**
   * Get theme info
   * @returns {object} Theme info
   */
  getThemeInfo() {
    return this.themes[this.currentTheme];
  }
};

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Theme;
}

// Theme Module
const Theme = {
  currentTheme: localStorage.getItem('theme') || 'light',

  init() {
    console.log('[THEME] Init - Current theme:', this.currentTheme);
    this.apply();
  },

  apply() {
    console.log('[THEME] Applying theme:', this.currentTheme);
    const html = document.documentElement;
    html.classList.remove('theme-light', 'theme-dark');
    html.classList.add('theme-' + this.currentTheme);
    html.setAttribute('data-theme', this.currentTheme);
    console.log('[THEME] Theme class applied -', 'theme-' + this.currentTheme);
  },

  toggle() {
    console.log('[THEME] Toggle clicked');
    this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', this.currentTheme);
    this.apply();
    console.log('[THEME] Theme toggled to:', this.currentTheme);
  },

  getCurrentTheme() {
    return this.currentTheme;
  },

  setTheme(theme) {
    if (theme !== 'light' && theme !== 'dark') {
      console.error('[THEME] Invalid theme:', theme);
      return;
    }
    this.currentTheme = theme;
    localStorage.setItem('theme', theme);
    this.apply();
  }
};
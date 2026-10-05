// SatQuery AI Mission Control Configuration
// Allows dynamic backend URL configuration without inline hardcoding

window.SATQUERY_CONFIG = {
  BACKEND_API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000/query'
    : 'http://localhost:8000/query'
};

const getApiBaseUrl = () => {
  // Override with environment variable if provided
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // Check if we're in development mode
  if (import.meta.env.DEV) {
    return 'http://localhost:5000/api';
  }
  
  // For production, try to detect the current host
  const currentHost = window.location.hostname;
  
  // If accessing via localhost/127.0.0.1, assume development
  if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
    return 'http://localhost:5000/api';
  }
  
  // For production, use the same host as the frontend with port 5000
  return `http://${currentHost}:5000/api`;
};

const API_BASE_URL = getApiBaseUrl();

class ApiService {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    if (this.token) {
      config.headers.Authorization = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async register(userData) {
    const response = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });

    if (response.access_token) {
      this.setToken(response.access_token);
    }

    return response;
  }

  async login(credentials) {
    const response = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });

    if (response.access_token) {
      this.setToken(response.access_token);
    }

    return response;
  }

  async getCurrentUser() {
    return await this.request('/auth/me');
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  isAuthenticated() {
    return !!this.token;
  }
}

export default new ApiService();
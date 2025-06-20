const getApiBaseUrl = () => {
  // Override with environment variable if provided
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL;
  }
  
  // Check if we're in development mode
  if (import.meta.env.DEV) {
    return 'http://localhost:5001/api';
  }
  
  // For production, try to detect the current host
  const currentHost = window.location.hostname;
  
  // If accessing via localhost/127.0.0.1, assume development
  if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
    return 'http://localhost:5001/api';
  }
  
  // For production, use the same host as the frontend with port 5001
  return `http://${currentHost}:5001/api`;
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

  // Module Management
  async getUserModules() {
    return await this.request('/user/modules');
  }

  async toggleUserModule(moduleId) {
    return await this.request(`/user/modules/${moduleId}/toggle`, {
      method: 'PUT'
    });
  }

  async getUserPreferences() {
    return await this.request('/user/preferences');
  }

  async updateUserPreferences(preferences) {
    return await this.request('/user/preferences', {
      method: 'PUT',
      body: JSON.stringify(preferences)
    });
  }

  // Boats API
  async getBoats() {
    return await this.request('/boats');
  }

  async getBoat(id) {
    return await this.request(`/boats/${id}`);
  }

  async createBoat(boatData) {
    return await this.request('/boats', {
      method: 'POST',
      body: JSON.stringify(boatData)
    });
  }

  async updateBoat(id, boatData) {
    return await this.request(`/boats/${id}`, {
      method: 'PUT',
      body: JSON.stringify(boatData)
    });
  }

  async deleteBoat(id) {
    return await this.request(`/boats/${id}`, {
      method: 'DELETE'
    });
  }

  // Trips API
  async getTrips() {
    return await this.request('/trips');
  }

  async getTrip(id) {
    return await this.request(`/trips/${id}`);
  }

  async createTrip(tripData) {
    return await this.request('/trips', {
      method: 'POST',
      body: JSON.stringify(tripData)
    });
  }

  async updateTrip(id, tripData) {
    return await this.request(`/trips/${id}`, {
      method: 'PUT',
      body: JSON.stringify(tripData)
    });
  }

  async deleteTrip(id) {
    return await this.request(`/trips/${id}`, {
      method: 'DELETE'
    });
  }
}

export default new ApiService();
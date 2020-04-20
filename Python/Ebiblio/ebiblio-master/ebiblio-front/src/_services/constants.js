const API_URL = process.env.REACT_APP_API_URL || 'http://0.0.0.0:8000';

export const defaultHeaders = Object.freeze({
  baseURL: API_URL.endsWith('/') ? API_URL : `${API_URL}/`,
  timeout: 60000,
});

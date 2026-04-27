import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://194.87.76.29:8000',
  withCredentials: true, // отправляем httpOnly refresh-cookie автоматически
});

export default api;

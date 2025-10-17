// API Configuration
const config = {
  apiUrl: process.env.REACT_APP_API_URL || 
    (process.env.NODE_ENV === 'production' 
      ? 'https://chinese-study-production.up.railway.app'
      : 'http://localhost:5000')
};

export default config;


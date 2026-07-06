import axios from 'axios';

// Create an Axios instance pointing to the FastAPI backend
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Send a chat message to the Agent Router.
 * 
 * @param {string} message - The user's input text
 * @returns {Promise<Object>} The structured response from the backend
 */
export const sendChatMessage = async (message) => {
  const response = await api.post('/api/chat', { message });
  return response.data;
};

/**
 * Fetch all saved vocabulary from the backend.
 * 
 * @returns {Promise<Object>} The vocabulary response
 */
export const getVocabulary = async () => {
  const response = await api.get('/api/vocabulary');
  return response.data;
};

export default api;

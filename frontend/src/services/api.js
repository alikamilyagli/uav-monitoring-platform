const API_BASE_URL = 'http://localhost:5001/api';
const BASIC_AUTH_USERNAME = 'admin';
const BASIC_AUTH_PASSWORD = 'admin';

const getAuthHeaders = () => {
  const encodedCredentials = btoa(`${BASIC_AUTH_USERNAME}:${BASIC_AUTH_PASSWORD}`);
  return {
    'Content-Type': 'application/json',
    'Authorization': `Basic ${encodedCredentials}`,
  };
};

const handleResponse = async (response) => {
  if (!response.ok) {
    const errorData = await response.json();
    const error = new Error('Error in API request');
    error.data = errorData;
    throw error;
  }
  return response.json();
};

export default {
  async getDrones(page = 1, perPage = 10) {
    try {
      const response = await fetch(`${API_BASE_URL}/drones?page=${page}&per_page=${perPage}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('Error fetching drones:', error);
      throw error;
    }
  },

  async getTasks() {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('Error fetching tasks:', error);
      throw error;
    }
  },

  async updateTask(task) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${task.id}`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(task),
      });
      return handleResponse(response);
    } catch (error) {
      console.error(`Error updating task ${task.id}:`, error);
      throw error;
    }
  },

  async createTask(taskData) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });
      return handleResponse(response);
    } catch (error) {
      console.error('Error creating task:', error);
      throw error;
    }
  },

  async getTaskById(taskId) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      return handleResponse(response);
    } catch (error) {
      console.error(`Error fetching task ${taskId}:`, error);
      throw error;
    }
  },

  async executeTask(taskId) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/execute`, {
        method: 'POST',
        headers: getAuthHeaders(),
      });
      return handleResponse(response);
    } catch (error) {
      console.error(`Error executing task ${taskId}:`, error);
      throw error;
    }
  },

  async getTaskImages(taskId) {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/images`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });
      return handleResponse(response);
    } catch (error) {
      console.error(`Error fetching images for task ${taskId}:`, error);
      throw error;
    }
  },
};

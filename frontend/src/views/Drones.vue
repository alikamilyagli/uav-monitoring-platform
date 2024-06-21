<template>
  <div :class="{'dark': isDarkMode}" class="bg-gray-200 dark:bg-gray-800 flex items-center justify-center py-6 px-4 sm:px-3 lg:px-4">
    <!-- Boxed card container -->
    <div :class="{'dark': isDarkMode}" class="bg-white dark:bg-gray-700 w-full max-w-4xl shadow-md rounded-lg p-4">
      <!-- Header section with select box and create task button -->
      <div class="px-2 py-4">
        <div class="flex justify-between items-center mb-4">
          <!-- Select box for choosing items per page -->
          <div class="flex items-center">
            <label :for="perPage" :class="{'dark:text-white': isDarkMode}" class="mr-2">Items per page:</label>
            <select v-model="perPage" @change="fetchDrones" class="rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
              <option v-for="option in perPageOptions" :key="option" :value="option">{{ option }}</option>
            </select>
          </div>

          <!-- Create task button -->
          <button @click="openCreateTaskModal" :disabled="selectedDrones.length === 0" class="bg-blue-500 dark:bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
            Create Task for Selected Drones
          </button>
        </div>
      </div>

      <!-- Drone list section -->
      <div class="px-6 py-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          <drone-card
            v-for="drone in drones"
            :key="drone.id"
            :drone="drone"
            @click="toggleSelected(drone.id)"
            :selected="selectedDrones.includes(drone.id)"
          />
        </div>
      </div>

      <!-- Pagination section -->
      <div class="px-6 py-4">
        <pagination :currentPage="currentPage" :totalPages="totalPages" @page-changed="handlePageChange" />
      </div>

      <!-- Create Task Modal -->
      <div v-if="showCreateTaskModal" class="fixed inset-0 z-50 overflow-y-auto bg-gray-500 dark:bg-gray-900 bg-opacity-75 flex items-center justify-center">
        <div class="bg-white dark:bg-gray-800 rounded-lg p-6">
          <h2 :class="{'dark:text-white': isDarkMode}" class="text-lg font-bold mb-4">Create Task</h2>
          <div class="mb-4">
            <label :for="taskName" :class="{'dark:text-white': isDarkMode}" class="block text-sm font-medium text-gray-700">Task Name:</label>
            <input type="text" id="taskName" v-model="taskName" class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
          </div>
          <div class="mb-4">
            <label :for="taskDescription" :class="{'dark:text-white': isDarkMode}" class="block text-sm font-medium text-gray-700">Task Description:</label>
            <textarea id="taskDescription" v-model="taskDescription" class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"></textarea>
          </div>
          <div class="mb-4">
            <p :class="{'dark:text-white': isDarkMode}" class="font-medium">Selected Drones:</p>
            <ul class="list-disc ml-6">
              <li v-for="droneId in selectedDrones" :key="droneId">ID: {{ droneId }}, Name: {{ getDroneName(droneId) }}</li>
            </ul>
          </div>
          <div class="flex justify-end">
            <button @click="closeCreateTaskModal" class="bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-700 text-gray-800 dark:text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-opacity-50">
              Cancel
            </button>
            <button @click="submitCreateTask" class="ml-2 bg-blue-500 dark:bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
              Create Task
            </button>
          </div>
        </div>
      </div>

      <!-- Alert for task creation -->
      <div v-if="alert" class="fixed inset-0 z-50 flex items-center justify-center">
        <div :class="alertClass" class="px-6 py-4 rounded-lg shadow-lg max-w-lg">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <svg v-if="alert.type === 'success'" class="h-8 w-8 text-green-500 dark:text-green-300 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M18.293 1.293a1 1 0 0 1 1.414 1.414l-9 9a1 1 0 0 1-1.414 0l-5-5a1 1 0 0 1 1.414-1.414L9 10.586l8.293-8.293z" clip-rule="evenodd" />
              </svg>
              <svg v-else class="h-8 w-8 text-red-500 dark:text-red-300 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm4.293-11.707a1 1 0 00-1.414 0L10 9.172 7.121 6.293a1 1 0 10-1.414 1.414L8.586 10l-2.879 2.879a1 1 0 101.414 1.414L10 10.828l2.879 2.879a1 1 0 001.414-1.414L11.414 10l2.879-2.879a1 1 0 000-1.414z" clip-rule="evenodd" />
              </svg>
              <div>
                <strong class="font-bold">{{ alert.message }}</strong>
                <p v-if="alert.type === 'success'" class="text-sm">Task ID: {{ alert.id }}</p>
              </div>
            </div>
            <button @click="dismissAlert" class="text-gray-500 dark:text-gray-300 hover:text-gray-700 dark:hover:text-gray-400 focus:outline-none">
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import DroneCard from '@/components/drone/DroneCard.vue';
import Pagination from '@/components/reusable/Pagination.vue';

export default {
  name: 'Drones',
  components: {
    DroneCard,
    Pagination,
  },
  data() {
    return {
      drones: [],
      perPage: 10,
      currentPage: 1,
      totalPages: 1,
      selectedDrones: [],
      perPageOptions: [2, 5, 10, 15],
      showCreateTaskModal: false,
      taskName: '',
      taskDescription: '',
      alert: null,
      isDarkMode: false,
    };
  },
  mounted() {
    this.fetchDrones();
    this.isDarkMode = localStorage.getItem('isDarkMode') === 'true';
  },
  methods: {
    fetchDrones() {
      api.getDrones(this.currentPage, this.perPage)
        .then(response => {
          this.drones = response.data;
          this.totalPages = response.pagination.pages;
        })
        .catch(error => {
          console.error('Error fetching drones:', error);
        });
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchDrones();
    },
    toggleSelected(droneId) {
      if (this.selectedDrones.includes(droneId)) {
        this.selectedDrones = this.selectedDrones.filter(id => id !== droneId);
      } else {
        this.selectedDrones.push(droneId);
      }
    },
    openCreateTaskModal() {
      this.showCreateTaskModal = true;
    },
    closeCreateTaskModal() {
      this.showCreateTaskModal = false;
      this.resetTaskForm();
    },
    resetTaskForm() {
      this.taskName = '';
      this.taskDescription = '';
    },
    getDroneName(droneId) {
      const drone = this.drones.find(drone => drone.id === droneId);
      return drone ? drone.name : 'Unknown';
    },
    submitCreateTask() {
      // Prepare payload
      const payload = {
        name: this.taskName,
        description: this.taskDescription,
        drone_ids: this.selectedDrones,
      };

      // Call API to create task
      api.createTask(payload)
        .then(response => {
          console.log('Task created successfully:', response);
          this.alert = {
            id: response.data.id,
            message: 'Task created successfully!',
            type: 'success',
          };
          this.closeCreateTaskModal();
        })
        .catch(error => {
          console.error('Error creating task:', error);
          this.alert = {
            message: 'Failed to create task. Please try again.',
            type: 'error',
          };
        });
    },
    dismissAlert() {
      this.alert = null;
    },
    // Toggle dark mode
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('isDarkMode', this.isDarkMode);
    },
  },
  computed: {
    alertClass() {
      return this.alert.type === 'success' ? 'bg-green-100 dark:bg-green-800 border border-green-400 text-green-700 dark:text-green-300' : 'bg-red-100 dark:bg-red-800 border border-red-400 text-red-700 dark:text-red-300';
    },
  },
};
</script>

<style scoped>
/* Scoped styles */
</style>

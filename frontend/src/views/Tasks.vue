<template>
  <div :class="{'dark': isDarkMode}" class="bg-gray-200 dark:bg-gray-800 py-6 px-4 sm:px-3 lg:px-4 flex items-center justify-center">
    <div :class="{'dark': isDarkMode}" class="bg-white dark:bg-gray-700 w-full max-w-4xl shadow-md rounded-lg p-4">
      <div>
        <div class="overflow-x-auto">
          <table class="w-full bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 text-center">
            <thead>
              <tr class="bg-gray-100 dark:bg-gray-600">
                <th class="px-6 py-3 border-b border-gray-200 dark:border-gray-600 text-center text-xs font-medium text-gray-500 text-primary-black dark:text-white uppercase tracking-wider">ID</th>
                <th class="px-6 py-3 border-b border-gray-200 dark:border-gray-600 text-center text-xs font-medium text-gray-500 text-primary-black dark:text-white uppercase tracking-wider">Name</th>
                <th class="px-6 py-3 border-b border-gray-200 dark:border-gray-600 text-center text-xs font-medium text-gray-500 text-primary-black dark:text-white uppercase tracking-wider">Description</th>
                <th class="px-6 py-3 border-b border-gray-200 dark:border-gray-600 text-center text-xs font-medium text-gray-500 text-primary-black dark:text-white uppercase tracking-wider">Drone IDs</th>
                <th class="px-6 py-3 border-b border-gray-200 dark:border-gray-600 text-center text-xs font-medium text-gray-500 text-primary-black dark:text-white uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in tasks" :key="task.id">
                <td class="px-6 py-3 text-primary-black dark:text-white whitespace-no-wrap border-b border-gray-200 dark:border-gray-600">{{ task.id }}</td>
                <td class="px-6 py-3 text-primary-black dark:text-white whitespace-no-wrap border-b border-gray-200 dark:border-gray-600">{{ task.name }}</td>
                <td class="px-6 py-3 text-primary-black dark:text-white whitespace-no-wrap border-b border-gray-200 dark:border-gray-600">{{ task.description }}</td>
                <td class="px-6 py-3 text-primary-black dark:text-white whitespace-no-wrap border-b border-gray-200 dark:border-gray-600">{{ task.drone_ids.join(', ') }}</td>
                <td class="px-6 py-3 text-primary-black dark:text-white whitespace-no-wrap border-b border-gray-200 dark:border-gray-600">
                  <button @click="executeTask(task.id)" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
                    Execute Task
                  </button>
                  <button @click="viewTaskImages(task.id)" class="bg-green-500 hover:bg-green-700 text-white font-bold mx-2 py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50">
                    Images
                  </button>
                  <button @click="openEditTaskModal(task)" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-opacity-50">
                    Edit
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <!-- Pagination -->
        <div class="mb-4">
          <pagination :currentPage="currentPage" :totalPages="totalPages" @page-changed="handlePageChange" />
        </div>
      </div>
    </div>
    <!-- Create/Edit Task Modal -->
    <div v-if="showTaskModal" class="fixed inset-0 z-50 overflow-y-auto bg-gray-500 dark:bg-gray-900 bg-opacity-75 flex items-center justify-center">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6">
        <h2 :class="{'dark:text-white': isDarkMode}" class="text-lg font-bold mb-4">{{ isEditMode ? 'Edit Task' : 'Create Task' }}</h2>
        <div class="mb-4">
          <label :for="taskName" :class="{'dark:text-white': isDarkMode}" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Task Name:</label>
          <input type="text" id="taskName" v-model="taskForm.name" class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
        </div>
        <div class="mb-4">
          <label :for="taskDescription" :class="{'dark:text-white': isDarkMode}" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Task Description:</label>
          <textarea id="taskDescription" v-model="taskForm.description" class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50"></textarea>
        </div>
        <div class="mb-4">
          <label :for="drones" :class="{'dark:text-white': isDarkMode}" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Select Drones:</label>
          <select id="drones" v-model="taskForm.drone_ids" multiple class="mt-1 block w-full border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50">
            <option v-for="drone in drones" :key="drone.id" :value="drone.id">{{ drone.name }}</option>
          </select>
        </div>
        <div class="flex justify-end">
          <button @click="closeTaskModal" class="bg-gray-300 dark:bg-gray-600 hover:bg-gray-400 dark:hover:bg-gray-700 text-gray-800 dark:text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-gray-300 focus:ring-opacity-50">
            Cancel
          </button>
          <button @click="submitTask" class="ml-2 bg-blue-500 dark:bg-blue-600 hover:bg-blue-700 dark:hover:bg-blue-800 text-white font-bold py-2 px-4 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
            {{ isEditMode ? 'Update Task' : 'Create Task' }}
          </button>
        </div>
      </div>
    </div>
    <!-- Alert -->
    <div v-if="alert" class="fixed inset-0 z-50 flex items-center justify-center">
      <div :class="alertClass" class="px-6 py-4 rounded-lg shadow-lg max-w-lg">
        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <svg v-if="alert.status === 'success'" class="h-8 w-8 text-green-500 dark:text-green-300 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18.293 1.293a1 1 0 0 1 1.414 1.414l-9 9a1 1 0 0 1-1.414 0l-5-5a1 1 0 0 1 1.414-1.414L9 10.586l8.293-8.293z" clip-rule="evenodd" />
            </svg>
            <svg v-else class="h-8 w-8 text-red-500 dark:text-red-300 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm4.293-11.707a1 1 0 00-1.414 0L10 9.172 7.121 6.293a1 1 0 10-1.414 1.414L8.586 10l-2.879 2.879a1 1 0 101.414 1.414L10 10.828l2.879 2.879a1 1 0 001.414-1.414L11.414 10l2.879-2.879a1 1 0 000-1.414z" clip-rule="evenodd" />
            </svg>
            <div>
              <strong class="font-bold">{{ alert.message }}</strong>
              <p v-if="alert.status === 'success'" class="text-sm">Task ID: {{ alert.task_id }}</p>
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
</template>

<script>
import api from '@/services/api';
import Pagination from '@/components/reusable/Pagination.vue';

export default {
  name: 'Tasks',
  components: {
    Pagination,
  },
  data() {
    return {
      tasks: [],
      drones: [],
      currentPage: 1,
      totalPages: 1,
      perPage: 10,
      showTaskModal: false,
      isEditMode: false,
      taskForm: {
        id: null,
        name: '',
        description: '',
        drone_ids: [],
      },
      alert: null,
      isDarkMode: false,
    };
  },
  mounted() {
    this.fetchTasks();
    this.fetchDrones();
    this.isDarkMode = localStorage.getItem('isDarkMode') === 'true';
  },
  methods: {
    fetchTasks() {
      api.getTasks(this.currentPage, this.perPage)
        .then(response => {
          this.tasks = response.data;
          this.totalPages = response.pagination.pages;
        })
        .catch(error => {
          console.error('Error fetching tasks:', error);
        });
    },
    fetchDrones() {
      api.getDrones()
        .then(response => {
          this.drones = response.data;
        })
        .catch(error => {
          console.error('Error fetching drones:', error);
        });
    },
    handlePageChange(page) {
      this.currentPage = page;
      this.fetchTasks();
    },
    executeTask(taskId) {
      api.executeTask(taskId)
        .then(response => {
          this.alert = { status: response.status, message: response.message, task_id: taskId };
          this.fetchTasks();
        })
        .catch(error => {
          this.alert = { status: 'error', message: 'Error executing task: ' + error.message };
        });
    },
    viewTaskImages(taskId) {
      this.$router.push({ name: 'TaskImages', params: { taskId: taskId } });
    },
    openEditTaskModal(task) {
      this.isEditMode = true;
      this.taskForm = { ...task };
      this.showTaskModal = true;
    },
    closeTaskModal() {
      this.showTaskModal = false;
      this.isEditMode = false;
      this.resetTaskForm();
    },
    submitTask() {
      if (this.isEditMode) {
        this.updateTask();
      } else {
        this.createTask();
      }
    },
    createTask() {
      api.createTask(this.taskForm)
        .then(response => {
          this.alert = { status: response.status, message: 'Task created successfully', task_id: response.data.id };
          this.fetchTasks();
          this.closeTaskModal();
        })
        .catch(error => {
          this.alert = { status: 'error', message: 'Error creating task: ' + error.message };
        });
    },
    updateTask() {
      api.updateTask(this.taskForm)
        .then(response => {
          this.alert = { status: response.status, message: 'Task updated successfully', task_id: response.data.id };
          this.fetchTasks();
          this.closeTaskModal();
        })
        .catch(error => {
          this.alert = { status: 'error', message: 'Error updating task: ' + error.message };
        });
    },
    resetTaskForm() {
      this.taskForm = {
        id: null,
        name: '',
        description: '',
        drone_ids: [],
      };
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
      return this.alert.status === 'success' ? 'bg-green-100 dark:bg-green-800 border border-green-400 text-green-700 dark:text-green-300' : 'bg-red-100 dark:bg-red-800 border border-red-400 text-red-700 dark:text-red-300';
    },
  },
};
</script>

<style scoped>
/* Add scoped styles here if needed */
</style>

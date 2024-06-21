<template>
  <div :class="{'dark': isDarkMode}" class="bg-gray-200 dark:bg-gray-800 flex items-center justify-center py-6 px-4 sm:px-3 lg:px-4">
    <div :class="{'dark': isDarkMode}" class="bg-white dark:bg-gray-700 w-full max-w-4xl shadow-md rounded-lg p-4">
      <div class="">
        <div class="overflow-x-auto">
          <table class="min-w-full bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600">
            <thead :class="{'dark:bg-gray-600': isDarkMode}" class="bg-gray-100 dark:bg-gray-600">
              <tr>
                <th class="px-4 py-2 text-primary-black dark:text-white">Thumbnail</th>
                <th class="px-4 py-2 text-primary-black dark:text-white">Drone ID</th>
                <th class="px-4 py-2 text-primary-black dark:text-white">Capture Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="image in taskImages" :key="image.image_url">
                <td class="px-4 py-2 text-primary-black dark:text-white">
                  <button @click="openModal(image)">
                    <img :src="image.image_url" alt="Task Image" class="h-16 w-auto rounded-lg shadow-md cursor-pointer">
                  </button>
                </td>
                <td class="px-4 py-2 text-primary-black dark:text-white">{{ image.drone_id }}</td>
                <td class="px-4 py-2 text-primary-black dark:text-white">{{ formatDate(image.capture_date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div v-if="modalImageUrl" class="fixed inset-0 z-50 overflow-auto bg-black dark:bg-black bg-opacity-50 flex items-center justify-center">
      <div class="relative p-4 mx-auto max-w-full max-h-full">
        <button @click="modalImageUrl = ''" class="absolute top-0 right-0 m-4 text-white dark:text-gray-300 text-lg font-semibold cursor-pointer">&times;</button>
        <img :src="modalImageUrl" alt="Task Image" class="max-w-full" height="512" width="512">
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';

export default {
  name: 'TaskImages',
  props: ['taskId'],
  data() {
    return {
      taskImages: [],
      modalImageUrl: '',
      isDarkMode: false,
    };
  },
  created() {
    this.getTaskImages();
    this.isDarkMode = localStorage.getItem('isDarkMode') === 'true';
  },
  methods: {
    getTaskImages() {
      api.getTaskImages(this.taskId)
        .then(response => {
          this.taskImages = response.data;
        })
        .catch(error => {
          console.error('Error fetching task images:', error);
        });
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    },
    openModal(image) {
      this.modalImageUrl = image.image_url;
    },
    // Toggle dark mode
    toggleDarkMode() {
      this.isDarkMode = !this.isDarkMode;
      localStorage.setItem('isDarkMode', this.isDarkMode);
    },
  },
};
</script>

<style scoped>
/* Scoped styles */
</style>

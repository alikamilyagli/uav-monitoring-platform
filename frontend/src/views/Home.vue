<!-- src/views/Home.vue -->

<template>
  <div class="container mx-auto">
    <h1 class="text-3xl text-primary-black dark:text-white font-bold text-center mt-8">Welcome to UAV Monitoring Platform</h1>

    <!-- Brief Project Description -->
    <div class="mt-4 text-lg text-primary-black dark:text-white">
      <p>
        On this platform, you can manage all your UAV (drone) operations seamlessly. You can:
        <ul class="list-disc list-inside mt-2">
          <li>Create and define new tasks for your drones</li>
          <li>Assign specific tasks to individual drones</li>
          <li>Execute tasks and monitor their progress in real-time</li>
          <li>Retrieve and review images captured during task execution</li>
        </ul>
        This platform provides a comprehensive solution for efficient drone task management and image retrieval.
      </p>
    </div>

    <!-- Card buttons for /drones and /tasks -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-8">
      <!-- Card for Drones Page -->
      <router-link to="/drones">
        <div class="bg-white rounded-lg shadow-md p-4 hover:bg-gray-100 cursor-pointer transition">
          <h2 class="text-xl font-bold text-primary-dark">Manage Drones</h2>
          <p class="text-gray-600 mt-2">Click here to manage drones</p>
        </div>
      </router-link>

      <!-- Card for Tasks Page -->
      <router-link to="/tasks">
        <div class="bg-white rounded-lg shadow-md p-4 hover:bg-gray-100 cursor-pointer transition">
          <h2 class="text-xl font-bold text-primary-dark">Manage Tasks</h2>
          <p class="text-gray-600 mt-2">Click here to manage tasks</p>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
/* Add scoped styles here */
</style>

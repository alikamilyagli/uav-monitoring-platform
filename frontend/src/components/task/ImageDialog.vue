<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" @click.self="close">
    <div class="flex items-center justify-center min-h-screen">
      <div class="bg-white p-4 shadow-lg rounded-lg">
        <div v-for="(image, index) in images" :key="index" class="mb-4">
          <img :src="image" alt="Task Image" class="max-w-full max-h-96 mx-auto" />
        </div>
        <button @click="close"
                class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded">
          Close
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isOpen: false,
      images: [],
    };
  },
  methods: {
    open() {
      this.isOpen = true;
    },
    close() {
      this.isOpen = false;
    },
    setImages(images) {
      this.images = images;
    },
  },
};
</script>

<style scoped>
/* Scoped styles */
</style>

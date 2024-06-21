<template>
  <nav class="pagination flex items-center justify-center mt-4">
    <button @click="prevPage" :disabled="currentPage === 1"
      class="bg-gray-200 hover:bg-gray-300 text-gray-700 hover:text-gray-900 font-semibold py-2 px-4 rounded-l-md focus:outline-none"
    >
      Prev
    </button>
    <span class="pagination-info px-4">{{ currentPage }} / {{ totalPages }}</span>
    <button @click="nextPage" :disabled="currentPage === totalPages"
      class="bg-gray-200 hover:bg-gray-300 text-gray-700 hover:text-gray-900 font-semibold py-2 px-4 rounded-r-md focus:outline-none"
    >
      Next
    </button>
  </nav>
</template>

<script>
export default {
  name: 'Pagination',
  props: {
    currentPage: Number,
    totalPages: Number,
  },
  methods: {
    prevPage() {
      if (this.currentPage > 1) {
        this.$emit('page-changed', this.currentPage - 1);
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.$emit('page-changed', this.currentPage + 1);
      }
    },
  },
};
</script>

<style scoped>
/* Scoped styles */
.pagination {
  /* Optional: Add container-wide styles if needed */
}

.pagination-info {
  /* Optional: Add styles for the pagination info */
}
</style>

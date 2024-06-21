<template>
  <div class="bg-white rounded shadow p-4" :class="{ 'border-2 border-blue-500': isSelected }">
    <!-- Drone icon -->
    <img src="@/assets/images/drone.png" alt="Drone Icon" class="w-16 h-16 mb-4 mx-auto">

    <h2 class="text-lg font-bold text-center">{{ drone.name }}</h2>
    <p class="text-center text-gray-600">{{ drone.description }}</p>

    <!-- Checkbox for selection -->
    <input type="checkbox" :checked="isSelected" class="mt-4 mx-auto" @change="toggleSelection">
    <label class="ml-2 cursor-pointer" @click="toggleSelection" />
  </div>
</template>

<script>
export default {
  name: 'DroneCard',
  props: {
    drone: Object,
    selected: Boolean,
  },
  computed: {
    isSelected: {
      get() {
        return this.selected;
      },
      set(value) {
        this.$emit('toggle', this.drone.id, value);
      },
    },
  },
  methods: {
    toggleSelection() {
      this.isSelected = !this.isSelected;
    },
  },
};
</script>

<style scoped>
/* Scoped styles */
</style>

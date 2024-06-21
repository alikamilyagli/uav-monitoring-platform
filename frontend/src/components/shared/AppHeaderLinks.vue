<script>
export default {
	props: ['showModal', 'isOpen'],
};
</script>

<template>
	<!-- Header links -->
	<div
		:class="isOpen ? 'block' : 'hidden'"
		class="m-0 sm:ml-4 mt-5 sm:mt-3 sm:flex p-5 sm:p-0 justify-center items-center shadow-lg sm:shadow-none"
	>
		<router-link
			to="/drones"
			class="font-general-medium block text-left text-lg font-medium text-primary-dark dark:text-ternary-light sm:mx-4 mb-2 sm:py-2 "
			aria-label="Drones"
			>Drones</router-link
		>
		<router-link
			to="/tasks"
			class="font-general-medium block text-left text-lg font-medium text-primary-dark dark:text-ternary-light sm:mx-4 mb-2 sm:py-2 border-t-2 pt-3 sm:pt-2 sm:border-t-0 border-primary-light dark:border-secondary-dark"
			aria-label="Tasks"
			>Tasks</router-link
		>

	</div>
</template>

<style lang="scss" scoped></style>

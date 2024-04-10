<template>
		<div class="background">
			<!-- Your login component content here -->
			<LogInView />
		</div>
</template>

<script>
import LogInView from '../views/LogInView.vue';

export default {
	name: 'LogIn',
	components: {
		LogInView
	},
	// Your component's logic here
}
</script>

<style scoped>
</style>
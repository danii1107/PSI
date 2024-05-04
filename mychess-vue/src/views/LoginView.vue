<template>
	<div class="background-image">
		<div class="row">
			<div class="column" v-for="(image, index) in visibleImages.slice(0, 3)" :key="index" :style="transitionStyles">
				<img :src="image" :alt="'Image ' + (index + 1)" />
			</div>
		</div>
		<div class="row">
			<div class="column" v-for="(image, index) in visibleImages.slice(3, 6)" :key="index + 3" :style="transitionStyles">
				<img :src="image" :alt="'Image ' + (index + 4)" />
			</div>
		</div>
		<login @LoginAPI="consumeAPI" />
	</div>
</template>

<script>
	import Login from '../components/Login.vue';
	import { ref, onMounted } from 'vue';
	import { useCounterStore } from '../stores/counter';
	import { useTokenStore } from '../stores/token'

	const apiURL = import.meta.env.VITE_DJANGOURL;

	import image1 from '../assets/logn-bg.jpg';
	import image2 from '../assets/fak.jpg';
	import image3 from '../assets/REINA.jpg';
	import image4 from '../assets/sign-up-bg.jpg';
	import image5 from '../assets/logn-bg.jpg';
	import image6 from '../assets/fak.jpg';

	export default {
		components: {
			Login
		},
		setup() {
			const personas = ref([]);
			const store = useCounterStore();
			const tokenStore = useTokenStore();
			const images = ref([image1, image2, image3, image4, image5, image6]);
			const visibleImages = ref([...images.value]);
			const transitionDuration = ref(500);

			const moveImages = () => {
				visibleImages.value = [...images.value.slice(1), images.value[0]];
				images.value = [...visibleImages.value];
			};

			const transitionStyles = {
				transition: 'opacity ${transitionDuration.value}ms ease-in-out',
			};

			onMounted(() => {
				setInterval(moveImages, 3000);
			});

			const consumeAPI = async (persona) => {
				
				try {
					const response = await fetch(apiURL + '/api/v1/mytokenlogin/', {
						method: 'POST',
						body: JSON.stringify(persona),
						headers: { 'Content-type': 'application/json; charset=UTF-8' },
					});
					if (response.ok) {
						const personaCreada = await response.json();
						personas.value = [...personas.value, personaCreada];
						store.increment();
						tokenStore.setToken(personaCreada.auth_token, personaCreada.user_id);
					}
				} catch (error) {
					console.error(error);
				}
			};

			return {
				personas,
				consumeAPI,
				store,
				tokenStore,
				visibleImages,
				transitionStyles
			};
		}
	};
</script>

<style scoped>
	.background-image {
		width: 100vw;
		height: 100vh;
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		overflow: hidden;
	}

	.row {
		display: flex;
		flex-direction: row;
		width: 100%;
		height: 50%;
	}

	.column {
		flex: 1;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.column img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}
</style>
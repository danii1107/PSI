<template>
  <div class="background-image">
    <div
      class="container"
      data-cy="logoutPage"
    >
      <h1>Log Out</h1>
      <p>Has cerrado sesión exitosamente. Serás redirigido a la página de inicio en 5 segundos.</p>
    </div>
  </div>
</template>
  
  <script>
  import { useTokenStore } from '../stores/token';
  import { useRouter } from 'vue-router';
  import { onMounted } from 'vue';
  
  export default {
	name: 'LogOutView',
	setup() {
	  const router = useRouter();
	  const store = useTokenStore();
    const apiURL = import.meta.env.VITE_DJANGOURL;
    
	  

    const logOut = async () => {
				try {
					const response = await fetch(`${apiURL}/api/v1/token/logout`, {
						method: 'POST',
						headers: {
							'Authorization': 'token ' + store.token,
							'Accept': 'application/json',
							'Content-Type': 'application/json' 
						},
					});
					if (response.ok) {
            store.removeToken();
            setTimeout(() => {
              router.push("/log-in");
            }, 5000);
					}else{
            console.log("a");
          }
				} catch (error) {
					console.error(error);
				}
			};

      onMounted(() => {
        logOut(); 
      });
	}
  }
  </script>
  
  <style scoped>
  .background-image {
	width: 100vw;
	height: 100vh;
	background-image: url('../assets/REINA.jpg');
	background-size: cover;
	background-repeat: no-repeat;
	background-position: center;
  }
  
  .container {
	color: white;
	text-align: center;
  }
  </style>
  
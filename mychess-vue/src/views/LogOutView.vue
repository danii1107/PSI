<template>
  <div
    class="background-image"
    data-cy="logoutPage"
  >
    <div class="text">
      <p class="logout">
        Log Out
      </p>
      <p class="log-out-text">
        Goodbye! Come back soon!
      </p> 
      <p class="redirect">
        You will be redirected to login page in 5 seconds
      </p>
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
	background-image: url('../assets/LOGOUT.jpg');
	background-size: cover;
	background-repeat: no-repeat;
	background-position: center;
  display: flex;
  }

  .text {
    margin-top: 13%;
    text-align: center;
    margin-left: 50%;
  }
  .logout {
    font-size: 2rem;
    font-family: Verdana, Tahoma, sans-serif;
    color: white;
  }
  .log-out-text {
    font-size: 1.5rem;
    font-family: Verdana, Tahoma, sans-serif;
    color: white;
  }
  .redirect {
    font-size: 1rem;
    font-family: Verdana, Tahoma, sans-serif;
    color: white;
  }
  </style>
  
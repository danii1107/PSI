<template>
  <div class="background-image">
  <div id="app">
    <LoginView />
  </div>
</div>
</template>

<script>
import LoginView from './components/LogIn.vue';

export default {
  name: 'App',
  components: {
    LoginView
  }
}
</script>

<style>
.background-image {
	background-image: url('assets/logn-bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  height: 100vh;
  width: 100vw;
  }
</style>
<template>
  <div id="app">
    <NavBar />
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import NavBar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    NavBar
  }
};
</script>

<style>
#app {
  font-family: Roboto, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-image: linear-gradient(to right, #C9D6FF, #E2E2E2);
}

.main-content {
  overflow-y: auto;
  height: 100vh;
}

body {
  height: 100vh;
  margin: 0;
}
</style>

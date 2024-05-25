<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-body-tertiary fixed-top">
    <!-- Container wrapper -->
    <div class="container-fluid">
      <!-- Toggle button -->
      <button data-mdb-collapse-init class="navbar-toggler" type="button" data-mdb-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
      </button>

      <!-- Collapsible wrapper -->
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <!-- Navbar brand -->
        <router-link class="navbar-brand mt-2 mt-lg-0" to="/">
          <img src="../assets/img/logo.svg" height="30" alt="Brandly Logo" loading="lazy" />
          <p class="mb-0 title">Brandly</p>
        </router-link>
      </div>
      <!-- Collapsible wrapper -->

      <!-- Avatar -->
      <div v-if="isLoggedIn" class="dropdown">
        <a data-mdb-dropdown-init class="dropdown-toggle d-flex align-items-center" href="#"
          id="navbarDropdownMenuAvatar" role="button" aria-expanded="true">
          <img src="https://mdbcdn.b-cdn.net/img/new/avatars/2.webp" class="rounded-circle" height="25"
            alt="Black and White Portrait of a Man" loading="lazy" />
        </a>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuAvatar">
          <li>
            <a class="dropdown-item" href="#">My profile</a>
          </li>
          <li>
            <a class="dropdown-item" href="#">Settings</a>
          </li>
          <li>
            <a class="dropdown-item" @click="logout" href="#">Logout</a>
          </li>
        </ul>
      </div>

      <!-- Right elements -->
      <div v-else class="d-flex align-items-center">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <a class="nav-link text-black" href="#">Admin</a>
          </li>
        </ul>
      </div>
      <!-- Right elements -->
    </div>
    <!-- Container wrapper -->
  </nav>
  <!-- Navbar -->
</template>

<script>
import { Dropdown, Collapse, initMDB } from "mdb-ui-kit";

export default {
  name: 'NavBar',
  mounted() {
    this.initMDBInputs();
    this.isLoggedIn = localStorage.getItem('accessToken') !== null;
  },
  updated() {
    this.initMDBInputs();
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.isLoggedIn;
    },
  },
  methods: {
    initMDBInputs() {
      initMDB({ Dropdown, Collapse });
    },
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/register')
    },
  },
};
</script>

<style scoped>
.title {
  font-family: "Poetson One", cursive;
  font-weight: 400;
  color: #8d3400;
}

.link-text {
  font-family: 'Rubik', 'Lucida Sans';
  text-decoration: none;
  color: #1a1a1a;
  font-weight: 400;
}
</style>

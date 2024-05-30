<template>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-body-tertiary fixed-top">
    <!-- Container wrapper -->
    <div class="container-fluid">
      <!-- Toggle button -->
      <button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarSupportedContent"
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
      <div v-if="isLoggedIn && user" class="dropdown">
        <a class="dropdown-toggle d-flex align-items-center" href="#" id="navbarDropdownMenuAvatar" role="button"
          data-mdb-toggle="dropdown" aria-expanded="false">
          <img src="../assets/img/avatar.svg" class="rounded-circle" height="35"
            alt="Black and White Portrait of a Man" loading="lazy" />
        </a>
        <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdownMenuAvatar">
          <li v-if="user.email && user.role">
            <span class="dropdown-item-text mb-0">{{ user.email }}<br> Role: {{ user.role }}</span>
          </li>
          <li>
            <hr class="dropdown-divider mt-0 mb-0"/>
            <router-link class="dropdown-item mb-0" to="/editProfile">Edit Profile</router-link>
          </li>
          <li>
            <a class="dropdown-item mt-0" @click="logout" href="#">Logout</a>
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
import { mapState, mapActions } from 'vuex';
import { Dropdown, Collapse, initMDB } from 'mdb-ui-kit';

export default {
  name: 'NavBar',
  computed: {
    ...mapState(['isLoggedIn']),
    user() {
      return this.$store.state.user;
    },
  },
  methods: {
    ...mapActions(['logout']),
    initMDBInputs() {
      initMDB({ Dropdown, Collapse });
      new Dropdown(document.getElementById('navbarDropdownMenuAvatar'));
    },
  },
  mounted() {
    this.initMDBInputs();
  },
  updated() {
    this.initMDBInputs();
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

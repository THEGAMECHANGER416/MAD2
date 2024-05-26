<template>
  <section class="vh-100 mb-0 my-5">
    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-6 text-black">
          <div class="d-flex align-items-center h-100 px-5 ms-xl-4">
            <form @submit.prevent="handleSubmit" style="width: 23rem;">
              <div id="radius-shape-3" class="position-absolute rounded-circle shadow-5-strong"></div>
              <div id="radius-shape-4" class="position-absolute shadow-5-strong"></div>

              <h2 class="my-5 display-5 fw-bold" style="color: #fafafa">Login</h2>

              <!-- Email input -->
              <div data-mdb-input-init class="form-outline form-white mb-4">
                <input type="email" id="form3Example3" class="form-control form-control-lg" v-model="formData.email"
                  required>
                <label class="form-label" for="form3Example3">Email address</label>
              </div>

              <!-- Password input -->
              <div data-mdb-input-init class="form-outline form-white mb-4">
                <input type="password" id="form3Example4" class="form-control form-control-lg"
                  v-model="formData.password" required />
                <label class="form-label" for="form3Example4">Password</label>
              </div>

              <div class="pt-1 mb-4">
                <button type="submit" data-mdb-button-init data-mdb-ripple-init
                  class="btn btn-login btn-lg btn-block">Login</button>
              </div>

              <div v-if="errorMessage" class="alert alert-warning mt-3" role="alert">
                {{ errorMessage }}
              </div>

              <p style="color: #fafafa">Don't have an account? <router-link to="/register" class="link-primary">Register
                  here</router-link></p>
            </form>
          </div>
        </div>
        <div class="col-sm-6 px-0 d-none d-sm-block">
          <img src="../assets/img/bg1.jpg" alt="Login image" class="w-100 vh-100"
            style="object-fit: cover; object-position: right;">
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapActions } from 'vuex';
import { Input, initMDB } from 'mdb-ui-kit';

export default {
  name: 'LoginPage',
  data() {
    return {
      formData: {
        email: '',
        password: '',
      },
      errorMessage: '',
    };
  },
  mounted() {
    this.initMDBInputs();
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
      this.$router.push('/');
    }
  },
  methods: {
    ...mapActions(['login']),
    initMDBInputs() {
      const formOutlines = document.querySelectorAll('.form-outline');
      if (formOutlines.length === 0) {
        console.warn('No form outlines found.');
        return;
      }
      initMDB({ Input });
      formOutlines.forEach((formOutline) => {
        new Input(formOutline).init();
      });
    },
    handleSubmit() {
      const myHeaders = new Headers();
      myHeaders.append('Content-Type', 'application/json');

      const requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: JSON.stringify(this.formData),
        redirect: 'follow',
      };

      fetch('http://127.0.0.1:8000/api/login', requestOptions)
        .then((response) => {
          if (!response.ok) {
            return response.json().then((data) => {
              throw new Error(data.msg || 'Network response was not ok');
            });
          }
          return response.json();
        })
        .then((data) => {
          const accessToken = data.access_token;
          const userData = data.user;
          console.log(userData, accessToken)
          if (accessToken && userData) {
            this.$store.dispatch('login', { user: userData, accessToken: accessToken });
          }
        })
        .catch((error) => {
          this.errorMessage = error.message;
        });
    },
  },
};
</script>

<style>
.bg-image-vertical {
  position: relative;
  overflow: hidden;
  background-repeat: no-repeat;
  background-position: right center;
  background-size: auto 100%;
}

.link-primary {
  color: rgb(138, 186, 250) !important;
}

.vh-100 {
  height: 93vh !important;
  background: linear-gradient(15deg, #5c180f, #7e1a12, #a31a1b, #c51e22);
}

.btn-login {
  background: #a31a1b;
  color: #fafafa;
  transition: background-color 0.3s, color 0.3s;
}

.btn-login:hover {
  background: #c51e22;
  color: #ffffff;
}

#radius-shape-3 {
  height: 220px;
  width: 220px;
  top: -20px;
  left: 220px;
  opacity: 0.1;
  background: radial-gradient(#881600, #c16200);
  overflow: hidden;
}

#radius-shape-4 {
  border-radius: 38% 62% 63% 37% / 70% 33% 67% 30%;
  bottom: 0px;
  right: 740px;
  width: 300px;
  height: 300px;
  opacity: 0.1;
  background: radial-gradient(#4e0110, #bd6f26);
  overflow: hidden;
}

.d-flex.align-items-center {
  height: 100%;
  overflow: hidden !important;
}
</style>

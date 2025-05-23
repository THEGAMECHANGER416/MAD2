<template>
  <section class="background-radial-gradient overflow-hidden mb-0">
    <div class="container px-4 py-5 px-md-5 text-center text-lg-start my-5 mb-0">
      <div class="row gx-lg-5 align-items-center mb-5">
        <div class="col-lg-6 mb-5 mb-lg-0" style="z-index: 10">
          <h1 class="my-5 display-5 fw-bold ls-tight" style="color: #fafafa">
            Connecting Sponsors <br />
            <span style="color: #ffdb8c">with Top Influencers</span>
          </h1>
          <p class="mb-4" style="color: #fafafa">
            Discover the perfect partnership to elevate your brand. Our platform brings together
            Sponsors and Influencers to create impactful collaborations. Join us to explore
            opportunities, enhance your reach, and grow your business.
          </p>
        </div>

        <div class="col-lg-6 mb-5 mb-lg-0 position-relative">
          <div id="radius-shape-1" class="position-absolute rounded-circle shadow-5-strong"></div>
          <div id="radius-shape-2" class="position-absolute shadow-5-strong"></div>

          <div class="card bg-glass">
            <div class="card-body px-4 py-5 px-md-5">
              <form @submit.prevent="handleSubmit">
                <!-- Email input -->
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="email" id="form3Example3" class="form-control" v-model="formData.email" required>
                  <label class="form-label" for="form3Example3">Email address</label>
                </div>

                <!-- Password input -->
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="password" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
                    title="Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters"
                    id="form3Example4" class="form-control" v-model="formData.password" required />
                  <label class="form-label" for="form3Example4">Password</label>
                </div>

                <!-- Confirm Password input -->
                <div data-mdb-input-init class="form-outline mb-4">
                  <input type="password" id="form3Example5" class="form-control" v-model="formData.confirmPassword"
                    required />
                  <label class="form-label" for="form3Example5">Confirm Password</label>
                </div>

                <!-- Warning message for password mismatch -->
                <div v-if="!passwordsMatch" class="alert alert-danger mb-3" role="alert">
                  Passwords do not match. Please try again.
                </div>

                <!-- User type radio buttons -->
                <div class="row">
                  <div class="col-md-6 mb-4">
                    <div class="form-check-inline">
                      <input class="form-check-input" type="radio" id="Sponsor" value="Sponsor" v-model="userType"
                        @change="handleChangeUserType(userType)">
                      <label class="form-check-label" for="Sponsor">Sponsor</label>
                    </div>
                  </div>
                  <div class="col-md-6 mb-4">
                    <div class="form-check-inline">
                      <input class="form-check-input" type="radio" id="Influencer" value="Influencer" v-model="userType"
                        @change="handleChangeUserType(userType)">
                      <label class="form-check-label" for="Influencer">Influencer</label>
                    </div>
                  </div>
                </div>

                <!-- Conditional input fields based on user type -->
                <template v-if="userType === 'Sponsor'">
                  <div data-mdb-input-init class="form-outline mb-4">
                    <input type="text" id="companyName" class="form-control" v-model="formData.companyName" />
                    <label class="form-label" for="companyName">Company Name</label>
                  </div>
                  <div data-mdb-input-init class="form-outline mb-4">
                    <input type="text" id="industry" class="form-control" v-model="formData.industry" />
                    <label class="form-label" for="industry">Industry</label>
                  </div>
                  <div data-mdb-input-init class="form-outline mb-4">
                    <input type="number" id="budget" class="form-control" v-model="formData.budget" />
                    <label class="form-label" for="budget">Budget</label>
                  </div>
                </template>
                <template v-if="userType === 'Influencer'">
                  <div data-mdb-input-init class="form-outline mb-4">
                    <input type="text" id="name" class="form-control" v-model="formData.name" />
                    <label class="form-label" for="name">Full Name</label>
                  </div>
                  <div data-mdb-input-init class="form-outline mb-4">
                    <input type="text" id="category" class="form-control" v-model="formData.category" />
                    <label class="form-label" for="category">Category</label>
                  </div>
                  <div data-mdb-input-init class="form-outline mb-4">
                    <input type="text" id="niche" class="form-control" v-model="formData.niche" />
                    <label class="form-label" for="niche">Niche</label>
                  </div>
                  <div data-mdb-input-init class="form-outline mb-4">
                    <input type="number" id="reach" class="form-control" v-model="formData.reach" />
                    <label class="form-label" for="reach">Reach</label>
                  </div>
                </template>

                <!-- Submit button -->
                <button type="submit" data-mdb-button-init data-mdb-ripple-init class="btn btn-primary btn-block mb-4">
                  Sign up
                </button>

                <div v-if="errorMessage" class="alert alert-warning mt-3" role="alert">
                  {{ errorMessage }}
                </div>

                <!-- Already a member? Login Instead link -->
                <div class="text-center mt-3">
                  <p>Already a member? <router-link to="/login">Login</router-link></p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { Input, initMDB } from "mdb-ui-kit";
import { mapActions } from 'vuex';

export default {
  name: "SignupPage",
  data() {
    return {
      userType: 'Sponsor',
      formData: {
        email: '',
        password: '',
        confirmPassword: '',
        companyName: '',
        industry: '',
        budget: null,
        role: 'Sponsor',
        name: '',
        category: '',
        niche: '',
        reach: null
      },
      passwordsMatch: true,
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
    handleChangeUserType(newUserType) {
      this.userType = newUserType;
      this.formData.role = newUserType;
      setTimeout(() => {
        this.initMDBInputs();
      }, 0);
    },
    handleSubmit() {
      if (!this.passwordsMatch) {
        return;
      }
      const myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      const requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: JSON.stringify(this.formData),
        redirect: "follow"
      };

      fetch("http://127.0.0.1:8000/api/signup", requestOptions)
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
          if (accessToken && userData) {
            this.$store.dispatch('login', { user: userData, accessToken: accessToken });
          }
        })
        .catch((error) => {
          this.errorMessage = error.message;
        });
    }
  },
  watch: {
    'formData.confirmPassword': function (newConfirmPassword) {
      this.passwordsMatch = newConfirmPassword === this.formData.password;
    }
  }
}
</script>

<style>
.background-radial-gradient {
  background-color: #c16200;
  background-image: radial-gradient(650px circle at 0% 0%, #d27300 15%, #b45600 35%, #994500 75%, #7d3700 100%),
    radial-gradient(1250px circle at 100% 100%, #d27300 15%, #b45600 35%, #994500 75%, #7d3700 100%);
}

#radius-shape-1 {
  height: 220px;
  width: 220px;
  top: -60px;
  left: -130px;
  background: radial-gradient(#881600, #c16200);
  overflow: hidden;
}

#radius-shape-2 {
  border-radius: 38% 62% 63% 37% / 70% 33% 67% 30%;
  bottom: -60px;
  right: -110px;
  width: 300px;
  height: 300px;
  background: radial-gradient(#4e0110, #bd6f26);
  overflow: hidden;
}

.bg-glass {
  background-color: hsla(0, 0%, 100%, 0.9) !important;
  backdrop-filter: saturate(200%) blur(25px);
}
</style>

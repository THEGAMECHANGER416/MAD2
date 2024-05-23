<template>
    <div class="d-flex flex-column" style="height: 100vh;">
      <div>
        <NavBar />
      </div>
      <div class="flex-grow-1 d-flex justify-content-start align-items-center gap-3">
        <div class="d-flex flex-column align-items-center mr-3">
          <img src="../assets/img/character2.gif" height="400" width="440">
        </div>
        <div class="d-flex flex-grow-1 flex-column align-items-start ms-4 me-4">
          <p class="d-flex text-basic">Elevate your brand with ease! Connect sponsors and influencers seamlessly for impactful collaborations that drive results.</p>
          <div class="d-flex flex-start flex-row">
            <button class="btn btn-primary me-2" @click="loginClicked">Login</button>
            <button class="btn btn-outline-primary" @click="signupClicked">Signup</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import NavBar from "./Navbar.vue"
  import { router } from "../main"; // Adjust the path to your router instance
  
  export default {
    name: 'HomePage',
    components: {
      NavBar,
    },
    methods: {
      loginClicked() {
        router.push('/login'); // Route to the login page
      },
      signupClicked() {
        router.push('/signup'); // Route to the signup page
      }
    }
  }
  </script>
  
  <style>
  .text-basic {
      font-family: 'Rubik','Lucida Sans';
      font-size: 1.4rem;
      font-weight: 400;
      color: #1a1a1a;
  }
  </style>
  
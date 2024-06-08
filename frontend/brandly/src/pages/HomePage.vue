<template>
  <div class="mb-0 container-fluid wrapper-class">
    <div v-if="user">
      <div v-if="role === 'Influencer'">Role: Influencer</div>
      <div v-else-if="role === 'Sponsor'">
        <SponsorHome />
      </div>
      <div v-else>Role: Unknown</div>
    </div>
    <div v-else>
      <p>Please log in to view this page.</p>
    </div>
  </div>
</template>

<script>
import SponsorHome from '../components/SponsorHome.vue';

export default {
  name: 'HomePage',
  components:{
    SponsorHome
  },
  computed: {
    user() {
      return this.$store.state.user;
    },
    role() {
      return this.$store.state.role;
    }
  },
  created() {
    this.fetchUserDetails();
  },
  methods: {
    fetchUserDetails() {
      try {
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
          this.$router.push('/register')
        }

        const myHeaders = new Headers();
        myHeaders.append("Authorization", `Bearer ${accessToken}`);

        const requestOptions = {
          method: "GET",
          headers: myHeaders,
          redirect: "follow"
        };

        fetch("http://127.0.0.1:8000/api/profile", requestOptions)
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.json();
          })
          .then((data) => {
            const userData = data;
            this.$store.dispatch("updateUser", userData);
          })
          .catch((error) => {
            console.error(error);
            this.$store.dispatch('logout');
          });
      } catch (error) {
        console.error('Error fetching user details:', error.message);
        this.$store.dispatch('logout');
      }
    }
  }
}
</script>

<style>
.wrapper-class {
  margin-top: 5em;
}
</style>

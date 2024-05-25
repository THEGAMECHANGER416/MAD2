<template>
    <div class="mb-0 container-fluid">
        <h1>Home Page</h1>
    </div>
</template>
<script>
export default {
  name: 'HomePage',
  mounted() {
    const accessToken = localStorage.getItem('accessToken');
    if (!accessToken) {
      this.$router.push('/register');
    }
  }
}
</script>

<style>
    
</style>
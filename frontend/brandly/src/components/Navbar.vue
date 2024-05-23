<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-transparent">
        <div class="container-fluid d-flex justify-content-between align-items-center">
            <a class="navbar-brand d-flex align-items-center" href="#">
                <img src="../assets/img/logo.svg" alt="Logo" width="32" height="30" class="align-text-top">
                <h3 class="title mb-0 ml-2">Brandly</h3>
            </a>
            <div class="d-flex align-items-center">
                <router-link to="/admin" class="link-text mx-2">Admin</router-link>
            </div>
        </div>
    </nav>

</template>
<script>

export default {
    name: 'NavBar'
}
</script>
<style scoped>
.title {
    font-family: "Poetson One", cursive;
    font-weight: 400;
    color: #8d3400;
}

.link-text {
    font-family: 'Rubik','Lucida Sans';
    text-decoration: none;
    color: #1a1a1a;
    font-weight: 400;
}
</style>
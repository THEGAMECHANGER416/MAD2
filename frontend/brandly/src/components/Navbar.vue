<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand d-flex align-items-center" href="#">
                <img src="../assets/img/logo.svg" alt="Logo" width="32" height="30" class="align-text-top">
                <h3 class="title mb-0 ml-2">Brandly</h3>
            </a>
            <div class="ml-auto d-flex align-items-center collapse">
                <button class="btn btn-outline-primary">Login</button>
                <button class="btn btn-primary mx-1">Sign Up</button>
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
    color: #ff4906;
}
</style>
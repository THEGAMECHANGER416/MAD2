<template>
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-body-tertiary fixed-top">
        <!-- Container wrapper -->
        <div class="container-fluid">
            <!-- Toggle button -->
            <button data-mdb-collapse-init class="navbar-toggler" type="button"
                data-mdb-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <i class="fas fa-bars"></i>
            </button>

            <!-- Collapsible wrapper -->
            <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <!-- Navbar brand -->
                <a class="navbar-brand mt-2 mt-lg-0" href="#">
                    <img src="../assets/img/logo.svg" height="30"
                        alt="Brandly Logo" loading="lazy" />
                    <p class="mb-0 title">Brandly</p>
                </a>
            </div>
            <!-- Collapsible wrapper -->

            <!-- Right elements -->
            <div class="d-flex align-items-center">
                <!-- Right links -->
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link text-black" href="#">Admin</a>
                    </li>
                </ul>
                <!-- Right links -->
            </div>
            <!-- Right elements -->
        </div>
        <!-- Container wrapper -->
    </nav>
    <!-- Navbar -->
</template>
<script>
// Initialization for ES Users
import { Dropdown, Collapse, initMDB } from "mdb-ui-kit";

export default {
    name: 'NavBar',
    mounted() {
        // Ensure that MDB is initialized after the component is mounted
        this.initMDBInputs();
    },
    methods: {
        initMDBInputs() {
            initMDB({ Dropdown, Collapse });
        }
    }
}
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
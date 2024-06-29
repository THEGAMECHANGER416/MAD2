<template>
    <div class="container">
        <div class="mb-3">
            <span @click="goBack" class="back-button">
                <i class="fas fa-arrow-left"></i> Back
            </span>
        </div>
        <h1>Ad Request</h1>
        <div class="mb-3">
            Title
        </div>
    </div>
</template>
<script>
import { Input, initMDB } from "mdb-ui-kit";

export default {
    name: 'CreateAdRequest',
    props: {
        id: {
            type: Number,
            required: true
        },
    },
    mounted() {
        this.initMDBInputs();
    },
    methods: {
        goBack() {
            this.$router.back();
        },
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
    }
}
</script>
<style scoped>
.container {
    margin-top: 5em;
}
</style>
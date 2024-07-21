<template>
    <div class="influencer-card">
        <div class="d-flex flex-column align-items-center justify-content-between">
            <div class="d-flex flex-row align-items-top justify-content-between">
                <img :src="'http://localhost:8000' + influencer.image" alt="Influencer" class="mb-3 me-4" style="width: 100px; height: 100px; object-fit: cover;" />
                <div class="d-flex flex-column flex-grow-1 ms-3">
                    <h3 class="card-title mb-1">{{ influencer.name }}</h3>
                    <p class="card-text mb-0"><strong>Category:</strong> {{ influencer.category }}</p>
                    <p class="card-text mb-0"><strong>Reach:</strong> {{ influencer.reach }}</p>
                    <p class="card-text mb-1"><strong>Niche:</strong> {{ influencer.niche }}</p>        
                </div>
            </div>
            <div class="d-flex flex-row justify-content-end w-100">
                <button @click="$emit('sendRequest', influencer)" class="btn btn-rounded btn-primary btn-success btn-sm w-100">
                    <i class="fas fa-plus fa-xl"></i> <!-- Removed extra padding from icon -->
                </button>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: 'InfluencerCard',
    props: {
        influencer: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
        }
    },
    methods: {
    }
}
</script>
<style scoped>
.influencer-card {
    border-radius: 15px;
    padding: 1.5rem;
    width: 100%;
    margin: 1rem;
    box-shadow: none;
    background: white;
}

.platform-icon {
    font-size: 1.7rem;
    /* Adjust size as needed */
}

.btn {
    padding: 0.55rem 1.5rem;
}
</style>
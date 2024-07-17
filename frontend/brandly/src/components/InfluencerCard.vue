<template>
    <div class="influencer-card">
        <div class="card-body w-100 d-flex align-items-center flex-column justify-content-between">
                <h3 class="card-title mb-3">{{ influencer.name }}</h3>
                <p class="card-text mb-0 me-2"><strong>Category:</strong> {{ influencer.category }}</p>
                <p class="card-text mb-0"><strong>Reach:</strong> {{ influencer.reach }}</p>
                <p class="card-text mb-1"><strong>Niche:</strong> {{ influencer.niche }}</p>
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
<template>
    <div class="card ad-request-card w-100">
        <div class="card-body">
            <h5 class="card-title">{{ ad.goal }}</h5>
            <p class="card-text">Platform: {{ ad.platform }}</p>
            <p class="card-text">Target Audience: {{ ad.target_audience }}</p>
            <p class="card-text">Budget: ${{ ad.budget }}</p>
            <p class="card-text">Status: {{ ad.status }}</p>
        </div>
    </div>
</template>

<script>
export default {
    name: 'AdRequestCard',
    props: {
        ad: {
            type: Object,
            required: true
        }
    }
}
</script>

<style>
.ad-request-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 1rem;
}
</style>

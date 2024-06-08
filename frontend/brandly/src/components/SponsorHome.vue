<template>
    <div>
        <h2 class="mx-4 display-6 fw-bold">Your Campaigns</h2>
        <div class="campaigns-container">
            <CampaignCard v-for="campaign in campaigns" :key="campaign.id" :campaign="campaign" />
        </div>
    </div>
</template>

<script>
import CampaignCard from './CampaignCard.vue';

export default {
    components: {
        CampaignCard
    },
    data() {
        return {
            campaigns: [
                {
                    "id": 1,
                    "name": "Samsung S23 Launch",
                    "description": "Promoting the new Samsung S23 smartphone.",
                    "start_date": "2023-07-01",
                    "end_date": "2023-07-31",
                    "budget": 10000,
                    "isActive": true,
                    "isPrivate": true,
                    "progress": 40,
                    "ad_requests": [
                        {
                            "ad_id": 103,
                            "goal": "Showcase new features of Samsung S23",
                            "platform": "YouTube",
                            "target_audience": "Tech enthusiasts",
                            "budget": 6000,
                            "status": "active"
                        },
                        {
                            "ad_id": 104,
                            "goal": "Generate pre-orders for Samsung S23",
                            "platform": "Instagram",
                            "target_audience": "18-35 years",
                            "budget": 4000,
                            "status": "pending"
                        }
                    ]
                },
            ]
        };
    }
}
</script>

<style>
.campaigns-container {
    display: flex;
    overflow-x: auto;
    padding: 1rem;
}

.campaigns-container::-webkit-scrollbar {
    height: 6px;
}

.campaigns-container::-webkit-scrollbar-track {
    border-radius: 25px;
    background-color: #d8d8d8;
}

.campaigns-container::-webkit-scrollbar-thumb {
    background-color: #c4c4c4;
    border-radius: 10px;
}

.campaigns-container::-webkit-scrollbar-thumb:hover {
    background-color: #b6b6b6;
}
</style>

<template>
    <div class="card campaign-card" style="cursor: pointer" @click="openCampaign">
        <div class="card-body">
            <h5 class="card-title">{{ campaign.name }}</h5>
            <p class="card-text"><strong>Description:</strong> {{ campaign.description }}</p>
            <div class="card-details">
                <p class="card-text"><strong>Duration:</strong> {{ formatDuration(campaign.start_date,
                    campaign.end_date) }}</p>
                <div class="status-visibility">
                    <p class="card-text"><strong>Status:</strong> {{ campaign.isActive ? 'Active' : 'Inactive' }}</p>
                    <p class="card-text"><strong>Budget:</strong> {{ campaign.budget }}
                    </p>
                </div>
                <div class="progress" style="height: 8px; position: relative;">
                    <div class="rounded-9 progress-bar-striped bg-success" role="progressbar"
                        :style="{ width: campaign.progress + '%'}" :aria-valuenow="campaign.progress" aria-valuemin="0"
                        aria-valuemax="100">
                        <span class="progress-text">{{ campaign.progress }}%</span>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import { Ripple, initMDB } from "mdb-ui-kit";

export default {
    name: 'CampaignCard',
    props: {
        campaign: {
            type: Object,
            required: true
        }
    },
    mounted() {
        initMDB({ Ripple });
    },
    methods: {
        formatDuration(startDate, endDate) {
            const start = new Date(startDate);
            const end = new Date(endDate);
            const startFormatted = `${start.getDate()} ${start.toLocaleString('default', { month: 'short' })}`;
            const endFormatted = `${end.getDate()} ${end.toLocaleString('default', { month: 'short' })}`;
            return `${startFormatted} - ${endFormatted}`;
        },
        openCampaign() {
            this.$emit('open-campaign', this.campaign.id, this.campaign.name);
        }
    }
}
</script>

<style scoped>
.campaign-card {
    margin: 0.5rem;
    padding: 0.5rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    transition: transform 0.3s ease-in-out;
    min-width: 350px;
}

.campaign-card:hover {
    transform: scale(1.05);
}

.campaign-card .card-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.campaign-card .card-text {
    font-size: 1rem;
    margin-bottom: 0.25rem;
}

.card-details {
    display: flex;
    flex-direction: column;
}

.card-details .card-text {
    margin-bottom: 0.5rem;
}

.status-visibility {
    display: flex;
    justify-content: space-between;
}

.status-visibility .card-text {
    margin-right: 1rem;
}

.campaign-card .btn {
    margin-top: 1rem;
    font-size: 1rem;
}

.progress-text {
    font-weight: 600;
    position: absolute;
    left: 5px;
    top: 50%;
    transform: translateY(-50%);
    color: #1a1a1a;
    font-size: 0.8em;
}
</style>

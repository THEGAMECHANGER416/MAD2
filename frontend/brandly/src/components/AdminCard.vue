<template>
    <div class="card campaign-card">
        <div class="card-body">
            <h5 class="card-title">{{ localCampaign.name }}</h5>
            <p class="card-text"><strong>Description:</strong> {{ localCampaign.description }}</p>
            <div class="card-details">
                <p class="card-text"><strong>Duration:</strong> {{ formatDuration(localCampaign.start_date, localCampaign.end_date) }}</p>
                <div class="status-visibility mb-1">
                    <div class="form-inline d-flex flex-row">
                        <p class="card-text me-1 mb-1"><strong>Status:</strong></p>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" v-model="localCampaign.isActive" @change="updateCampaign">
                            <label class="form-check-label" :class="{'text-success': localCampaign.isActive, 'text-danger': !localCampaign.isActive}">
                                {{ localCampaign.isActive ? 'Active' : 'Inactive' }}
                            </label>
                        </div>
                    </div>
                    <p class="card-text"><strong>Budget:</strong> {{ localCampaign.budget }}</p>
                </div>
                <div class="progress" style="height: 8px; position: relative;">
                    <div class="rounded-9 progress-bar-striped bg-success" role="progressbar"
                        :style="{ width: localCampaign.progress + '%'}" :aria-valuenow="localCampaign.progress" aria-valuemin="0"
                        aria-valuemax="100">
                        <span class="progress-text">{{ localCampaign.progress }}%</span>
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
    data() {
        return {
            localCampaign: { ...this.campaign }
        };
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
        updateCampaign() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register');
                return;
            }

            const startDate = new Date(this.localCampaign.start_date);
            const endDate = new Date(this.localCampaign.end_date);
            const formattedStartDate = `${startDate.getFullYear()}-${startDate.getMonth() + 1}-${startDate.getDate()}`;
            const formattedEndDate = `${endDate.getFullYear()}-${endDate.getMonth() + 1}-${endDate.getDate()}`;

            const body = JSON.stringify({
                name: this.localCampaign.name,
                description: this.localCampaign.description,
                start_date: formattedStartDate,
                end_date: formattedEndDate,
                budget: this.localCampaign.budget,
                progress: this.localCampaign.progress,
                isActive: this.localCampaign.isActive
            });

            const myHeaders = new Headers();
            myHeaders.append("Authorization", `Bearer ${accessToken}`);
            myHeaders.append("Content-Type", "application/json");

            const requestOptions = {
                method: "PUT",
                headers: myHeaders,
                redirect: "follow",
                body: body,
            };

            fetch(`http://127.0.0.1:8000/api/campaigns/${this.localCampaign.id}`, requestOptions)
                .then(response => response.text())
                .then(result => console.log(result))
                .catch(error => console.error(error));
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
    align-items: center; /* Center align the toggle button */
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

<template>
    <div>
        <div class="header-container">
            <h2 class="mx-4 display-6 fw-bold">Your Campaigns</h2>
            <button type="button" class="btn btn-primary" @click="showModal">
                Create Campaign
            </button>
        </div>
        <div class="campaigns-container">
            <CampaignCard v-for="campaign in campaigns" :key=campaign.id :campaign="campaign"
                @open-campaign="openCampaign" />
        </div>

        <div class="header-container">
            <h2 class="mx-4 display-6 fw-bold">Your Ad Requests</h2>
        </div>
        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true"
            ref="exampleModal">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Add New Campaign</h5>
                        <button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="saveCampaign">
                            <div class="mb-3">
                                <label for="name" class="form-label">Name</label>
                                <input v-model="campaign.name" type="text" class="form-control" id="name" required />
                            </div>
                            <div class="mb-3">
                                <label for="description" class="form-label">Description</label>
                                <textarea v-model="campaign.description" class="form-control" id="description"
                                    required></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="start_date" class="form-label">Start Date</label>
                                <input v-model="campaign.start_date" type="date" class="form-control" id="start_date"
                                    required />
                            </div>
                            <div class="mb-3">
                                <label for="end_date" class="form-label">End Date</label>
                                <input v-model="campaign.end_date" type="date" class="form-control" id="end_date"
                                    required />
                            </div>
                            <div class="mb-3">
                                <label for="budget" class="form-label">Budget</label>
                                <input v-model="campaign.budget" type="number" class="form-control" id="budget"
                                    required />
                            </div>
                            <button type="submit" class="btn btn-primary">Save</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CampaignCard from './CampaignCard.vue';
import { Modal, initMDB } from "mdb-ui-kit";

export default {
    components: {
        CampaignCard
    },
    data() {
        return {
            campaigns: [],
            campaign: {
                "name": '',
                "description": '',
                "start_date": '',
                "end_date": '',
                "budget": 0,
                "isActive": false,
                "progress": 0
            },
            modalInstance: null // Add this line
        };
    },
    mounted() {
        this.initMDBSetup();
        this.fetchCampaigns();
    },
    methods: {
        initMDBSetup() {
            initMDB({ Modal });
            this.modalInstance = new Modal(this.$refs.exampleModal, {});
        },
        showModal() {
            if (!this.modalInstance) {
                this.modalInstance = new Modal(this.$refs.exampleModal, {});
            }
            this.modalInstance.show();
        },
        hideModal() {
            if (this.modalInstance) {
                this.modalInstance.hide();
            }
        },
        fetchCampaigns() {
            const url = "http://127.0.0.1:8000/api/campaigns"; // Replace with your actual API endpoint

            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                console.error('Access token not found.');
                // Handle scenario where token is missing (e.g., redirect to login)
                return;
            }

            const requestOptions = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                    'Content-Type': 'application/json'
                }
            };

            fetch(url, requestOptions)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    this.campaigns = data; // Update campaigns data property with fetched data
                    console.log('Campaigns fetched successfully:', data);
                })
                .catch(error => {
                    console.error('Error fetching campaigns:', error);
                    // Handle error scenarios (e.g., show error message to user)
                });
        },
        saveCampaign() {
            console.log('Saving campaign:', this.campaign);
            try {
                const accessToken = localStorage.getItem('accessToken');
                if (!accessToken) {
                    this.$router.push('/register');
                    return;
                }

                const myHeaders = new Headers();
                myHeaders.append("Authorization", `Bearer ${accessToken}`);
                myHeaders.append("Content-Type", "application/json");

                const requestOptions = {
                    method: "POST",
                    headers: myHeaders,
                    body: JSON.stringify(this.campaign),
                    redirect: "follow"
                };

                fetch("http://127.0.0.1:8000/api/campaigns", requestOptions)
                    .then((response) => {
                        if (!response.ok) {
                            return response.json().then((data) => {
                                throw new Error(data.msg || 'Network response was not ok');
                            });
                        }
                        return response.json();
                    })
                    .then((data) => {
                        console.log('Campaign created successfully', data);
                        // Optionally, update campaigns list or perform other actions after successful creation
                        this.campaigns.push(data);
                        // Hide modal after successful creation
                        this.hideModal();
                        // Reset form fields after hiding the modal
                        this.campaign = { name: '', description: '', start_date: '', end_date: '', budget: 0 };
                    })
                    .catch((error) => {
                        console.error('Error creating campaign:', error.message);
                        // Handle error scenarios (e.g., show error message to user)
                    });
            } catch (error) {
                console.error('Error submitting form:', error.message);
                // Handle error scenarios (e.g., show error message to user)
            }
        },
        openCampaign(campaignId, campaignName) {
            this.$router.push({ name: 'CampaignDetail', params: { id: campaignId, name: campaignName } });
        }
    }
};
</script>

<style>
.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 1rem;
}

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

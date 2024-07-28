<template>
    <div>
        <div class="header-container">
            <h2 class="mx-4 display-6 fw-bold">Top Campaigns</h2>
        </div>
        <div v-if="campaigns.length > 0" class="campaigns-container">
            <CampaignCard v-for="campaign in campaigns" :key=campaign.id :campaign="campaign"
                @open-campaign="openCampaign" />
        </div>

        <div v-else class="campaigns-container ms-4">
            <h5 class="text-warning">Sorry but there are no active campaigns!</h5>
        </div>

        <div class="header-container">
            <h2 class="mx-4 display-6 fw-bold">Your Ad Requests</h2>
        </div>

        <div v-if="adRequests.length > 0" class="ad-requests-container">
            <AdsCard v-for="adRequest in adRequests" :key=adRequest.id :ad="adRequest"/>
        </div>

        <div v-else class="ad-requests-container ms-4">
            <h5 class="text-success">No Updates as of now. Have a great day!</h5>
        </div>  
    </div>
</template>

<script>
import AdsCard from './AdsCard.vue';
import CampaignCard from './CampaignCard.vue';

export default {
    components: {
        CampaignCard,
        AdsCard
    },
    data() {
        return {
            campaigns: [],
            adRequests: [],
        };
    },
    mounted() {
        this.fetchCampaigns();
        this.fetchAdRequests();
    },
    methods: {
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
        },
        fetchAdRequests() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register');
                return;
            }

            const myHeaders = new Headers();
            myHeaders.append("Authorization", `Bearer ${accessToken}`);
            myHeaders.append("Content-Type", "application/json");

            const requestOptions = {
                method: "GET",
                headers: myHeaders,
                redirect: "follow"
            };
            fetch("http://127.0.0.1:8000/api/ad_requests", requestOptions)
                .then(response => response.json())
                .then(data => {
                    this.adRequests = data;
                    console.log('Ad requests fetched successfully:', data);
                    if (!this.adRequests) {
                        this.adRequests = [];
                    }
                    else {
                        this.adRequests = this.adRequests.filter(request => request.status == 2);
                    }      
                })
                .catch(error => {
                    console.error('Error fetching ad requests:', error);
                });
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
.ad-requests-container {
    display: flex;
    overflow-x: auto;
    padding: 1rem;
}

.ad-requests-container::-webkit-scrollbar {
    height: 6px;
}

.ad-requests-container::-webkit-scrollbar-track {
    border-radius: 25px;
    background-color: #d8d8d8;
}

.ad-requests-container::-webkit-scrollbar-thumb {
    background-color: #c4c4c4;
    border-radius: 10px;
}

.ad-requests-container::-webkit-scrollbar-thumb:hover {
    background-color: #b6b6b6;
}
</style>

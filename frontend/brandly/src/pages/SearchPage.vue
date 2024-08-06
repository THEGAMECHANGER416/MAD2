<template>
    <div class="container-fluid mb-0 d-flex flex-column align-items-center wrapper-class"
        style="background: linear-gradient(15deg, #5c180f, #7e1a12, #a31a1b, #c51e22) !important;">
        <div class="mt-5">
            <div v-if="user">
                <div v-if="role === 'Influencer'">
                    <h1 class="mb-0 display-6 fw-bold text-white">Search for Ad Campaigns</h1>
                </div>
                <div v-else-if="role === 'Sponsor'">
                    <h1 class="mb-0 display-6 fw-bold text-white">Search for Influencers</h1>
                </div>
                <div v-else-if="role === 'Admin'">
                    <h1 class="mb-0 display-6 fw-bold text-white">Search for Ad Campaigns</h1>
                </div>
                <div class="card mt-3 w-100"
                    style="border-radius: 10em; background: transparent; border: 2px solid white;">
                    <div class="card-body p-2">
                        <div class="input-group input-group-lg">
                            <input type="text" class="form-control form-control-lg round bg-transparent text-white"
                                placeholder="Type Keywords" aria-label="Type Keywords" aria-describedby="basic-addon2"
                                v-model="query" style="color: white;" @keyup.enter="search" />
                            <button class="input-group-text border-0" id="basic-addon2" type="submit" @click="search">
                                <i class="fas fa-search fa-lg text-white"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="mt-3 campaigns-container" v-if="role === 'Influencer' && results.length > 0">
                    <CampaignCard v-for="campaign in results" :key="campaign.id" :campaign="campaign"
                        @open-campaign="openCampaign" />
                </div>
                <div class="mt-3 influencers-container" v-else-if="role === 'Sponsor' && results.length > 0">
                    <InfluencerCard v-for="influencer in results" :key="influencer.id" :influencer="influencer"
                        @sendRequest="sendRequest" />
                </div>
                <div class="mt-3 admins-container" v-else-if="role === 'Admin' && results.length > 0">
                    <AdminCard v-for="campaign in results" :key="campaign.id" :campaign="campaign"
                        @open-campaign="openCampaign" />
                </div>
                <div class="mt-3" v-else-if="results.length === 0">
                    <p class="text-white">No results found</p>
                </div>
            </div>
        </div>

        <CustomModal v-if="role === 'Sponsor'" :show.sync="sendRequestModalVisible">
            <template v-slot:header>
                <h5>Send Request</h5>
            </template>
            <template v-slot:body>
                <div class="container">
                    <!-- Dropdown to choose campaign -->
                    <div class="mb-3">
                        <label for="campaignDropdown" class="form-label">Select Campaign</label>
                        <select id="campaignDropdown" v-model="selectedCampaignId" @change="fetchAdRequests"
                            class="form-select" required>
                            <option value="" disabled>Select a campaign</option>
                            <option v-for="campaign in sponsorCampaigns" :key="campaign.id" :value="campaign.id">
                                {{ campaign.name }}
                            </option>
                        </select>
                    </div>

                    <!-- Dropdown to choose ad request -->
                    <div class="mb-3" v-if="selectedCampaignId">
                        <label for="adRequestDropdown" class="form-label">Select Ad Request</label>
                        <select id="adRequestDropdown" v-model="selectedAdRequestId" class="form-select" required>
                            <option value="" disabled>Select an ad request</option>
                            <option v-for="adRequest in adRequests" :key="adRequest.id" :value="adRequest.id">
                                {{ adRequest.goal }}
                            </option>
                        </select>
                    </div>

                    <div class="mt-4">
                        <button type="button" class="btn btn-secondary" @click="hideSendRequestModal">Cancel</button>
                        <button type="button" class="btn btn-primary" @click="submitRequest">Submit</button>
                    </div>
                </div>
            </template>
        </CustomModal>
    </div>
</template>

<script>
import CampaignCard from '@/components/CampaignCard.vue';
import CustomModal from '@/components/CustomModal.vue';
import InfluencerCard from '@/components/InfluencerCard.vue';
import AdminCard from '@/components/AdminCard.vue';

export default {
    name: 'SearchPage',
    components: {
        CampaignCard,
        InfluencerCard,
        CustomModal,
        AdminCard
    },
    computed: {
        user() {
            return this.$store.state.user;
        },
        role() {
            return this.$store.state.role;
        },
        adRequest() {
            return this.adRequests.find(request => request.id == this.selectedAdRequestId);
        }
    },
    data() {
        return {
            query: '',
            results: [],
            sendRequestModalVisible: false,
            selectedCampaignId: '',
            selectedAdRequestId: '',
            adRequests: [],
            sponsorCampaigns: [],
            selectedInfluencerId: ''  // Added to store the selected influencer's ID
        };
    },
    created() {
        this.fetchUserDetails();
    },
    methods: {
        fetchUserDetails() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register');
                return;
            }

            fetch("http://127.0.0.1:8000/api/profile", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${accessToken}`
                },
            })
            .then(response => response.json())
            .then(data => {
                this.$store.dispatch("updateUser", data);
                if (this.role === 'Sponsor') {
                    this.fetchSponsorCampaigns();
                }
            })
            .catch(error => {
                console.error(error);
                this.$store.dispatch('logout');
            });
        },
        search() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register');
                return;
            }

            fetch(`http://127.0.0.1:8000/api/search?q=${this.query}`, {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
            })
            .then(response => response.json())
            .then(data => this.results = data)
            .catch(error => console.error(error));
        },
        openCampaign(campaignId, campaignName) {
            this.$router.push({ name: 'CampaignDetail', params: { id: campaignId, name: campaignName } });
        },
        sendRequest(influencer) {
            this.sendRequestModalVisible = true;
            this.selectedInfluencerId = influencer.id;  // Store the selected influencer's ID
        },
        hideSendRequestModal() {
            this.sendRequestModalVisible = false;
            this.selectedCampaignId = '';
            this.selectedAdRequestId = '';
            this.adRequests = [];
            this.selectedInfluencerId = '';  // Clear the selected influencer's ID
        },
        submitRequest() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register');
                return;
            }

            fetch(`http://127.0.0.1:8000/api/ad_requests/${this.selectedAdRequestId}`, {
                method: 'PUT',
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    campaign_id: this.selectedCampaignId,
                    influencer_id: this.selectedInfluencerId,  // Use the selected influencer's ID
                    ad_request_id: this.selectedAdRequestId,
                    requirements: this.adRequest.requirements,
                    payment_amount: this.adRequest.payment_amount,
                    status: '2',
                    goal: this.adRequest.goal,
                    platform: this.adRequest.platform
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.hideSendRequestModal();
            })
            .catch(error => console.error(error));
        },
        fetchSponsorCampaigns() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register');
                return;
            }

            fetch('http://127.0.0.1:8000/api/campaigns', {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
            })
            .then(response => response.json())
            .then(data => this.sponsorCampaigns = data)
            .catch(error => console.error(error));
        },
        fetchAdRequests() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register');
                return;
            }

            fetch(`http://127.0.0.1:8000/api/campaigns/${this.selectedCampaignId}`, {
                method: 'GET',
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
            })
            .then(response => response.json())
            .then(data => {
                this.adRequests = data.ads;
            })
            .catch(error => console.error(error));
        }
    }
}
</script>

<style scoped>
.wrapper-class {
    margin-top: 3.6em;
    /* Adjust height to allow scrolling on the entire page */
    min-height: calc(100vh - 3.6em);
    overflow-y: auto;
}

.form-control {
    border-color: transparent;
}

.input-group>.form-control:focus {
    border-color: transparent;
    box-shadow: inset 0 0 0 1px transparent;
}

.form-control::placeholder {
    color: white;
    opacity: 1;
    /* Ensure placeholder is fully visible */
}

.campaigns-container,
.influencers-container,
.admins-container {
    display: flex;
    flex-wrap: wrap;
    /* Remove specific height and overflow properties */
    margin-bottom: 1rem;
}
</style>

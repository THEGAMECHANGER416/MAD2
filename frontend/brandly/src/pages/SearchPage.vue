<template>
    <div class="container-fluid mb-0 d-flex wrapper-class flex-column align-items-center"
        style="background: linear-gradient(15deg, #5c180f, #7e1a12, #a31a1b, #c51e22)  !important;">
        <div class="mt-5">
            <div v-if="user">
                <div v-if="role === 'Influencer'">
                    <h1 class="mb-0 display-6 fw-bold text-white">Search for Ad Campaigns</h1>
                </div>
                <div v-else-if="role === 'Sponsor'">
                    <h1 class="mb-0 display-6 fw-bold text-white">Search for Influencers</h1>
                </div>
                <div class="card mt-3 w-100"
                    style="border-radius: 10em; background: transparent; border: 2px solid white;">
                    <div class="card-body p-2">
                        <div class="input-group input-group-lg">
                            <input type="text" class="form-control form-control-lg round bg-transparent text-white"
                                placeholder="Type Keywords" aria-label="Type Keywords" aria-describedby="basic-addon2"
                                v-model="query" style="color: white;" @keyup.enter="search"/>
                            <button class="input-group-text border-0" id="basic-addon2" type="submit" @click="search">
                                <i class="fas fa-search fa-lg text-white"></i>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="mt-3 campaigns-container" v-if="role == 'Influencer' && results.length > 0">
                    <CampaignCard v-for="campaign in results" :key=campaign.id :campaign="campaign" @open-campaign="openCampaign" />
                </div>
                <div class="mt-3 influencers-container" v-else-if="role == 'Sponsor' && results.length > 0">
                    <InfluencerCard v-for="influencer in results" :key=influencer.id :influencer="influencer" @open-influencer="openInfluencer"/>
                </div>
                <div class="mt-3" v-else-if="results.length == 0">
                    <p class="text-white">No results found</p>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import CampaignCard from '@/components/CampaignCard.vue';
import InfluencerCard from '@/components/InfluencerCard.vue';

export default {
    name: 'SearchPage',
    components: {
        CampaignCard,
        InfluencerCard
    },
    computed: {
        user() {
            return this.$store.state.user;
        },
        role() {
            return this.$store.state.role;
        }
    },
    data() {
        return {
            query: '',
            results: [],
        };
    },
    created() {
        this.fetchUserDetails();
    },
    methods: {
        fetchUserDetails() {
            try {
                const accessToken = localStorage.getItem('accessToken');
                if (!accessToken) {
                    this.$router.push('/register')
                }

                const myHeaders = new Headers();
                myHeaders.append("Authorization", `Bearer ${accessToken}`);

                const requestOptions = {
                    method: "GET",
                    headers: myHeaders,
                    redirect: "follow"
                };

                fetch("http://127.0.0.1:8000/api/profile", requestOptions)
                    .then((response) => {
                        if (!response.ok) {
                            throw new Error("Network response was not ok");
                        }
                        return response.json();
                    })
                    .then((data) => {
                        const userData = data;
                        this.$store.dispatch("updateUser", userData);
                    })
                    .catch((error) => {
                        console.error(error);
                        this.$store.dispatch('logout');
                    });
            } catch (error) {
                console.error('Error fetching user details:', error.message);
                this.$store.dispatch('logout');
            }
        },
        search() {
            const accessToken = localStorage.getItem('accessToken');
            if (!accessToken) {
                this.$router.push('/register')
            }

            const myHeaders = new Headers();
            myHeaders.append("Authorization", `Bearer ${accessToken}`);
            myHeaders.append("Content-Type", "application/json");
            
            fetch(`http://127.0.0.1:8000/api/search?q=${this.query}`, {
                method: 'GET',
                headers: myHeaders,
                redirect: 'follow',
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                this.results = data;
                console.log(this.results);
            })
            .catch(error => console.error(error));
        },
        openCampaign(campaignId, campaignName) {
            this.$router.push({ name: 'CampaignDetail', params: { id: campaignId, name: campaignName } });
        }
    }
}
</script>
<style scoped>
.wrapper-class {
    margin-top: 3.6em;
    height: calc(100vh - 3.6em);
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

.campaigns-container {
    display: flex;
    flex-wrap: wrap;
    overflow-y: auto;
    height: 100%;
}

.influencers-container {
    display: flex;
    flex-wrap: wrap;
    overflow-y: auto;
    height: 100%;
}
</style>
<template>
    <div class="mb-0 container-fluid d-flex flex-column align-items-center wrapper-class">
        <div v-if="user">
            <div v-if="role === 'Influencer'">
                <h1 class="mb-0 display-6 fw-bold">Search for Ad Campaigns</h1>
            </div>
            <div v-else-if="role === 'Sponsor'">
                <h1 class="mb-0 display-6 fw-bold">Search for Influencers</h1>
            </div>
            <div class="card m-2 w-75" style="border-radius: 10em; background: linear-gradient(to right, #7E1A12, #D12B2B);">
    <div class="card-body p-2">
        <div class="input-group input-group-lg">
            <input type="text" class="form-control form-control-lg round bg-transparent text-white"
                placeholder="Type Keywords" aria-label="Type Keywords" aria-describedby="basic-addon2"
                style="color: white;"/>
            <span class="input-group-text border-0" id="basic-addon2"><i
                    class="fas fa-search fa-lg text-white"></i></span>
        </div>
    </div>
</div>

        </div>
    </div>
</template>
<script>
export default {
    name: 'SearchPage',
    computed: {
        user() {
            return this.$store.state.user;
        },
        role() {
            return this.$store.state.role;
        }
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
        }
    }
}
</script>
<style scoped>
.wrapper-class {
    margin-top: 5em
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
    opacity: 1; /* Ensure placeholder is fully visible */
}
</style>
<template>
    <div class="ad-request-card">
        <div class="card-body d-flex align-items-center flex-column">
            <!-- Platform Icon -->

            <div class="d-flex flex-column w-100 justify-content-between">
                <h3 class="card-title mb-3">{{ ad.goal }}</h3>
                <div class="d-flex justify-content-between mb-1">
                    <span class="d-flex align-items-center flex-row">
                        <p class="card-text mb-0 me-2"><strong>Platform:</strong> {{ ad.platform }}</p>
                        <i :class="getPlatformIcon(ad.platform)" :style="{ color: getPlatformColor(ad.platform) }"
                            class="platform-icon mr-3"></i>
                    </span>
                    <p class="card-text mb-0"><strong>Amount:</strong> ${{ ad.payment_amount }}</p>
                </div>
                <div class="d-flex justify-content-between align-items-center">
                    <p class="card-text mb-1"><strong>Status:</strong> {{ ad.status }}</p>
                    <p class="card-text mb-1"><strong>Influencer:</strong> {{ ad.influencer_name || 'N/A' }}</p>
                </div>
                <p class="card-text mb-1"><strong>Requirements:</strong> {{ ad.requirements }}</p>
            </div>

            <!-- Action Buttons -->
            <div class="d-flex flex-row mt-3">
                <button @click="showEditModal" class="btn btn-sm btn-primary mr-2"><i class="fas fa-edit"></i>
                    Update</button>
                <!-- If status is 0, show delete button -->
                    <button v-if="ad.status === '0'" @click="showDeleteModal" class="btn btn-sm btn-danger"><i class="fas fa-trash-alt"></i>
                        Delete</button>
            </div>
        </div>
        <CustomModal :show.sync="showModal">
            <h3 slot="header">Update Ad</h3>
            <div slot="body">
                <form @submit.prevent="editAd">
                    <div class="mb-3">
                        <label for="payment_amount" class="form-label">Payment Amount</label>
                        <div class="input-group w-75">
                            <div class="input-group-text">₹</div>
                            <input v-model="adRequest.payment_amount" type="number"
                                placeholder="Enter your payment amount here" class="form-control" id="payment_amount"
                                required />
                        </div>
                    </div>
                    <div class="mb-3">
                        <label for="requirements" class="form-label">Requirements</label>
                        <textarea v-model="adRequest.requirements" placeholder="Enter your requirements here"
                            class="form-control" id="requirements" required></textarea>
                    </div>
                    <div class="row">
                        <div class="col-12 text-center mt-1">
                            <input class="btn btn-warning btn-lg" type="submit" value="Submit" />
                        </div>
                    </div>
                </form>
            </div>
        </CustomModal>
        <CustomModal :show.sync="deleteModalVisible">
            <template v-slot:header>
                <h5>Delete Ad</h5>
            </template>
            <template v-slot:body>
                <h6>Are you sure you want to delete this Ad?</h6>
                <p>This action can not be undone</p>
                <button type="button" class="btn btn-secondary" @click="hideDeleteModal">Cancel</button>
                <button type="button" class="btn btn-danger" @click="deleteAd">Delete</button>
            </template>
        </CustomModal>
    </div>
</template>

<script>
import CustomModal from './CustomModal.vue';

export default {
    name: 'AdRequestCard',
    props: {
        ad: {
            type: Object,
            required: true
        }
    },
    components: {
        CustomModal
    },
    methods: {
        getPlatformIcon(platform) {
            const brand = this.brands.find(b => b.value.toLowerCase() === platform.toLowerCase());
            return brand ? brand.icon : 'fas fa-globe'; // Default icon (globe icon) if not found
        },
        getPlatformColor(platform) {
            const brand = this.brands.find(b => b.value.toLowerCase() === platform.toLowerCase());
            return brand ? brand.color : '#333'; // Default color if not found
        },
        editAd(ad) {
            // Implement edit functionality
            console.log('Editing ad:', ad);
        },
        deleteAd(ad) {
            // Implement delete functionality
            console.log('Deleting ad:', ad);
        },
        showEditModal() {
            this.showModal = true;
        },
        hideEditModal() {
            this.showModal = false;
        },
        showDeleteModal() {
            this.deleteModalVisible = true;
        },
        hideDeleteModal() {
            this.deleteModalVisible = false;
        }
    },
    data() {
        return {
            brands: [
                { value: 'Facebook', color: '#3b5998', icon: 'fab fa-facebook-f' },
                { value: 'Twitter', color: '#55acee', icon: 'fab fa-twitter' },
                { value: 'Instagram', color: '#ac2bac', icon: 'fab fa-instagram' },
                { value: 'Tiktok', color: '#000000', icon: 'fab fa-tiktok' },
                { value: 'Linkedin', color: '#0082ca', icon: 'fab fa-linkedin-in' },
                { value: 'Youtube', color: '#ed302f', icon: 'fab fa-youtube' },
                { value: 'Reddit', color: '#ff4500', icon: 'fab fa-reddit-alien' },
                { value: 'Whatsapp', color: '#25d366', icon: 'fab fa-whatsapp' }
            ],
            showModal: false,
            deleteModalVisible: false,
            adRequest: this.ad
        };
    }
}
</script>

<style scoped>
.ad-request-card {
    border-radius: 15px;
    padding: 1.5rem;
    width: 30%;
    margin: 1rem;
    box-shadow: none;
    background: white;
}

.platform-icon {
    font-size: 1.7rem;
    /* Adjust size as needed */
}

.btn {
    padding: 0.35rem 0.7rem;
}
</style>

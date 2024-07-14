<template>
  <div>
    <div class="mb-0 container-fluid wrapper-class">
      <span @click="goBack" class="back-button ms-3">
        <i class="fas fa-arrow-left"></i> Back
      </span>
      <div class="header-container mb-0 mx-2">
        <div class="row mb-0">
          <h2 class="mx-4 display-6 fw-bold" style="display: inline-block;">{{ campaign.name }}</h2>
          <p class="mx-4 display-9" style="display: inline-block;">({{ campaign.description }})</p>
        </div>
        <div class="button-group ms-auto">
          <button @click="showEditModal" class="btn btn-primary" style="display: inline-block;">
            <i class="fa fa-pencil"></i>
          </button>
          <button @click="showDeleteModal" class="btn btn-danger" style="display: inline-block;">
            <i class="fa fa-trash"></i>
          </button>
          <button @click="createAdRequest" class="btn btn-success" style="display: inline-block;">
            <i class="fa fa-plus"></i>
          </button>
        </div>
      </div>
    </div>
    <!-- Arrange ads in nx2 grid -->
    <div class="container-fluid">
      <div class="row justify-content-center gx-2">
        <AdRequestCard class="col-md-4" v-for="ad in campaign.ads" :key="ad.id" :ad="ad" deleted="deleted"/>
      </div>
    </div> 
    
    <CustomModal :show.sync="editModalVisible">
      <template v-slot:header>
        <h4>Edit Campaign</h4>
      </template>
      <template v-slot:body>
        <form @submit.prevent="updateCampaign">
          <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input v-model="campaign.name" type="text" class="form-control" id="name" required />
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Description</label>
            <textarea v-model="modalCampaign.description" class="form-control" id="description" required></textarea>
          </div>
          <div class="mb-3">
            <label for="start_date" class="form-label">Start Date</label>
            <input v-model="modalCampaign.start_date" type="date" class="form-control" id="start_date" required />
          </div>
          <div class="mb-3">
            <label for="end_date" class="form-label">End Date</label>
            <input v-model="modalCampaign.end_date" type="date" class="form-control" id="end_date" required />
          </div>
          <div class="mb-3">
            <label for="budget" class="form-label">Budget</label>
            <input v-model="modalCampaign.budget" type="number" class="form-control" id="budget" required />
          </div>
          <button type="submit" class="btn btn-primary">Save</button>
          <button type="button" class="btn btn-secondary" @click="hideEditModal">Cancel</button>
        </form>
      </template>
    </CustomModal>

    <CustomModal :show.sync="deleteModalVisible">
      <template v-slot:header>
        <h5>Delete Campaign</h5>
      </template>
      <template v-slot:body>
        <h6>Are you sure you want to delete this campaign?</h6>
        <p>This will also delete all the ad requests associated with this campaign</p>
        <button type="button" class="btn btn-secondary" @click="hideDeleteModal">Cancel</button>
        <button type="button" class="btn btn-danger" @click="deleteCampaign">Delete</button>
      </template>
    </CustomModal>

    <CustomModal :show.sync="createAdModalVisible">
      <template v-slot:header>
        <h5>Create Ad</h5>
      </template>
      <template v-slot:body>
        <form @submit.prevent="postAdRequest">
          <!-- Goal -->
          <div class="mb-3">
            <label for="goal" class="form-label">Goal</label>
            <input v-model="newAdRequest.goal" type="text" placeholder="Enter your goal here" class="form-control"
              id="goal" required />
          </div>
          <!-- Platfom -->
          <div class="mb-3">
            <label for="platform" class="form-label">Platform</label>
            <div class="row">
              <div class="col-12">
                <div v-for="brand in brands" :key="brand.value" class="brand-button-container">
                  <input type="radio" :id="brand.value" :value="brand.value" v-model="newAdRequest.platform"
                    class="brand-radio" />
                  <label :for="brand.value" class="btn text-white btn-floating"
                    :style="{ backgroundColor: brand.color }">
                    <i :class="brand.icon"></i>
                  </label>
                </div>
                <p class="form-text text-muted">Selected Brand: {{ newAdRequest.platform }}</p>
              </div>
            </div>
          </div>
          <!-- Payment Amount Inline-->
          <div class="mb-3 d-flex align-items-center justify-content-between">
            <label for="payment-amount" class="form-label">Payment Amount</label>
            <div class="input-group w-75">
              <div class="input-group-text">₹</div>
              <input v-model="newAdRequest.payment_amount" type="number" class="form-control" id="payment-amount"
                required />
            </div>
          </div>
          <!-- List of Requirements in Markdown -->
          <div class="mb-3">
            <label for="requirements" class="form-label">Requirements</label>
            <textarea v-model="newAdRequest.requirements" placeholder="Enter your requirements here"
              class="form-control" id="requirements" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Save</button>
          <button type="button" class="btn btn-secondary" @click="hideCreateAdModal">Cancel</button>
        </form>
      </template>
    </CustomModal>
  </div>
</template>


<script>
import AdRequestCard from '../components/AdRequestCard.vue';
import CustomModal from '../components/CustomModal.vue';

export default {
  name: 'CampaignDetail',
  components: {
    AdRequestCard,
    CustomModal
  },
  props: {
    id: {
      type: Number,
      required: true
    },
  },
  data() {
    return {
      campaign: {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: 0,
        isActive: false,
        progress: 0,
        ads: []
      },
      modalCampaign: {
        name: '',
        description: '',
        start_date: '',
        end_date: '',
        budget: 0,
        isActive: false,
        progress: 0
      },
      newAdRequest: {
        platform: 'Facebook',
        goal: '',
        payment_amount: 0,
        requirements: ''
      },
      brands: [
        { value: 'Facebook', color: '#3b5998', icon: 'fab fa-xl fa-facebook-f' },
        { value: 'Twitter', color: '#55acee', icon: 'fab fa-xl fa-twitter' },
        { value: 'Instagram', color: '#ac2bac', icon: 'fab fa-xl fa-instagram' },
        { value: 'Tiktok', color: '#000000', icon: 'fab fa-xl fa-tiktok' },
        { value: 'Linkedin', color: '#0082ca', icon: 'fab fa-xl fa-linkedin-in' },
        { value: 'Youtube', color: '#ed302f', icon: 'fab fa-xl fa-youtube' },
        { value: 'Reddit', color: '#ff4500', icon: 'fab fa-xl fa-reddit-alien' },
        { value: 'Whatsapp', color: '#25d366', icon: 'fab fa-xl fa-whatsapp' }
      ],
      editModalVisible: false,
      deleteModalVisible: false,
      createAdModalVisible: false,
      editAdModalVisible: false
    };
  },
  mounted() {
    this.fetchCampaignDetails();
  },
  methods: {
    goBack() {
      this.$router.back();
    },
    createAdRequest() {
      this.showCreateAdModal();
    },
    fetchCampaignDetails() {
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
        redirect: "follow",
      };

      fetch(`http://127.0.0.1:8000/api/campaigns/${this.id}`, requestOptions)
        .then(response => response.json())
        .then(data => {
          this.campaign.name = data.name;
          this.campaign.description = data.description;
          // convert date to yyyy-mm-dd
          const date = new Date(data.start_date);
          const year = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const day = String(date.getDate()).padStart(2, '0');
          this.campaign.start_date = `${year}-${month}-${day}`;

          const endDate = new Date(data.end_date);
          const endYear = endDate.getFullYear();
          const endMonth = String(endDate.getMonth() + 1).padStart(2, '0');
          const endDay = String(endDate.getDate()).padStart(2, '0');
          this.campaign.end_date = `${endYear}-${endMonth}-${endDay}`;
          this.campaign.budget = data.budget;
          this.campaign.isActive = data.isActive;
          this.campaign.progress = data.progress;
          this.campaign.ads = data.ads;
          // filter ads to get status 0 1 and 2
          this.campaign.ads = this.campaign.ads.filter(ad => ad.status == 0 || ad.status == 1 || ad.status == 2);
          this.modalCampaign = { ...this.campaign };
          console.log('Campaign details fetched successfully:', data);
        })
        .catch(error => console.error(error));
    },
    showEditModal() {
      this.editModalVisible = true;
    },
    hideEditModal() {
      this.editModalVisible = false;
    },
    updateCampaign() {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        this.$router.push('/register');
        return;
      }
      const body = JSON.stringify({
        name: this.modalCampaign.name,
        description: this.modalCampaign.description,
        start_date: this.modalCampaign.start_date,
        end_date: this.modalCampaign.end_date,
        budget: this.modalCampaign.budget,
        progress: this.modalCampaign.progress,
        isActive: this.modalCampaign.isActive
      });

      // Send a PUT request to update the campaign
      const myHeaders = new Headers();
      myHeaders.append("Authorization", `Bearer ${accessToken}`);
      myHeaders.append("Content-Type", "application/json");

      const requestOptions = {
        method: "PUT",
        headers: myHeaders,
        redirect: "follow",
        body: body,
      };

      fetch(`http://127.0.0.1:8000/api/campaigns/${this.id}`, requestOptions)
        .then(response => response.text())
        .then(() => {
          this.fetchCampaignDetails();
          this.hideEditModal();
          this.campaign = this.modalCampaign;
        })
        .catch(error => console.error(error));
      this.hideEditModal();
    },
    showDeleteModal() {
      this.deleteModalVisible = true;
    },
    hideDeleteModal() {
      this.deleteModalVisible = false;
    },
    showCreateAdModal() {
      this.createAdModalVisible = true;
    },
    hideCreateAdModal() {
      this.createAdModalVisible = false;
    },
    deleteCampaign() {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        this.$router.push('/register');
        return;
      }

      const myHeaders = new Headers();
      myHeaders.append("Authorization", `Bearer ${accessToken}`);

      const requestOptions = {
        method: "DELETE",
        headers: myHeaders,
        redirect: "follow"
      };

      fetch(`http://127.0.0.1:8000/api/campaigns/${this.id}`, requestOptions)
        .then((response) => response.text())
        .then(() => {
          this.$router.push('/')
        })
        .catch((error) => console.error(error));
      this.hideDeleteModal();
    },
    postAdRequest() {
      const accessToken = localStorage.getItem('accessToken');
      if (!accessToken) {
        this.$router.push('/register');
        return;
      }

      const myHeaders = new Headers();
      myHeaders.append("Authorization", `Bearer ${accessToken}`);
      myHeaders.append("Content-Type", "application/json");

      const body = JSON.stringify({
        campaign_id: this.id,
        goal: this.newAdRequest.goal,
        platform: this.newAdRequest.platform,
        payment_amount: this.newAdRequest.payment_amount,
        requirements: this.newAdRequest.requirements
      });

      const requestOptions = {
        method: "POST",
        headers: myHeaders,
        redirect: "follow",
        body: body
      };

      fetch("http://127.0.0.1:8000/api/ad_requests", requestOptions)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((result) => {
          console.log(result, 'Ad request created successfully');
          this.hideCreateAdModal();
          this.campaign.ads.push(result);
          this.newAdRequest = {
            goal: '',
            platform: 'Facebook',
            payment_amount: 0,
            requirements: ''
          }
        })
        .catch((error) => console.error(error));
    },
    deleted(id) {
      this.campaign.ads = this.campaign.ads.filter(ad => ad.id !== id);
    }
  }
}
</script>

<style scoped>
.wrapper-class {
  margin-top: 5em;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand-button-container {
  display: inline-block;
  margin: 0.5rem;
}

.brand-radio {
  display: none;
}

.brand-radio:checked+label {
  transform: scale(1.2);
  border: 1px solid #00000070;
}
</style>
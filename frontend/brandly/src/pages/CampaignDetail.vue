<template>
    <div>
      <div class="mb-0 container-fluid wrapper-class">
        <div class="header-container mb-0">
          <span @click="goBack" class="back-button ms-3">
            <i class="fas fa-arrow-left"></i> Back
          </span>
          <h2 class="mx-4 display-6 fw-bold" style="display: inline-block;">{{ campaign.name }}</h2>
          <div class="button-group ms-auto">
              <button @click="showEditModal" class="btn btn-primary" style="display: inline-block;">
                <i class="fa fa-pencil"></i>
              </button>
              <button @click="showDeleteModal" class="btn btn-danger" style="display: inline-block;">
                <i class="fa fa-trash"></i>
              </button>
          </div>
        </div>
      </div>
      <div class="ad-requests-container mt-0">
        <AdRequestCard v-for="ad in adRequests" :key="ad.ad_id" :ad="ad" class="mb-3" />
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
              <textarea v-model="campaign.description" class="form-control" id="description" required></textarea>
            </div>
            <div class="mb-3">
              <label for="start_date" class="form-label">Start Date</label>
              <input v-model="campaign.start_date" type="date" class="form-control" id="start_date" required />
            </div>
            <div class="mb-3">
              <label for="end_date" class="form-label">End Date</label>
              <input v-model="campaign.end_date" type="date" class="form-control" id="end_date" required />
            </div>
            <div class="mb-3">
              <label for="budget" class="form-label">Budget</label>
              <input v-model="campaign.budget" type="number" class="form-control" id="budget" required />
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
        adRequests: [],
        campaign: {
          name: '',
          description: '',
          start_date: '',
          end_date: '',
          budget: 0
        },
        editModalVisible: false,
        deleteModalVisible: false
      };
    },
    mounted() {
      this.fetchCampaignDetails();
      this.fetchAdRequests();
    },
    methods: {
      goBack() {
        this.$router.back();
      },
      fetchAdRequests() {
        const mockAdRequests = [
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
        ];
  
        this.adRequests = mockAdRequests;
      },
      fetchCampaignDetails() {
        const mockCampaign = {
          name: 'Campaign Name',
          description: 'Campaign Description',
          start_date: '2024-06-24',
          end_date: '2024-07-24',
          budget: 5000
        };
  
        this.campaign = mockCampaign;
      },
      showEditModal() {
        this.editModalVisible = true;
      },
      hideEditModal() {
        this.editModalVisible = false;
      },
      updateCampaign() {
        console.log('Updated campaign:', this.campaign);
        this.hideEditModal();
      },
      showDeleteModal() {
        this.deleteModalVisible = true;
      },
      hideDeleteModal() {
        this.deleteModalVisible = false;
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
    margin: 2rem;
  }
  
  .ad-requests-container {
    margin: 2rem;
    padding: 2rem;
  }
  </style>
  
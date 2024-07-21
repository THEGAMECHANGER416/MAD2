<template>
    <section class="intro">
        <div class="mask d-flex align-items-center justify-content-center gradient-custom">
            <div class="container" style="margin-top: 4em;">
                <div class="row justify-content-center">
                    <div class="col-12 col-lg-9 col-xl-7">
                        <div class="mb-4 d-flex flex-row justify-content-center">
                            <span @click="goBack" style="cursor: pointer; color: #1a1a1a; text-decoration: none; font-size: 1.2em; font-weight: 400; box-shadow: none;">
                                <i class="fas fa-arrow-left"></i> Back
                            </span>
                            <div style="flex-grow: 1; display: flex; justify-content: center; margin-left: auto; margin-right: 4em;">
                                <h3 style="margin-bottom: 0; padding-bottom: 0;">Edit Profile</h3>
                            </div>
                        </div>
                        <div class="card">
                            <div class="card-body px-4 py-4 px-md-5">
                                <form @submit.prevent="handleSubmit">
                                    <!-- Show profile image if exists -->
                                    <div v-if="role==='Influencer' && this.formData.image" class="text-center mb-0">
                                        <img :src="imagePreview || 'http://localhost:8000' + this.formData.image" alt="Profile Image" style="width: 150px; height: 150px; object-fit: cover;" class="img-fluid rounded-circle" />
                                    </div>
                                    <!-- Image upload for influencer -->
                                    <div v-if="role==='Influencer'" class="row mb-4 ms-0 me-0 mt-0">
                                        <label for="image" class="form-label">Profile Image</label>
                                        <input type="file" @change="handleFileUpload" class="form-control" />
                                    </div>
                                    
                                    <div class="row mb-4">
                                        <div class="col-md-12">
                                            <div class="form-outline">
                                                <input type="email" v-model="formData.email" id="emailAddress" class="form-control" disabled/>
                                                <label class="form-label" for="emailAddress">Email</label>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div v-if="role === 'Sponsor'" class="row mb-4">
                                        <div class="col-md-6">
                                            <div class="form-outline">
                                                <input type="text" v-model="formData.companyName" id="companyName" class="form-control" />
                                                <label class="form-label" for="companyName">Company Name</label>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-outline">
                                                <input type="text" v-model="formData.industry" id="industry" class="form-control" />
                                                <label class="form-label" for="industry">Industry</label>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div v-if="role === 'Sponsor'" class="row mb-4">
                                        <div class="col-md-6">
                                            <div class="form-outline">
                                                <input type="number" id="budget" class="form-control" v-model="formData.budget" />
                                                <label class="form-label" for="budget">Budget</label>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div v-if="role === 'Influencer'" class="row mb-4">
                                        <div class="col-md-6">
                                            <div class="form-outline">
                                                <input type="text" v-model="formData.name" id="name" class="form-control" />
                                                <label class="form-label" for="name">Name</label>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-outline">
                                                <input type="text" v-model="formData.category" id="category" class="form-control" />
                                                <label class="form-label" for="category">Category</label>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    <div v-if="role === 'Influencer'" class="row mb-4">
                                        <div class="col-md-6">
                                            <div class="form-outline">
                                                <input type="text" v-model="formData.niche" id="niche" class="form-control" />
                                                <label class="form-label" for="niche">Niche</label>
                                            </div>
                                        </div>
                                        <div class="col-md-6">
                                            <div class="form-outline">
                                                <input type="number" v-model="formData.reach" id="reach" class="form-control" />
                                                <label class="form-label" for="reach">Reach</label>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-if="message" class="alert p-0 m-0 text-success">{{ message }}</div>
                                    
                                    <div class="row">
                                        <div class="col-12 text-center mt-1">
                                            <input class="btn btn-warning btn-lg" type="submit" value="Submit" />
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { Input, initMDB } from "mdb-ui-kit";

export default {
    name: 'ProfilePage',
    computed: {
        user() {
            return this.$store.state.user;
        },
        role() {
            return this.$store.state.role;
        }
    },
    watch: {
        user: {
            handler: 'initFormData',
            immediate: true
        },
        role: {
            handler: 'initFormData',
            immediate: true
        }
    },
    created() {
        this.fetchUserDetails();
    },
    mounted() {
        this.initMDBInputs();
        const accessToken = localStorage.getItem('accessToken');
        if (!accessToken) {
            this.$router.push('/register');
        }
    },
    updated() {
        this.initMDBInputs();
    },
    data() {
        return {
            formData: {
                email: '',
                companyName: '',
                industry: '',
                budget: null,
                name: '',
                category: '',
                niche: '',
                reach: null,
                image: ''
            },
            message: '',
            fileName: '',
            imagePreview: null,
        }
    },
    methods: {
        initMDBInputs() {
            const formOutlines = document.querySelectorAll('.form-outline');
            if (formOutlines.length === 0) {
                console.warn('No form outlines found.');
                return;
            }
            initMDB({ Input });
            formOutlines.forEach((formOutline) => {
                new Input(formOutline).init();
            });
        },
        initFormData() {
            if (this.role === 'Sponsor') {
                this.formData.email = this.user.email || '';
                this.formData.companyName = this.user.sponsor?.companyName || '';
                this.formData.industry = this.user.sponsor?.industry || '';
                this.formData.budget = this.user.sponsor?.budget || null;
            } else {
                this.formData.email = this.user.email || '';
                this.formData.image = this.user.influencer?.image || '';
                this.formData.name = this.user.influencer?.name || '';
                this.formData.category = this.user.influencer?.category || '';
                this.formData.niche = this.user.influencer?.niche || '';
                this.formData.reach = this.user.influencer?.reach || null;
            }
        },
        handleFileUpload(event) {
            const file = event.target.files[0];
            if (file) {
                this.fileName = file.name;  // Set the filename property
                const reader = new FileReader();
                reader.onloadend = () => {
                    this.imagePreview = reader.result; // Base64 string of the image
                    this.formData.image = file; // Store the file itself
                };
                reader.readAsDataURL(file);
            }
        },
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
        handleSubmit() {
            try {
                const accessToken = localStorage.getItem('accessToken');
                if (!accessToken) {
                    this.$router.push('/register');
                    return;
                }

                const formData = new FormData();

                if (this.formData.image) {
                    formData.append('image', this.formData.image);
                }

                if (this.role === 'Sponsor') {
                    formData.append('companyName', this.formData.companyName);
                    formData.append('industry', this.formData.industry);
                    formData.append('budget', this.formData.budget);
                } else {
                    formData.append('name', this.formData.name);
                    formData.append('category', this.formData.category);
                    formData.append('niche', this.formData.niche);
                    formData.append('reach', this.formData.reach);
                }

                const myHeaders = new Headers();
                myHeaders.append("Authorization", `Bearer ${accessToken}`);

                const requestOptions = {
                    method: "PUT",
                    headers: myHeaders,
                    body: formData,
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
                        console.log('Profile updated successfully', data);
                        this.$store.dispatch("updateUser", data);
                        this.message = "Profile Updated Successfully";
                    })
                    .catch((error) => {
                        console.error('Error updating profile:', error.message);
                    });
            } catch (error) {
                console.error('Error submitting form:', error.message);
            }
        },
        goBack() {
            this.$router.back();
        }
    }
}
</script>

<style scoped>
.intro {
    height: 100%;
}
.back-button {
    cursor: pointer;
    color: #1a1a1a;
    text-decoration: none;
    font-size: 1.2em;
    font-weight: 400;
    box-shadow: none;
}
.back-button:hover {
    font-weight: 500;
}
</style>

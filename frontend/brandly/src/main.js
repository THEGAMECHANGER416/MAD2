// main.js
import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
import SignupPage from './pages/SignupPage.vue';
import 'mdb-vue-ui-kit/css/mdb.min.css';
import LoginPage from './pages/LoginPage.vue';
import HomePage from './pages/HomePage.vue';
import ProfilePage from './pages/ProfilePage.vue'
import store from './store'; // Import Vuex store
import CampaignDetail from './pages/CampaignDetail.vue'
import SearchPage from './pages/SearchPage.vue'

Vue.config.productionTip = false;
Vue.use(VueRouter);

const router = new VueRouter({
  routes: [
    { path: '/', component: HomePage },
    { path: '/login', component: LoginPage },
    { path: '/register', component: SignupPage },
    { path: '/editProfile', component: ProfilePage },
    {
      path: '/campaign/:id',
      name: 'CampaignDetail',
      component: CampaignDetail,
      props: true
    },
    { path: '/search', component: SearchPage}
  ],
});

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');

export default router;
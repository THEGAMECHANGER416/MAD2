import Vue from 'vue';
import VueRouter from 'vue-router';
import App from './App.vue';
import SignupPage from './pages/SignupPage.vue';
import 'mdb-vue-ui-kit/css/mdb.min.css';

Vue.config.productionTip = false;
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
  { path: '/', component: SignupPage },
]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

export {router};
import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import HomePage from './components/HomePage.vue'
import LoginPage from './components/LoginPage.vue'
import 'mdb-vue-ui-kit/css/mdb.min.css';

Vue.config.productionTip = false
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  // { path: '/signup', component: SignupPage },
]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

export {router};
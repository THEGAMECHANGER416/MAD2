import Vue from 'vue'
import VueRouter from 'vue-router'
import App from './App.vue'
import HelloWorld from './components/HelloWorld.vue'
import HomePage from './components/HomePage.vue'

Vue.config.productionTip = false
Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
  { path: '/', component: HomePage },
  { path: '/about', component: HelloWorld }
]
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')

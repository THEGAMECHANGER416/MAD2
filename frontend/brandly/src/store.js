// store/index.js

import Vue from 'vue';
import Vuex from 'vuex';
import router from './main'; // Import the router

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: !!localStorage.getItem('accessToken'),
    user: null,
    role: null,
  },
  mutations: {
    setLoggedIn(state, status) {
      state.isLoggedIn = status;
    },
    setUser(state, user) {
      state.user = user;
    },
    setRole(state, role) {
      state.role = role;
    }
  },
  actions: {
    updateUser({ commit }, user) {
      commit("setUser", user);
      commit("setRole",user.role);
    },
    login({ commit }, { accessToken, user }) {
      localStorage.setItem('accessToken', accessToken);
      commit('setLoggedIn', true);
      commit('setUser', user);
      commit('setRole', user ? user.role : null);
      router.push('/');
    },
    logout({ commit }) {
      localStorage.removeItem('accessToken');
      commit('setLoggedIn', false);
      commit('setUser', null);
      commit('setRole', null);
      router.push('/register');
    },
  },
  getters: {
    role: (state) => state.user ? state.user.role : null,
  }
});

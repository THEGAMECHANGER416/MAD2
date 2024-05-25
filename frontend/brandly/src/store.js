// store/index.js

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: localStorage.getItem('accessToken') !== null,
  },
  mutations: {
    setLoggedIn(state, status) {
      state.isLoggedIn = status;
    },
  },
  actions: {
    login({ commit }, accessToken) {
      localStorage.setItem('accessToken', accessToken);
      commit('setLoggedIn', true);
    },
    logout({ commit }) {
      localStorage.removeItem('accessToken');
      commit('setLoggedIn', false);
    },
  },
});

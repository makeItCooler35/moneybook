import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    perPage: 10,
  },
  getters: {
  },
  mutations: {
    "CHANGE_PER_PAGE"(state, value) {
      state.perPage = value;
    }
  },
  actions: {
  },
  modules: {
  }
})

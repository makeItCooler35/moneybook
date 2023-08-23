import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    perPage: 10,
    selections: {}
  },
  getters: {
    getSelection: (state) => (name) => {
      return state.selections[name] ?? {};
    },
  },
  mutations: {
    "CHANGE_PER_PAGE"(state, value) {
      state.perPage = value;
    },
    "CHANGE_SELECTION"(state, {name, fields}) {
      state.selections[name] = [...fields];
    },
    "CLEAR_SELECTION"(state, name = null) {
      if(!name) {
        this.state.selections = {};
      } else {
        state.selections[name] = {};
      }
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState()]
})

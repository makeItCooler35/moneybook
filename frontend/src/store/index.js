import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    perPage: 10,
    selections: {},
    jobs: {}
  },
  getters: {
    getSelection: (state) => (name) => {
      return state.selections[name] ?? {};
    },
    getJobs(state) {
      return state.jobs;
    },
    getJob: (state) => (jobId) => {
      return state.jobs[jobId]?.title ?? '';
    }
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
    },
    "CLEAR_JOBS"(state) {
      state.jobs = {};
    },
    "ADD_JOB"(state, {jobId, title='', timer}) {
      state.jobs[jobId] = {
        status: '',
        title,
        timer
      };
      state.jobs = {...state.jobs};
    },
    "CHANGE_JOB"(state, payload) {
      const jobId = payload.jobId;
      state.jobs[jobId] = {
        status: payload?.status ?? state.jobs[jobId]?.status ?? '',
        timer: payload?.timer ?? null,
        title: payload?.title ?? state.jobs[jobId]?.title ?? ''
      };
      state.jobs = {...state.jobs};
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState()]
})

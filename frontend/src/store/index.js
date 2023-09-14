import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate';

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    perPage: 10,
    selections: {},
    jobs: []
  },
  getters: {
    getSelection: (state) => (name) => {
      return state.selections[name] ?? {};
    },
    getJobs(state) {
      return [...state.jobs].reverse();
    },
    getJob: (state) => (jobId) => {
      return state.jobs.filter(x => x.jobId ==jobId)?.[0] ?? {};
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
    "ADD_JOB"(state, {jobId, title='', timer, responseType}) {
      state.jobs.push({
        jobId, title, timer, responseType,
        status: '',
        startTime: (new Date()).toLocaleString("ru-RU"),
      });

      state.jobs = [...state.jobs];
    },
    "CHANGE_JOB"(state, payload) {
      const jobId = payload.jobId;
      const index = state.jobs.findIndex(x => x.jobId == jobId);
      if(index > -1) {
        state.jobs[index] = {...state.jobs[index],
          status: payload?.status ?? state.jobs[index]?.status ?? '',
          timer: payload?.timer ?? null,
          result: payload.result
        };
  
        state.jobs = [...state.jobs];
      }
    },
    "DELETE_JOB"(state, jobId) {
      if(jobId === null) {
        state.jobs.forEach(x => {
          if(typeof(x.result) == 'string' && x.result.includes('blob')) {
            URL.revokeObjectURL(x.result);
          }
        });
        state.jobs = [];
      } else {
        const index = state.jobs.findIndex(x => x.jobId == jobId);
        if(index > -1) {
          const url = state.jobs[index]?.result;
          if(typeof(url) == 'string' && url.includes('blob')) {
            URL.revokeObjectURL(url);
          }

          state.jobs.splice(index, 1);
        }
      }
    }
  },
  actions: {
  },
  modules: {
  },
  plugins: [createPersistedState()]
})

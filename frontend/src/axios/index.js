import axios from "axios";

class Axios
{
  constructor(app) {
    this.app = app;

    this.instance = axios.create({
      baseURL: process.env.VUE_APP_BACK_HOST,
    });

    this.instance.interceptors.request.use(this.apiRequestHandler.bind(this), this.apiRequestErrorHandler.bind(this));

    this.instance.interceptors.response.use(this.apiResponseHandler.bind(this), this.apiResponseErrorHandler.bind(this));
  }

  _toShowToast(method) {
    return ['post', 'delete', 'patch'].includes(method) ? true : false
  }

  apiRequestHandler(config) {
    if(config.method == 'post' && config.data) {
      for(const item of Object.values(config.data)) {
        if(item instanceof Blob) {
          config.data.bgTask = 1;
          break;
        }
      }
    }

    return config;
  }

  apiRequestErrorHandler(err) {
    const message = err.response.data.error.message;
    this.app.$toast(message, 1);
    return err.response;
  }

  async apiResponseHandler(response) {    
    //this.app.$store.commit("CLEAR_JOBS");
    const jobId = response?.data?.jobId;

    if(response.status == 202) {
      const timer = setTimeout(async() => {
        await this.app.$http.get("jobs", {params: {jobId}});
      }, 5000);

      this.app.$store.commit("ADD_JOB", {
        jobId,
        title: response.data.title,
        timer
      });
    } else if(jobId) {
      this.apiCheckStatusJob(response, jobId);
    } else if(this._toShowToast(response.config.method)) { // обычная (нефоновая) задача
      this.app.$toast("Операция завершена.", 0);
    }
  
    return response;
  }

  apiCheckStatusJob(response, jobId) {
    if(!(response?.data?.end)) {
      const timer = setTimeout(async() => {
        await this.app.$http.get("jobs", {params: {jobId}});
      }, 5000);

      this.app.$store.commit("CHANGE_JOB", {jobId, timer});
    } else {
      this.app.$store.commit("CHANGE_JOB", {
        jobId,
        status: response.data.status
      });
      
      const title = this.app.$store.getters.getJob(jobId);
      this.app.$toast(`${title}: Операция завершена.`, 0);
    }
  }

  apiResponseErrorHandler(err) {
    const message = err.response.data.error.message;
    this.app.$toast(message, 1);
    return err.response;
  }
}


export default Axios;
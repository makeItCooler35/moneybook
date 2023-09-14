import axios from "axios";

class Axios
{
  constructor(app) {
    this.app = app;
    this.timeToAskServer = 5000;

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

      if(config?.responseType == 'blob') {
        config.data.bgTask = 1;
      }

      if(config.data.bgTask) {
        config.service = {
          title: config.data.title ?? '',
          responseType: config.responseType ?? 'json'
        };

        // blob нам нужен только при получении результата
        config.responseType = 'json';
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
    const jobId = response.headers?.['job-id'];
    if(jobId) {
      if(response.status === 202) {
        this.apiAddJob(response, jobId);
      } else {
        this.apiCheckStatusJob(response, jobId);
      }
    } else if(this._toShowToast(response.config.method)) { // обычная (нефоновая) задача
      this.app.$toast("Операция завершена.", 0);
    }
  
    return response;
  }

  apiAddJob(response, jobId) {
    const timer = setTimeout(() => {
      this.app.$http.get("jobs", {
        params: {
          jobId,
          get_result: 0
        }
      });
    }, this.timeToAskServer);

    this.app.$store.commit("ADD_JOB", {
      jobId, timer,
      title: response.config.service.title,
      responseType: response.config.service.responseType
    });
  }

  apiCheckStatusJob(response, jobId) {
    const hasResult = Boolean(Number(response.headers?.["job-result-return"]));
    const responseType = this.app.$store.getters.getJob(jobId).responseType ?? 'json';

    if(!hasResult) {
      //сервер скажет, когда работа выполнена
      const jobEnd = Number(response.headers?.['job-end']);

      // если работа была выполнена, то запросим результат,
      // иначе продолжим опрашивать
      const timer = setTimeout(() => {
        this.app.$http.get("jobs", {
          params: {
            jobId,
            get_result: jobEnd
          },
          responseType: jobEnd ? responseType : 'json'
        });
      }, this.timeToAskServer);
    
      this.app.$store.commit("CHANGE_JOB", { jobId, timer });
    } else {
      let result = response.data;
      if(response.config.responseType == 'blob') {
        result = URL.createObjectURL(response.data);
      }

      this.app.$store.commit("CHANGE_JOB", {
        jobId, result,
        status: response.data.status,
        headers: response.headers
      });

      const title = this.app.$store.getters.getJob(jobId)?.title ?? '';
      this.app.$toast(`${title}: Операция завершена.`, 0);
    }
  }

  apiResponseErrorHandler(err) {
    const message = err.response?.data?.error?.message;
    this.app.$toast(message, 1);
    return err.response;
  }
}

export default Axios;
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
    return err.response;
  }

  apiResponseHandler(response) {
    if(this._toShowToast(response.config.method)) {
      this.app.$toast("Операция завершена.", 0);
   }
  
    return response;
  }

  apiResponseErrorHandler(err) {
    const message = err.response.data.error.message;
    this.app.$toast(message, 1);
    return err.response;
  }
}


export default Axios;
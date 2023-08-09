import axios from "axios";

class Axios
{
  constructor(app) {
    this.app = app;

    this.instance = axios.create({
      baseURL: process.env.VUE_APP_BACK_HOST,
    });

    this.instance.interceptors.response.use(this.apiResponseHandler.bind(this), this.apiResponseErrorHandler.bind(this));
  }

  _toShowToast(method) {
    return ['post', 'delete', 'patch'].indexOf(method) > -1 ? true : false
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
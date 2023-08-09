import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import Axios from './axios'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import NTable from '@/components/NTable'

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './assets/styles/style.scss'

// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.component('n-table', NTable)
Vue.component('n-table2', NTable)

Vue.config.productionTip = false

const app = new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')

const axios = new Axios(app);
Vue.prototype.$http = axios.instance;

Vue.prototype.$toast = (message = '', status = 0) => {
  const properties = [
    {
      variant: 'success',
      title: 'Успешно'
    },
    {
      variant: 'danger',
      title: 'Ошибка'
    },
    {
      variant: 'warning',
      title: 'Предупрждение'
    },
    {
      variant: 'info',
      title: 'Инфо'
    }
  ];
  const prop = properties[status];

  app.$bvToast.toast(message, {
    autoHideDelay: 5000,
    variant: prop.variant,
    title: prop.title,
    toaster: 'b-toaster-bottom-right',
    solid: true
  });
}


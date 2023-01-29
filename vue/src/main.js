import {createApp} from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import ConfirmationService from 'primevue/confirmationservice';

import "primevue/resources/themes/lara-light-indigo/theme.css"
import "primevue/resources/primevue.min.css"
import "primeicons/primeicons.css"
import "./assets/css/app.css"
import "./assets/css/irregulars.css"
import "./assets/css/flex.css"
import "./assets/css/columns.css"
import "./assets/css/reset.css"
import "./assets/css/form.css"

createApp(App)
  .use(store)
  .use(router)
  .use(PrimeVue)
  .use(ToastService)
  .use(ConfirmationService)
  .mount('#app')

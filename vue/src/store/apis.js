import {CSRF_TOKEN} from "@/csrfToken";
import BASE_URL from "@/config"
import axios from "axios"
import store from "../store/index"

export default {
  /*-----------------------------------------
  *
  * crud operations
  * get, post, put, patch and delete
  * crud "payload" object contains keys which
  * -- form, action, endpoint --
  * it runs with action key
  *
  * */
  crud(payload){
    axios.defaults.headers.common['X-CSRFToken'] = CSRF_TOKEN;
    switch (payload.action){
      case "get":
        return axios.get(BASE_URL+payload.endpoint+window.location.search);
      case "post":
        return axios.post(BASE_URL+payload.endpoint, payload.data)
      case "put":
        return axios.put(BASE_URL+payload.endpoint, payload.data)
      case "patch":
        return axios.patch(BASE_URL+payload.endpoint, payload.data)
      case "delete":
        return axios.delete(BASE_URL+payload.endpoint)
      default:
        break;
    }
  }
}
import {createStore} from 'vuex'
import data from "./modules/index"


export default createStore({
  modules: {
    data
  },
})

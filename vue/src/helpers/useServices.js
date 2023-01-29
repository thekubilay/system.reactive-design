import store from "../store/index"

export default class UseServices {
  useCrud(payload){
    return new Promise((resolve, reject) => {
      store.dispatch("data/CRUD", payload).then((response) => {
        resolve(response)
        if (payload.hasOwnProperty("commit") && payload.commit){
          store.commit(payload.commit, response)
        }
      }).catch((e) => {
        console.log(e)
      })
    })
  }
}
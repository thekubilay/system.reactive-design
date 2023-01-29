import apis from "../apis"

export const actions = {
  CRUD({commit}, payload){
    return new Promise((resolve, reject) => {
      apis.crud(payload).then(response => {
        resolve(response.data)
      }).catch((error) => {
        reject(error)
      })
    })
  },
}
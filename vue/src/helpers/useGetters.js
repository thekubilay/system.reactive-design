import {useStore} from "vuex";
import {computed} from "vue";

export default function () {
  const store = useStore()
  const getProjects = computed(() => {
    return store.getters["data/GET_PROJECTS"]
  })

  return {
    getProjects
  }
}
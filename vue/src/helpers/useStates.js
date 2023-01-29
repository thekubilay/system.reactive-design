import {useStore} from "vuex";
import {computed} from "vue";

export default function () {
  const store = useStore()
  const user = computed(() => {
    return store.state.data.user
  })
  const teams = computed(() => {
    return store.state.data.teams
  })
  const team = computed(() => {
    return store.state.data.team
  })
  const projects = computed(() => {
    return store.state.data.projects
  })
  const currentEndDate = computed(() => {
    return store.state.data.currentEndDate
  })
  const currentEndDateIso = computed(() => {
    return store.state.data.currentEndDateIso
  })
  const invoiceType = computed(() => {
    return store.state.data.invoiceType
  })

  return {
    store, user, currentEndDate, currentEndDateIso, invoiceType, teams, team, projects
  }
}
export const mutations = {
  SET_USER(state, val) {
    state.user = val
  },
  SET_TEAMS(state, val) {
    state.teams = val
  },
  SET_TEAM(state, val) {
    state.team = val
  },
  SET_PROJECTS(state, val) {
    state.projects = val
  },
  SET_TASKS(state, val) {
    state.tasks = val
  },
  SET_CURRENT_END_DATE(state, val) {
    state.currentEndDate = val
  },
  SET_CURRENT_END_DATE_ISO(state, val) {
    state.currentEndDateIso = val
  },
  SET_INVOICE_TYPE(state, val) {
    state.invoiceType = val
  },
}
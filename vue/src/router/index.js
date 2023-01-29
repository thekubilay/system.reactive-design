import {createRouter, createWebHistory} from 'vue-router'
import store from "../store/index"
import Invoice from '@/views/InvoiceList.vue'
import ProjectList from "@/views/ProjectList";
import TotalInvoice from "@/views/TotalInvoiceList";
import CustomInvoice from "@/views/CustomInvoice";
import UseServices from "@/helpers/useServices"
import UseFormatter from "@/utils/UseFormatter";
const routes = [
  {
    path: '/',
    name: 'ProjectList',
    component: ProjectList,
    meta: {
      title: "分譲"
    }
  },
  {
    path: '/invoices/',
    name: 'Invoice',
    component: Invoice,
    meta: {
      title: "分譲"
    }
  },
  {
    path: '/total-invoices/',
    name: 'TotalInvoice',
    component: TotalInvoice,
    meta: {
      title: "分譲"
    }
  },
  {
    path: '/custom-invoice/',
    name: 'CustomInvoice',
    component: CustomInvoice,
    meta: {
      title: "分譲"
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env["VUE_APP_BASE_PATH"]),
  routes
})

function isAuth(to, from) {
  return new Promise((resolve, reject) => {
    const services = new UseServices()
    services.useCrud({action: "get", endpoint: "users/current/", commit: "data/SET_USER"}).then(response => {
      if (response) resolve(true)
    }).catch(e => {
      reject(false)
    })
  })
}

function areTeams(to, from) {
  return new Promise((resolve, reject) => {
    const services = new UseServices()
    services.useCrud({
      action: "get",
      endpoint: "teams/",
      commit: "data/SET_TEAMS"
    }).then(response => {
      // console.log(response)
      resolve(response)
    }).catch(e => {
      reject(false)
    })
  })
}

function areProjects(to, from) {
  return new Promise((resolve, reject) => {
    const services = new UseServices()
    services.useCrud({
      action: "get",
      endpoint: "projects/",
      commit: "data/SET_PROJECTS",
    }).then(response => {
      resolve(response)
    }).catch(e => {
      reject(false)
    })
  })
}

function areTasks(to, from) {
  return new Promise((resolve, reject) => {
    const services = new UseServices()
    services.useCrud({
      action: "get",
      endpoint: "tasks/",
      commit: "data/SET_TASKS",
    }).then(response => {
      resolve(response)
    }).catch(e => {
      reject(false)
    })
  })
}

router.beforeEach((to, from, next) => {
  const formatter = new UseFormatter()
  const date = new Date();
  const SD = new Date(date.getFullYear(), date.getMonth(), 2);
  const ED = new Date(date.getFullYear(), date.getMonth() + 1, 1);

  let payload = {start_date: SD.toISOString().substring(0, 10), end_date: ED.toISOString().substring(0, 10)}
  if (to.query.hasOwnProperty("start_date") && to.query.hasOwnProperty("end_date")) {
    payload = to.query
  }

  if (!store.state.data.user) {
    isAuth().then(user => {
      areTeams(to, from).then(teams => {
        payload.tid = teams[0]["tid"]
        router.replace({name: to.name, query: payload}).then(() => {
          const currentEndDate = payload.end_date.substring(0,4) + '年' + payload.end_date.substring(5, 7) + '月' + payload.end_date.substring(8, 10) + '日'
          store.commit("data/SET_CURRENT_END_DATE_ISO", payload.end_date)
          store.commit("data/SET_CURRENT_END_DATE", currentEndDate)
          store.commit("data/SET_TEAM", teams[0].tid)
          areProjects().then(projects => {
            next({name: to.name, query:payload})
            formatter.priceFormatter
          })
        })
      })
    })
  } else {
    next()
    formatter.priceFormatter
  }
})

export default router

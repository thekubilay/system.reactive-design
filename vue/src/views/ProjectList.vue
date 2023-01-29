<template>
  <div id="project-list">
    <Toast/>
    <page-toolbar class="flex align-center justify-space-between">
      <div class="column-2" style="padding-left: 10px">
        <select v-model="setTeam">
          <option v-for="(item, idx) in teams" :key="idx" :value="item.tid">{{item.name}}</option>
        </select>
      </div>
      <div class="right flex justify-end column-2">
        <div class="dr2 wrapper">
          <span class="label-title block">日付</span>
          <div class="wrapper flex">
            <button class="year-button prev-year flex align-center justify-center" @click="changeYear(false)">1年前
            </button>
            <Dropdown v-model="setCurrentEndDateIso" :options="ufn_get_end_of_months(year)" option-label="name"
                      option-value="value"/>
            <button class="year-button next-year flex align-center justify-center" @click="changeYear(true)">1年次
            </button>
          </div>
        </div>
      </div>
    </page-toolbar>
    <DataTable :value="projects" class="p-datatable-sm" :scrollable="true" scrollHeight="100%"
               :reorderableColumns="false"
               @columnReorder="onColReorder" @rowReorder="onRowReorder" editMode="row" dataKey="id"
               v-model:editingRows="editingRows" @row-edit-save="onRowEditSave">
      <template #header>
        <div class="flex justify-space-between align-center">
          <h5 class="p-m-0">物件一覧（{{ projects.length }}個）</h5>
          <p v-if="currentEndDate && !projects.length" style="color: #e74c3c; font-weight: 400; font-size: .9rem">
            {{ currentEndDate.substring(0, 8) }}には本番公開になっているタスクがありません</p>
        </div>
      </template>
      <Column :rowReorder="true" headerStyle="min-width:60px; width:10%;"
              style="min-width:60px; width:10%;" :reorderableColumn="false"/>
      <Column field="oid" header="順番" headerStyle="min-width:60px; width:10%;"
              style="min-width:60px; width:10%;"></Column>
      <Column field="pid" header="ASANA ID" headerStyle="min-width: 70px; width:20%" style="min-width: 70px; width:20%">
        <template #editor="{ data, field }">
          <InputText v-model="data[field]"/>
        </template>
      </Column>
      <Column field="name" header="物件名" headerStyle="min-width: 300px; width:20%" style="min-width: 300px; width:20%">
        <template #editor="{ data, field }">
          <InputText v-model="data[field]"/>
        </template>
      </Column>
      <Column field="company_name" header="会社名" headerStyle="min-width: 300px; width:20%"
              style="min-width: 300px; width:20%">
        <template #editor="{ data, field }">
          <InputText v-model="data[field]"/>
        </template>
      </Column>
      <Column :rowEditor="true" headerStyle="width:20%; min-width:8rem" style="width:20%; min-width:8rem"
              bodyStyle="text-align:center; justify-content:flex-end"></Column>
    </DataTable>

  </div>
</template>

<script>
import {ref, reactive, computed} from "vue";
import Dropdown from "primevue/dropdown";
import DataTable from "primevue/datatable"
import Column from "primevue/column"
import Toast from "primevue/toast"
import InputText from "primevue/inputtext"
import Checkbox from 'primevue/checkbox';

import {ufn_get_end_of_months} from "@/utils/ufn";
import {useToast} from "primevue/usetoast";
import useStates from "@/helpers/useStates";
import UseServices from "@/helpers/useServices"
import UseFormatter from "@/utils/UseFormatter";
import PageToolbar from "@/components/bars/PageToolBar";
import {useRoute, useRouter} from "vue-router";

export default {
  name: "ProjectList",
  components: {PageToolbar, Dropdown, DataTable, Column, Toast, InputText, Checkbox},
  setup() {
    const services = new UseServices()
    const router = useRouter()
    const route = useRoute()
    const {store, currentEndDate, currentEndDateIso, projects, teams, team} = useStates()
    const year = ref(new Date().getFullYear())

    const toast = useToast();
    const editingRows = ref([]);
    const columns = ref([
      {field: 'oid', header: '順番'},
      {field: 'pid', header: 'asana id'},
      {field: 'name', header: '物件名'},
      {field: 'company_name', header: '会社名'},
    ]);
    const form = reactive({
      archived: false
    })
    const onColReorder = () => {
      toast.add({severity: 'success', summary: '列が変更されました。', life: 3000});
    };
    const onRowReorder = (event) => {
      event.value.forEach((item, i) => {
        item.oid = i + 1
      })
      store.commit("data/SET_PROJECTS", event.value)
      const payload = {action: "post", endpoint: "reorders/", data: {reordered: event.value}}
      services.useCrud(payload).then(() => {
        toast.add({severity: 'success', summary: '行が変更されました。', life: 3000});
      })
    };

    const setTeam = computed({
      set(val) {
        router.replace({
          query: {
            start_date: year.value + "-01-01",
            end_date: year.value + "-01-31",
            tid: val
          }
        }).then(() => {
          store.commit("data/SET_TEAM", val)
          services.useCrud({
            action: "get",
            endpoint: "projects/",
            commit: "data/SET_PROJECTS",
          }).then(response => {
            formatter.priceFormatter
            resolve(response)
          }).catch(e => {
            reject(false)
          })


        })
      },
      get(){
        return team.value
      }
    })

    const changeYear = (bool) => {
      if (bool) {
        year.value = year.value + 1
        const ed = year.value + '年' + '12月' + '31日'
        router.replace({
          query: {
            start_date: year.value + "-01-01",
            end_date: year.value + "-01-31",
            tid: route.query.tid
          }
        }).finally(() => {
          store.commit("data/SET_CURRENT_END_DATE", ed)
          store.commit("data/SET_CURRENT_END_DATE_ISO", year.value + "-01-31")
          services.useCrud({
            action: "get",
            endpoint: "projects/",
            commit: "data/SET_PROJECTS",
          })
        })
      } else {
        year.value = year.value - 1
        const ed = year.value + '年' + '12月' + '31日'
        router.replace({
          query: {
            start_date: year.value + "-01-01",
            end_date: year.value + "-01-31",
            tid: route.query.tid
          }
        }).finally(() => {
          store.commit("data/SET_CURRENT_END_DATE", ed)
          store.commit("data/SET_CURRENT_END_DATE_ISO", year.value + "-12-31")
          services.useCrud({
            action: "get",
            endpoint: "projects/",
            commit: "data/SET_PROJECTS",
          })
        })
      }
    }

    const onCellEditComplete = (event) => {
      let {data, newValue, field} = event;
      if (newValue.trim().length > 0)
        data[field] = newValue;
      event.preventDefault();
    };

    const onRowEditSave = (event) => {
      let {newData, index} = event;
      const payload = {action: "patch", endpoint: "projects/" + newData.id + "/", data: newData}
      services.useCrud(payload).then(() => {
        services.useCrud({
          action: "get",
          endpoint: "projects/",
          commit: "data/SET_PROJECTS",
        })
      })
    };

    const setCurrentEndDateIso = computed({
      set(val) {
        router.replace({
          query: {
            start_date: val.substring(0, 8) + "01",
            end_date: val,
            tid: route.query.tid
          }
        }).finally(() => {
          const ed = val.substring(0, 4) + '年' + val.substring(5, 7) + '月' + val.substring(8, 10) + '日'
          store.commit("data/SET_CURRENT_END_DATE", ed)
          store.commit("data/SET_CURRENT_END_DATE_ISO", val)
          services.useCrud({
            action: "get",
            endpoint: "projects/",
            commit: "data/SET_PROJECTS",
          })
        })
      },
      get() {
        return currentEndDateIso.value
      }
    })

    return {
      form, columns, projects, editingRows, year, currentEndDate, setCurrentEndDateIso, teams,
      ufn_get_end_of_months, setTeam,
      changeYear, onColReorder, onRowReorder, onRowEditSave, onCellEditComplete,
    }
  }
}
</script>

<style>
#project-list {
  height: calc(100% - 120px);
}

#project-list .p-datatable {
  margin: 0 14px;
  height: calc(100% - 50px);
}

#project-list .p-datatable .p-datatable-thead > tr > th {
  flex: inherit;

}

#project-list .p-datatable.p-datatable-sm .p-datatable-tbody > tr > td {
  padding: 0.1rem 0.5rem;
  font-size: .7rem;
  flex: inherit;
}

#project-list .p-datatable.p-datatable-sm .p-datatable-tbody > tr > td .p-datatable-reorderablerow-handle {
  cursor: grab;
  height: 100%;
  display: flex;
  align-content: center;
  align-items: center;
}

#project-list .p-datatable.p-datatable-sm .p-datatable-tbody > tr > td .p-inputtext {
  font-size: .7rem;
  color: #495057;
  background: #ffffff;
  padding: 0.35rem 0.75rem 0.35rem 4px;
  width: 95%;
  border: 1px solid #ced4da;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s, box-shadow 0.2s;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  border-radius: 0;
}

#project-list .p-datatable.p-datatable-sm .p-datatable-tbody > tr > td .p-inputtext:focus {
  box-shadow: 0 0 0 0.1rem #c7d2fe;
  border-color: #6366F1;
}
</style>
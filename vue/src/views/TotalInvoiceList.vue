<template>
  <div id="total-invoice-list">
    <page-toolbar class="flex align-center justify-space-between">
      <div class="column-2"></div>
      <div class="right flex justify-end column-2">
        <div class="wrapper">
          <span class="label-title block">タイプ</span>
          <div class="dr1 wrapper flex">

            <Dropdown v-model="setInvoiceType" :options="['御見積書', '御請求書']" placeholder=""/>
          </div>
        </div>
        <button class="year-button prev-year flex align-center justify-center" @click="changeYear(false)">1年前</button>
        <div class="dr2 wrapper">
          <span class="label-title block">日付</span>
          <div class="wrapper flex">
            <Dropdown v-model="setCurrentEndDateIso" :options="ufn_get_end_of_months(year)" option-label="name"
                      option-value="value"/>
          </div>
        </div>
        <button class="year-button next-year flex align-center justify-center" @click="changeYear(true)">1年次</button>
        <div class="wrapper" style="margin-right: 14px">
          <span class="label-title block">税金</span>
          <div class="dr1 wrapper flex">
            <Dropdown v-model="isTax" :options="[{name:'税込', value:true}, {name:'税抜', value:false}]" option-label="name"
                      option-value="value"/>
          </div>
        </div>
        <div class="dr3 wrapper">
          <span class="label-title block">物件</span>
          <div class="wrapper flex">
            <MultiSelect v-model="setProjects" :options="projects" :filter="true" optionLabel="name"/>
          </div>
        </div>
      </div>
    </page-toolbar>

    <div v-if="teamData" class="contents flex-column align-center overflow-y column-1"
         style="height: 100%;padding: 20px 0 80px 0">
      <div class="totals">
        <h2 class="title">{{ teamData["full_name"] }}</h2>
        <h3 class="type-title">{{ currentEndDate.substring(5, 7) }}月 {{ invoiceType }}</h3>
        <table>
          <thead>
          <tr>
            <th>物件名</th>
            <th>金額</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="project in list" :key="project['id']">
            <td>{{ project["name"] }}</td>
            <td v-if="isTax"><span
                class="price-format block text-right">{{
                parseInt(project["tasks_total"]) + parseInt(project["tax"])
              }}</span>
            </td>
            <td v-else><span class="price-format block text-right">{{ parseInt(project["tasks_total"]) }}</span></td>
          </tr>
          </tbody>
          <tfoot>
          <tr v-if="!isTax">
            <td>小計</td>
            <td class="text-right"><span class="block price-format">{{ totals.totals }}</span></td>
          </tr>
          <tr v-if="!isTax">
            <td>消費税 (10%)</td>
            <td class="text-right"><span class="block price-format">{{ totals.taxes }}</span></td>
          </tr>
          <tr>
            <td>合計金額</td>
            <td class="text-right"><span class="block price-format">{{ totals.totalsWithTax }}</span></td>
          </tr>
          </tfoot>
        </table>
        <div v-if="invoiceType === '御請求書'" class="flex-column justify-start" style="margin-top: 50px">
          <p style="font-size:.8rem;">{{ teamData.setting.invoice_text1 }}</p>
          <p style="font-size:.8rem;">{{ teamData.setting.invoice_text2 }}</p>
          <p style="font-size:.8rem;">{{ teamData.setting.invoice_text3 }}</p>
        </div>

      </div>
    </div>

    <button @click="exportPDF(list, 'totals', isTax)" class="export-all flex align-center">
      <img src="../assets/svg/pdf.svg" alt="pdf">
      <span class="text block text-left">全て <br> エクスポート</span>
    </button>
  </div>
</template>


<script>
import {computed, nextTick, onMounted, ref, watch} from "vue";
import useStates from "@/helpers/useStates";
import usePdfBuilder from "@/helpers/pdf-builder/useMakePdf";
import PageToolbar from "@/components/bars/PageToolBar";
import UseServices from "@/helpers/useServices";
import UseFormatter from "@/utils/UseFormatter";
import {useRoute, useRouter} from "vue-router";
import {ufn_get_end_of_months} from "@/utils/ufn";
import Dropdown from 'primevue/dropdown';
import MultiSelect from 'primevue/multiselect';

export default {
  name: "TotalInvoiceList",
  components: {Dropdown, MultiSelect, PageToolbar},
  setup() {
    const list = ref([])
    const services = new UseServices()
    const formatter = new UseFormatter()
    const router = useRouter()
    const route = useRoute()
    const {store, team, teams, invoiceType, currentEndDate, currentEndDateIso, projects} = useStates()
    const year = ref(new Date().getFullYear())
    const {exportPDF} = usePdfBuilder()
    const isTax = ref(true)
    const teamData = ref()

    onMounted(() => {
      nextTick(() => {
        team.value = route.query.tid
        list.value = projects.value
        teamData.value = teams.value.find(item => {
          return item.tid === parseFloat(team.value)
        })
      })

    })

    watch(() => projects.value, val => {
      list.value = val
    })
    watch(() => isTax.value, val => {
      formatter.priceFormatter
    })


    const totals = computed(() => {
      const to = sumData(list.value, "tasks_total")
      const ta = sumData(list.value, "tax")
      return {
        totals: to,
        taxes: ta,
        totalsWithTax: to + ta
      }
    })

    function sumData(array, propertyName) {
      let sum = 0;
      array.forEach(item => {
        sum += parseInt(item[propertyName]) ?? 0;
      });
      return sum;
    }

    const setProjects = computed({
      set(val) {
        list.value = val.sort((a, b) => {
          return a.oid - b.oid
        })
        formatter.priceFormatter
      },
      get() {
        return list.value
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

    const setInvoiceType = computed({
      set(val) {
        store.commit("data/SET_INVOICE_TYPE", val)
      },
      get() {
        return invoiceType.value
      }
    })

    return {
      year,
      list,
      isTax,
      teamData,
      projects,
      invoiceType,
      currentEndDate,
      totals,
      setCurrentEndDateIso,
      setProjects,
      setInvoiceType,
      ufn_get_end_of_months,
      changeYear,
      exportPDF,
    }
  }
}
</script>

<style scoped>
#total-invoice-list {
  height: calc(100% - 46px);
}

#total-invoice-list > button.export-all {
  z-index: 101;
  position: fixed;
  right: 40px;
  bottom: 40px;
  width: 140px;
  height: 60px;
  background-color: #f1f1f1;
  box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
}

#total-invoice-list > button.export-all > img {
  height: 50px;
}

#total-invoice-list .totals {
  position: relative;
  height: auto;
  width: 755px;
  padding: 50px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  margin-bottom: 20px
}

#total-invoice-list .totals > h2.title {
  font-weight: 300;
  font-size: 1.4rem;
}

#total-invoice-list .totals > h3.type-title {
  font-weight: 400;
  font-size: 2.4rem;
  margin-bottom: 20px;
}

#total-invoice-list .totals table {
  width: 100%;
  border-collapse: collapse;
}

#total-invoice-list .totals thead th {
  font-weight: 400;
  height: 30px;
  font-size: .9rem;
  vertical-align: center;
  text-align: center;
  border-top: 1px solid #e1e0e0;
  border-bottom: 2px solid #000000;
  border-right: 1px solid #e1e0e0;
}

#total-invoice-list .totals thead th:first-child,
#total-invoice-list .totals tbody td:first-child,
#total-invoice-list .totals tfoot td:first-child {
  width: calc(100% - 100px);
}

#total-invoice-list .totals thead th:last-child,
#total-invoice-list .totals tbody td:last-child,
#total-invoice-list .totals tfoot td:last-child {
  width: 100px;
  min-width: 100px;
  border-right: 0;
}

#total-invoice-list .totals tbody td,
#total-invoice-list .totals tfoot td {
  font-weight: 400;
  min-height: 20px;
  padding: 5px 0;
  height: auto;
  font-size: .8rem;
  vertical-align: center;
  text-align: left;
  border-top: 1px solid #e1e0e0;
  border-bottom: 1px solid #e1e0e0;
  border-right: 1px solid #e1e0e0;
  position: relative;
}

#total-invoice-list .totals tfoot {
  border-top: 2px solid #000000;
}

#total-invoice-list .totals tfoot td:last-child {
  text-align: right;
}

/*#total-invoice-list .totals tbody td > span:last-child {*/
/*  position: absolute;*/
/*  top: 50%;*/
/*  min-width: 50px;*/
/*  width: 50px;*/
/*}*/


</style>
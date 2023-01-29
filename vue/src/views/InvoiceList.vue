<template>
  <div id="invoice-list" class="flex-column align-center">
    <Toast/>
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
        <div class="dr3 wrapper">
          <span class="label-title block">物件</span>
          <div class="wrapper flex">
            <MultiSelect v-model="setProjects" :options="projects" :filter="true" optionLabel="name"/>
          </div>
        </div>
      </div>
    </page-toolbar>

    <div class="contents flex-column align-center overflow-y column-1">
      <div class="invoice" :class="{first:idx===0}" v-for="(project, idx) in list" :key="project['id']">
        <div class="dev-buttons flex">
<!--          <button class="transfer" @click="transferData(idx)"><img src="../assets/svg/transfer.svg" alt="transfer data">-->
<!--          </button>-->
          <button class="edit relative" @click="project.styles.display = true">
            <img src="../assets/svg/text-edit.svg" alt="edit">
          </button>
          <button class="export" @click="exportPDF([project])"><img src="../assets/svg/pdf.svg" alt="pdf"></button>
          <div v-if="project.styles.display" class="bubble absolute flex-column">
            <button @click="project.styles.display = false" class="close"><img src="../assets/svg/close.svg" alt=""></button>
            <div class="wrapper flex-column" >
              <InputNumber v-model="project['styles']['headerTitleFontSize']" showButtons buttonLayout="horizontal"
                           decrementButtonClass="inc-btn-color" incrementButtonClass="inc-btn-color"
                           incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus"/>
            </div>
            <span class="wrapper flex-column">
                <InputNumber v-model="project['styles']['headerContentTextFontSize']" showButtons
                             buttonLayout="horizontal"
                             decrementButtonClass="inc-btn-color" incrementButtonClass="inc-btn-color"
                             incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus"/>
              </span>
            <span class="wrapper flex-column">
                <InputNumber v-model="project['styles']['headerBrandTextSize']" showButtons buttonLayout="horizontal"
                             decrementButtonClass="inc-btn-color" incrementButtonClass="inc-btn-color"
                             incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus"/>
              </span>
            <span class="wrapper flex-column">
                <InputNumber v-model="project['styles']['bodyContentFontSize']" showButtons buttonLayout="horizontal"
                             decrementButtonClass="inc-btn-color" incrementButtonClass="inc-btn-color"
                             incrementButtonIcon="pi pi-plus" decrementButtonIcon="pi pi-minus"/>
              </span>
            <button class="submit pointer block" @click="editPage(project.id, project.styles)">運用</button>
          </div>
        </div>
        <h3 class="invoice-type">{{ invoiceType }}</h3>

        <div class="invoice-header flex justify-space-between">
          <div class="header-left column-2-space">
            <dl class="flex first align-center">
              <dt>宛先</dt>
              <dd>{{ project["company_name"] }}</dd>
            </dl>
            <dl class="flex align-center">
              <dt>件名</dt>
              <dd>{{ project["name"] }}</dd>
            </dl>
            <dl class="flex align-center">
              <dt>日付</dt>
              <dd>{{ currentEndDate }}</dd>
            </dl>
            <dl class="flex align-center">
              <dd>下記の通り{{ invoiceType.substring(0, 3) }}申し上げます</dd>
            </dl>
            <dl class="total-wrapper flex justify-space-between align-center">
              <dt class="total-text">{{ invoiceType.substring(0, 3) }}金額</dt>
              <dd class="total-text text-right price-format">
                {{ parseInt(project["tasks_total"]) + parseInt(project["tax"]) }}
              </dd>
            </dl>
          </div>
          <div class="header-right flex justify-space-between column-2-space">
            <div class="brand-wrapper">
              <h2 class="company-name">reactive design <span class="sub-text block">株式会社リアクティブデザイン</span></h2>
              <p class="full-address">
                <span class="post-code block">〒550-0002</span>
                <span class="address block">大阪府大阪市西区江戸堀1‑22‑17</span>
                <span class="building block">西船場辰巳ビル3F</span>
              </p>
              <p class="contact">
                <span class="tel block">TEL: 06-6225-7444</span>
                <span class="fax block">FAX: 06-6225-7445</span>
                <span class="fax block">登録番号: T4120001146495</span>
              </p>
            </div>
            <div class="image-wrapper flex align-center">
              <img src="../assets/images/sign.png" alt="reactive design sign">
            </div>
          </div>
        </div>

        <table class="invoice-body">
          <thead>
          <tr>
            <th class="name">項目</th>
            <th class="count">数量</th>
            <th class="kind">単位</th>
            <th class="price">単価</th>
            <th class="price last">金額</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="task in project['tasks']" :key="task['id']">
            <td class="name relative">
            <span v-if="!task['task_price'] || !task['task_kind'] || !task['task_count']"
                  @click="pushToAsana(task['permalink'])"
                  class="alert absolute flex align-center justify-center">!</span>
              <span class="name-text block">{{ task["task_name"] }}</span>
              <span class="date-text block">{{ ufn_invoice_date_formatter(task["task_invoice_date"]) }}</span></td>
            <td class="count">{{ task["task_count"] }}</td>
            <td class="kind">{{ task["task_kind"] }}</td>
            <td class="price price-format">{{ task["task_price"] }}</td>
            <td class="price last price-format relative">
              {{ task["task_total_price"] }}
              <span v-if="!task['task_price'] || !task['task_kind'] || !task['task_count']"
                    @click="removeTaskFromList(task['id'])"
                    class="remove-task pointer flex align-center absolute">
              <img src="../assets/svg/close.svg" alt="remove">
            </span>
            </td>
          </tr>
          </tbody>
          <tfoot>
          <tr>
            <td class="name"></td>
            <td class="text" colspan="3">小計</td>
            <td class="price last price-format">{{ project["tasks_total"] }}</td>
          </tr>
          <tr>
            <td class="name"></td>
            <td class="text" colspan="3">消費税 (10%)</td>
            <td class="price last price-format">{{ project["tax"] }}</td>
          </tr>
          <tr>
            <td class="name"></td>
            <td class="text" colspan="3">{{ invoiceType.substring(0, 3) }}金額</td>
            <td class="price last price-format">{{ parseInt(project["tasks_total"]) + parseInt(project["tax"]) }}</td>
          </tr>
          </tfoot>
        </table>
        <div class="invoice-footer"></div>
      </div>
    </div>
    <!--    <div class="flex justify-center" style="height: 100%;">-->
    <!--      <h5 class="text-center"-->
    <!--          style="color:#b2bec3; font-size: 1.2rem; font-weight: 400; margin-top: 30px">{{ currentEndDate.substring(0, 8) }}には <br> 本番公開になってるタスクが存在していない</h5>-->
    <!--    </div>-->


    <button @click="exportPDF(list)" class="export-all flex align-center">
      <img src="../assets/svg/pdf.svg" alt="pdf">
      <span class="text block text-left">全ての選択を <br> エクスポート</span>
    </button>
  </div>
</template>

<script>
import {watch, ref, computed, onMounted} from "vue";
import {useRoute, useRouter} from "vue-router"
import useStates from "@/helpers/useStates";
import usePdfBuilder from "@/helpers/pdf-builder/useMakePdf";
import {ufn_invoice_date_formatter, ufn_get_end_of_months} from "@/utils/ufn";
import {useToast} from "primevue/usetoast";
import Toast from 'primevue/toast'
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import MultiSelect from 'primevue/multiselect';
import InputNumber from "primevue/inputnumber"
import PageToolbar from "@/components/bars/PageToolBar";
import UseServices from "@/helpers/useServices";
import UseFormatter from "@/utils/UseFormatter";

export default {
  name: 'InvoiceList',
  components: {Toast, Button, Dropdown, MultiSelect, InputNumber, PageToolbar},
  setup() {
    const list = ref([])

    const services = new UseServices()
    const formatter = new UseFormatter()
    const toast = useToast();
    const router = useRouter()
    const route = useRoute()
    const {store, invoiceType, currentEndDate, currentEndDateIso, projects} = useStates()
    const year = ref(new Date().getFullYear())
    const {exportPDF} = usePdfBuilder()

    onMounted(() => {
      list.value = projects.value
    })

    watch(() => projects.value, val => {
      list.value = val
    })

    const changeYear = (bool) => {
      if (bool) {
        year.value = year.value + 1
        const ed = year.value + '年' + '12月' + '31日'
        router.replace({
          query: {
            start_date: year.value+"-01-01",
            end_date: year.value+"-01-31",
            tid: route.query.tid
          }
        }).finally(() => {
          store.commit("data/SET_CURRENT_END_DATE", ed)
          store.commit("data/SET_CURRENT_END_DATE_ISO", year.value+"-01-31")
          services.useCrud({
            action: "get",
            endpoint: "projects/",
            commit: "data/SET_PROJECTS",
          })
        })
      }
      else {
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

    const pushToAsana = (link) => {
      window.open(link)
    }
    const removeTaskFromList = (taskId) => {
      const data = projects.value.map((element) => {
        return {...element, tasks: element["tasks"].filter((subElement) => subElement["id"] !== taskId)}
      })
      store.commit("data/SET_PROJECTS", data)
    }

    const transferData = (projectIdx) => {

    }

    const editPage = (id, styles) => {
      list.value.forEach(item => {
        if (item.id === id){
          item.styles = styles
          item.styles.display = false
        }
      })
      toast.add({severity: 'info', summary: '更新', detail: 'PDFの新規サイズを確認してください', life: 3000});
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

    const setCurrentEndDateIso = computed({
      set(val) {
        console.log(val)
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
      year, invoiceType, setInvoiceType, currentEndDate, setCurrentEndDateIso, list, projects, setProjects,
      ufn_invoice_date_formatter, ufn_get_end_of_months,
      changeYear, pushToAsana, removeTaskFromList, editPage, transferData, exportPDF
    }
  }
}
</script>
<style>
#invoice-list {
  height: calc(100% - 46px);
}

#invoice-list > button.export-all {
  z-index: 101;
  position: fixed;
  right: 40px;
  bottom: 40px;
  width: 140px;
  height: 60px;
  background-color: #f1f1f1;
  box-shadow: rgba(149, 157, 165, 0.4) 0px 8px 24px;
}

#invoice-list > button.export-all > img {
  height: 50px;
}

#invoice-list > button.export-all > span.text {
}

#invoice-list .invoice {
  position: relative;
  height: auto;
  width: 755px;
  padding: 50px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  margin-bottom: 20px
}

#invoice-list .invoice.first {
  margin-top: 14px;
}

#invoice-list .invoice > .dev-buttons {
  position: absolute;
  top: 10px;
  right: 10px;
}

#invoice-list .invoice > .dev-buttons > button {
  width: 30px;
  height: 35px;
  border-bottom: 2px solid #ffffff;
}

#invoice-list .invoice > .dev-buttons > button:hover {
  border-bottom: 2px solid #2c3e50;
}

#invoice-list .invoice > .dev-buttons > button > img {
  width: 30px;
}

#invoice-list .invoice > .dev-buttons > button.edit {
  margin-right: 10px;
  margin-left: 13px;
}

#invoice-list .invoice > .dev-buttons > button.edit > img {
  width: 22px;
  padding-top: 2px;
}

#invoice-list .invoice > h3.invoice-type {
  font-weight: 300;
  font-size: 1.4rem;
  margin-bottom: 16px;
}

/* left header */
#invoice-list .invoice dl {
  width: 100%;
  font-size: .9rem;
  min-height: 30px;
  height: auto;
  border-bottom: 1px solid #e1e0e0;
}

#invoice-list .invoice dl.first {
  border-top: 1px solid #e1e0e0;
}

#invoice-list .invoice dl > dt {
  min-width: 50px;
}

#invoice-list .invoice dl > dd {
  width: calc(100% - 50px);
}

#invoice-list .invoice dl.total-wrapper {
  width: 200px;
  margin: 10px auto 0 auto;
  font-size: 1rem;
  border-bottom: 2px solid #000000;
}

#invoice-list .invoice dl > dt.total-text,
#invoice-list .invoice dl > dd.total-text {
  width: 100px;
}

/* right header */
#invoice-list .invoice h2.company-name {
  font-size: 1.1rem;
}

#invoice-list .invoice h2 > span.sub-text {
  font-size: .8rem;
  font-weight: 300;
}

#invoice-list .invoice p.full-address {
  margin-top: 10px;
}

#invoice-list .invoice p.full-address > span {
  font-size: .8rem;
  font-weight: 300;
}

#invoice-list .invoice p.contact {
  margin-top: 10px;
}

#invoice-list .invoice p.contact > span {
  font-size: .8rem;
  font-weight: 300;
}

#invoice-list .invoice .header-right > .brand-wrapper {
  width: calc(100% - 100px);
}

#invoice-list .invoice .header-right > .image-wrapper {
  width: 90px;
  height: 100%;
}

#invoice-list .invoice .header-right > .image-wrapper > img {
  width: 100%;
}

#invoice-list .invoice table.invoice-body {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

#invoice-list .invoice table.invoice-body th {
  font-weight: 400;
  height: 30px;
  font-size: .9rem;
  vertical-align: center;
  text-align: center;
  border-top: 1px solid #e1e0e0;
  border-bottom: 2px solid #000000;
  border-right: 1px solid #e1e0e0;
}

#invoice-list .invoice table.invoice-body th.name {
  width: calc(100% - 314px);
}

#invoice-list .invoice table.invoice-body th.count,
#invoice-list .invoice table.invoice-body th.kind {
  width: 57px;
  min-width: 57px;
}

#invoice-list .invoice table.invoice-body th.price {
  width: 100px;
}

#invoice-list .invoice table.invoice-body th.last {
  border-right: 0;
}

/* table body */
#invoice-list .invoice table.invoice-body td {
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

#invoice-list .invoice table.invoice-body td > span.name-text {
  width: calc(100% - 50px);
}

#invoice-list .invoice table.invoice-body td > span:last-child {
  position: absolute;
  top: 50%;
  right: 0;
  text-align: center;
  min-width: 50px;
  width: 50px;
  transform: translateY(-50%);
}

#invoice-list .invoice table.invoice-body td > span.alert {
  left: -30px;
  top: 50%;
  transform: translateY(-50%);
  width: 22px;
  padding-left: 1px;
  padding-bottom: 1px;
  height: 22px;
  border-radius: 50%;
  background-color: rgba(231, 76, 60, 0.9);
  color: #ffffff;
  font-weight: 600;
  cursor: pointer;
}

#invoice-list .invoice table.invoice-body td.count,
#invoice-list .invoice table.invoice-body td.kind,
#invoice-list .invoice table.invoice-body td.price {
  text-align: center;
}

#invoice-list .invoice table.invoice-body td.last {
  border-right: 0;
  text-align: right;
}

#invoice-list .invoice table.invoice-body td.last > span.remove-task {
  top: 50%;
  right: -62px;
  transform: translateY(-50%);
  height: 30px;
}

#invoice-list .invoice table.invoice-body td.last > span.remove-task img {
  width: 20px;
}

/* table footer */
#invoice-list .invoice table.invoice-body tfoot {
  border-top: 2px solid #000000;
}

#invoice-list .invoice table.invoice-body tfoot td.text {
  padding-left: 10px;
}


/* irregulars */
.inc-btn-color {
  background-color: #b2bec3 !important;
  border: 0 !important;
}

.bubble {
  z-index: 99;
  top: 40px;
  right: 24px;
  padding: 10px 14px 14px 14px;
  background-color: white;
  box-shadow: rgba(17, 17, 26, 0.05) 0px 4px 16px, rgba(17, 17, 26, 0.05) 0px 8px 32px;
}

.bubble > button.close {
  margin-left: auto;
}
.bubble > button.close > img {
  width: 20px;
  margin-bottom: 14px;
}

.bubble > button.submit {
  background-color: #6366F1;
  color: #ffffff;
  height: 30px;
}

.bubble .wrapper {
  margin-bottom: 10px;
}

.bubble .wrapper .p-button {
  border-radius: 0;
  width: 40px;
  height: 36px;
}

.bubble .wrapper .p-inputtext {
  outline: none;
  height: 36px;
  padding: 0 10px;
  width: 40px;
  text-align: center;
}
</style>
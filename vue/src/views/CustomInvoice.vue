<template>
  <div id="custom-invoice">
    <button @click="createInvoice(list)" class="create-invoice flex align-center">
      <img src="../assets/svg/invoice.svg" alt="pdf">
      <span class="text block text-left">新規見積を <br> 追加する</span>
    </button>

    <page-toolbar class="flex align-center justify-space-between">
      <div class="column-2"></div>
      <div class="right flex justify-end column-2">
        <div class="wrapper">
          <span class="label-title block">タイプ</span>
          <div class="dr1 wrapper flex">
            <Dropdown v-model="setInvoiceType" :options="['御見積書', '御請求書']" placeholder=""/>
          </div>
        </div>
        <div class="dr2 wrapper">
          <span class="label-title block">日付</span>
          <div class="wrapper flex">
            <Dropdown v-model="setCurrentEndDateIso" :options="ufn_get_end_of_months(year)" option-label="name"
                      option-value="value"/>
          </div>
        </div>
      </div>
    </page-toolbar>

    <div v-if="list.length" class="contents flex-column align-center overflow-y column-1"
         style="height: 100%; padding-bottom: 70px">
      <div class="invoice" :class="{first:idx===0}" v-for="(project, idx) in list" :key="project['id']">
        <div class="dev-buttons flex">
          <button class="edit relative" @click="project.styles.display = true">
            <img src="../assets/svg/text-edit.svg" alt="edit">
          </button>
          <button class="export" @click="exportPDF([project])"><img src="../assets/svg/pdf.svg" alt="pdf"></button>
          <div v-if="project.styles.display" class="bubble absolute flex-column">
            <button @click="project.styles.display = false" class="close"><img src="../assets/svg/close.svg" alt="">
            </button>
            <div class="wrapper flex-column">
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
            <dl class="flex first align-center" @mouseenter="onHover($event, true)"
                @mouseleave="onHover($event, false)">
              <dt>宛先</dt>
              <dd>
                <span class="block">{{ project["company_name"] }}</span>
                <InputText v-model="project.company_name"></InputText>
              </dd>
            </dl>
            <dl class="flex align-center" @mouseenter="onHover($event, true)" @mouseleave="onHover($event, false)">
              <dt>件名</dt>
              <dd>
                <span class="block">{{ project["name"] }}</span>
                <InputText v-model="project.name"></InputText>
              </dd>
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
              <dd v-if="project.tasks_total && project.tax" class="total-text text-right price-format">
                {{ parseInt(project["tasks_total"]) + parseInt(project["tax"]) }}
              </dd>
              <dd v-else class="total-text text-right price-format">0</dd>
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
          <tr v-for="(task, tIdx) in project['tasks']" :key="tIdx">
            <td class="name relative">
            <span v-if="!task['task_price'] || !task['task_kind'] || !task['task_count']"
                  class="alert absolute flex align-center justify-center">!</span>
              <span class="name-text block">{{ task["task_name"] }}</span>
              <span class="date-text block">{{ ufn_invoice_date_formatter(task["task_invoice_date"]) }}</span></td>
            <td class="count">{{ task["task_count"] }}</td>
            <td class="kind">{{ task["task_kind"] }}</td>
            <td class="price price-format">{{ task["task_price"] }}</td>
            <td class="price last price-format relative">
              {{ task["task_total_price"] }}
              <span v-if="!task['task_price'] || !task['task_kind'] || !task['task_count']"
                    @click="removeTaskFromList(idx, tIdx)"
                    class="remove-task pointer flex align-center absolute">
              <img src="../assets/svg/close.svg" alt="remove">
            </span>
            </td>
          </tr>

          <tr class="new-task">
            <td class="name relative"></td>
            <td class="count"></td>
            <td class="kind"></td>
            <td class="price price-format"></td>
            <td class="price last relative">
              <button @click="display=true, projectId=idx"><img src="../assets/svg/plus.svg" alt="new item"></button>
            </td>
          </tr>
          </tbody>

          <tfoot v-if="project.tasks_total && project.tax">
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

    <button @click="exportPDF(list)" class="export-all flex align-center">
      <img src="../assets/svg/pdf.svg" alt="pdf">
      <span class="text block text-left">全ての選択を <br> エクスポート</span>
    </button>

    <Dialog v-model:visible="display" :style="{width: '600px'}">
      <template #header>
        <h3>新規タスク</h3>
      </template>
      <form class="new-task-form">
        <div class="row">
          <div class="input-wrapper flex-column column-1">
            <label>タスク名</label>
            <InputText id="task_name" type="text" v-model="form.task_name"/>
          </div>
        </div>
        <div class="row flex justify-space-between column-1">
          <div class="input-wrapper flex-column column-4-space">
            <label>期日</label>
            <Calendar v-model="form.task_invoice_date" dateFormat="yy-mm-dd" />
          </div>
          <div class="input-wrapper flex-column column-4-space">
            <label>数量</label>
            <InputNumber v-model="form.task_count"/>
          </div>
          <div class="input-wrapper flex-column column-4-space">
            <label>単位 </label>
            <InputText id="task_count" type="text" v-model="form.task_kind"/>
          </div>
          <div class="input-wrapper flex-column column-4-space">
            <label>単価</label>
            <InputNumber v-model="form.task_price" mode="currency" currency="JPY" locale="jp-JP"/>
          </div>
        </div>
      </form>
      <template #footer>
        <div class="form-footer flex justify-end column-1">
          <button class="cancel form-btn flex align-center justify-center">中止</button>
          <button @click="createTask()" class="submit form-btn flex align-center justify-center">登録</button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script>
import {watch, ref, computed, onMounted, reactive} from "vue";
import UseServices from "@/helpers/useServices";
import {useRoute, useRouter} from "vue-router"
import useStates from "@/helpers/useStates";
import usePdfBuilder from "@/helpers/pdf-builder/useMakePdf";
import {ufn_invoice_date_formatter, ufn_get_end_of_months, ufn_sum_object_value} from "@/utils/ufn";
import PageToolbar from "@/components/bars/PageToolBar";
import Dropdown from 'primevue/dropdown';
import InputText from "primevue/inputtext"
import InputNumber from "primevue/inputnumber"
import UseFormatter from "@/utils/UseFormatter";
import Dialog from 'primevue/dialog';
import Calendar from 'primevue/calendar';


export default {
  name: "CustomInvoice",
  components: {Dropdown, InputText, InputNumber, Dialog, Calendar, PageToolbar},
  setup() {
    const list = ref([])
    const form = reactive({
      id: "",
      permalink: "",
      task_id: "",
      task_status: true,
      task_name: "",
      task_count: 0,
      task_kind: "",
      task_price: 0,
      task_total_price: 0,
      task_over: true,
      task_invoice_date: "",
      task_due_date: "",
    })
    const year = ref(new Date().getFullYear())
    const display = ref(false)
    const projectId = ref(null)
    const action = ref(false)
    const router = useRouter()
    const route = useRoute()
    const {store, invoiceType, currentEndDate, currentEndDateIso} = useStates()
    const services = new UseServices()
    const formatter = new UseFormatter()
    const {exportPDF} = usePdfBuilder()

    watch(() => action.value, val => {
      console.log(val)
    })

    watch(() => form, val => {
      console.log(val)
    })


    const createInvoice = () => {
      const project = {
        name: "",
        tasks: [],
        tasks_totals: 0,
        tax: 0,
        styles: {
          "display": false,
          "headerTitleFontSize": 15,
          "headerContentTextFontSize": 11,
          "headerBrandTextSize": 13,
          "bodyContentFontSize": 10
        }
      }

      list.value.push(project)
    }

    const onHover = (event, hover) => {
      if (hover) {
        event.target.children[1].firstChild.style.display = "none"
        event.target.children[1].lastChild.style.display = "block"
      } else {
        event.target.children[1].firstChild.style.display = "block"
        event.target.children[1].lastChild.style.display = "none"
      }
    }


    const createTask = () => {
      let project = list.value.find((item, idx) => {
        return idx === projectId.value
      })
      const dt = new Date(form.task_invoice_date)
      form.task_invoice_date = dt.toISOString().substring(0, 10)
      form.task_total_price = form.task_price * form.task_count
      project["tasks"].push(JSON.parse(JSON.stringify(form)))
      display.value = false
            form.id= ""
      form.permalink= ""
      form.task_id= ""
      form.task_status= true
      form.task_name= ""
      form.task_count= 0
      form.task_kind= ""
      form.task_price= 0
      form.task_total_price= 0
      form.task_over= true
      form.task_invoice_date= ""
      form.task_due_date= ""
      project.tasks_total = ufn_sum_object_value(project["tasks"], "task_total_price")
      project.tax = (10 * project["tasks_total"]) / 100
      formatter.priceFormatter
    }

    const removeTaskFromList = (pIdx, tIdx) => {
      const data = list.value.map((element, i) => {
        return {...element, tasks: element["tasks"].filter((subElement, idx) => i !== pIdx && idx !== tIdx)}
      })
      store.commit("data/SET_PROJECTS", data)
    }

    const editPage = (id, styles) => {
      list.value.forEach(item => {
        if (item.id === id) {
          item.styles = styles
          item.styles.display = false
        }
      })
      toast.add({severity: 'info', summary: '更新', detail: 'PDFの新規サイズを確認してください', life: 3000});
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
      list,
      form,
      year,
      display,
      projectId,
      action,
      invoiceType,
      setInvoiceType,
      currentEndDate,
      currentEndDateIso,
      setCurrentEndDateIso,
      ufn_invoice_date_formatter,
      ufn_get_end_of_months,
      createInvoice,
      createTask,
      exportPDF,
      editPage,
      removeTaskFromList,
      onHover,
    }
  }
}
</script>

<style>

#custom-invoice {
  height: calc(100% - 46px);
}

#custom-invoice > button.create-invoice {
  z-index: 101;
  position: fixed;
  top: 150px;
  right: 40px;
  width: 140px;
  height: 60px;
  padding-left: 10px;
  background-color: #f1f1f1;
  box-shadow: rgba(149, 157, 165, 0.4) 0px 8px 24px;
}

#custom-invoice > button.export-all {
  z-index: 101;
  position: fixed;
  right: 40px;
  bottom: 40px;
  width: 140px;
  height: 60px;
  background-color: #f1f1f1;
  box-shadow: rgba(149, 157, 165, 0.4) 0px 8px 24px;
}

#custom-invoice > button.create-invoice > img {
  height: 40px;
  margin-right: 10px;
}

#custom-invoice > button.export-all > img {
  height: 50px;
}

#custom-invoice .invoice {
  position: relative;
  height: auto;
  width: 755px;
  padding: 50px;
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
  margin-bottom: 20px
}

#custom-invoice .invoice.first {
  margin-top: 14px;
}

#custom-invoice .invoice > .dev-buttons {
  position: absolute;
  top: 10px;
  right: 10px;
}

#custom-invoice .invoice > .dev-buttons > button {
  width: 30px;
  height: 35px;
  border-bottom: 2px solid #ffffff;
}

#custom-invoice .invoice > .dev-buttons > button:hover {
  border-bottom: 2px solid #2c3e50;
}

#custom-invoice .invoice > .dev-buttons > button > img {
  width: 30px;
}

#custom-invoice .invoice > .dev-buttons > button.edit {
  margin-right: 10px;
  margin-left: 13px;
}

#custom-invoice .invoice > .dev-buttons > button.edit > img {
  width: 22px;
  padding-top: 2px;
}

#custom-invoice .invoice > h3.invoice-type {
  font-weight: 300;
  font-size: 1.4rem;
  margin-bottom: 16px;
}

/* left header */
#custom-invoice .invoice dl {
  width: 100%;
  font-size: .9rem;
  min-height: 30px;
  height: auto;
  border-bottom: 1px solid #e1e0e0;
}

#custom-invoice .invoice dl.first {
  border-top: 1px solid #e1e0e0;
}

#custom-invoice .invoice dl > dt {
  min-width: 50px;
}

#custom-invoice .invoice dl > dd {
  width: calc(100% - 50px);
}

#custom-invoice .invoice dl.total-wrapper {
  width: 200px;
  margin: 10px auto 0 auto;
  font-size: 1rem;
  border-bottom: 2px solid #000000;
}

#custom-invoice .invoice dl > dt.total-text,
#custom-invoice .invoice dl > dd.total-text {
  width: 100px;
}

/* right header */
#custom-invoice .invoice h2.company-name {
  font-size: 1.1rem;
}

#custom-invoice .invoice h2 > span.sub-text {
  font-size: .8rem;
  font-weight: 300;
}

#custom-invoice .invoice p.full-address {
  margin-top: 10px;
}

#custom-invoice .invoice p.full-address > span {
  font-size: .8rem;
  font-weight: 300;
}

#custom-invoice .invoice p.contact {
  margin-top: 10px;
}

#custom-invoice .invoice p.contact > span {
  font-size: .8rem;
  font-weight: 300;
}

#custom-invoice .invoice .header-right > .brand-wrapper {
  width: calc(100% - 100px);
}

#custom-invoice .invoice .header-right > .image-wrapper {
  width: 90px;
  height: 100%;
}

#custom-invoice .invoice .header-right > .image-wrapper > img {
  width: 100%;
}

#custom-invoice .invoice table.invoice-body {
  width: 100%;
  margin-top: 20px;
  border-collapse: collapse;
}

#custom-invoice .invoice table.invoice-body th {
  font-weight: 400;
  height: 30px;
  font-size: .9rem;
  vertical-align: center;
  text-align: center;
  border-top: 1px solid #e1e0e0;
  border-bottom: 2px solid #000000;
  border-right: 1px solid #e1e0e0;
}

#custom-invoice .invoice table.invoice-body th.name {
  width: calc(100% - 314px);
}

#custom-invoice .invoice table.invoice-body th.count,
#custom-invoice .invoice table.invoice-body th.kind {
  width: 57px;
  min-width: 57px;
}

#custom-invoice .invoice table.invoice-body th.price {
  width: 100px;
}

#custom-invoice .invoice table.invoice-body th.last {
  border-right: 0;
}

/* table body */
#custom-invoice .invoice table.invoice-body td {
  font-weight: 400;
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

#custom-invoice .invoice table.invoice-body tr.new-task > td {
  padding: 14px 0;
}

#custom-invoice .invoice table.invoice-body tr.new-task > td.price:last-child > button {
  position: absolute;
  width: 20px;
  height: 20px;
  top: 50%;
  transform: translateY(-50%);
  right: -24px;
}

#custom-invoice .invoice table.invoice-body tr.new-task > td.price:last-child > button > img {
  width: 18px;
}


#custom-invoice .invoice table.invoice-body td > span.name-text {
  width: calc(100% - 50px);
}

#custom-invoice .invoice table.invoice-body td > span:last-child {
  position: absolute;
  top: 50%;
  right: 0;
  text-align: center;
  min-width: 50px;
  width: 50px;
  transform: translateY(-50%);
}

#custom-invoice .invoice table.invoice-body td > span.alert {
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

#custom-invoice .invoice table.invoice-body td.count,
#custom-invoice .invoice table.invoice-body td.kind,
#custom-invoice .invoice table.invoice-body td.price {
  text-align: center;
}

#custom-invoice .invoice table.invoice-body td.last {
  border-right: 0;
  text-align: right;
}

#custom-invoice .invoice table.invoice-body td.last > span.remove-task {
  top: 50%;
  right: -62px;
  transform: translateY(-50%);
  height: 30px;
}

#custom-invoice .invoice table.invoice-body td.last > span.remove-task img {
  width: 20px;
}

/* table footer */
#custom-invoice .invoice table.invoice-body tfoot {
  border-top: 2px solid #000000;
}

#custom-invoice .invoice table.invoice-body tfoot td.text {
  padding-left: 10px;
}

/* irregulars*/
#custom-invoice .contents .p-inputtext {
  width: 90%;
  border-radius: 0;
  height: 20px;
  font-size: .8rem;
  display: none;
}

</style>
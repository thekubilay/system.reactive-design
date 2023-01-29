import useStates from "@/helpers/useStates";
import UseInvoiceBuilder from "./UseInvoiceBuilder"
import UseTotalsBuilder from "./UseTotalsBuilder"
import pdfMake from "pdfmake/build/pdfmake";
import pdfFonts from "pdfmake/build/vfs_fonts";

export default function () {
  const {team, teams, invoiceType, currentEndDate} = useStates()

  pdfMake.vfs = pdfFonts.pdfMake.vfs;
  pdfMake.fonts = {
    noto: {
      thin: "NotoSansJP-Thin.otf",
      normal: "NotoSansJP-Regular.otf",
      medium: "NotoSansJP-Medium.otf",
    }
  };


  const exportPDF = (data, pdfType = null, taxType = null) => {
    if (!pdfType) {
      const TEAM = teams.value.find(item => {
        return item.tid === parseFloat(team.value)
      })

      const builders = new UseInvoiceBuilder(data, invoiceType, currentEndDate, TEAM["setting"])
      const documents = builders.invoice
      const pages = {
        content: documents,
        defaultStyle: {
          font: "noto",
        },
      }
      if (data.length === 1) {
        const name = data[0].name
        pdfMake.createPdf(pages).download(name + ".pdf");
      } else {
        pdfMake.createPdf(pages).download(invoiceType.value + "-" + currentEndDate.value + ".pdf");
      }
    } else {
      const TEAM = teams.value.find(item => {
        return item.tid === parseFloat(team.value)
      })
      const builders = new UseTotalsBuilder(data, team.value.full_name, currentEndDate.value, invoiceType.value, TEAM["setting"], taxType)
      const documents = builders.totals
      const pages = {
        content: documents,
        defaultStyle: {
          font: "noto",
        },
      }
      const name = taxType ? "合計表（税込）" : "合計表（税抜）"
      pdfMake.createPdf(pages).download(name + ".pdf");

    }
  }
  return {
    exportPDF,
  }
}
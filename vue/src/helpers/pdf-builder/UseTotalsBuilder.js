import {ufn_price_formatter, ufn_sum_object_value} from "@/utils/ufn";

export default class UseTotalsBuilder {
  constructor(data, company_name, date, type, setting, taxType) {
    this.data = data
    this.company_name = company_name
    this.type = type
    this.date = date.substring(5, 7) + "月"
    this.setting = setting
    this.taxType = taxType
  }

  get totals() {
    let contents = []

    const header1 = this.setHeader().h1
    const header2 = this.setHeader().h2
    const body = this.setBody()
    const footer = this.setFooter()

    const information = this.setBankInformation()

    if (this.type === "御請求書") {
      contents.push(header1, header2, body, footer, information)
    } else {
      contents.push(header1, header2, body, footer)
    }
    return contents
  }

  getPrice(total, tax) {
    let price = 0
    if (this.taxType) {
      price = parseInt(total) + parseInt(tax);
    } else {
      price = parseInt(total);
    }

    return price
  }

  getSumPrice() {
    const to = ufn_sum_object_value(this.data, "tasks_total")
    const ta = ufn_sum_object_value(this.data, "tax")
    return {
      totals: to,
      taxes: ta,
      totalsWithTax: to + ta
    }
  }

  setHeader() {
    return {
      h1: {text: this.company_name, fontSize: 12, margin: [0, 0, 0, 5]},
      h2: {text: this.date + " " + this.type, fontSize: 26, margin: [0, 0, 0, 10]}
    }
  }

  setBody() {
    let rows = []
    const th = [
      {
        text: "物件名",
        border: [false, true, true, true],
        alignment: "center",
        fontSize: 10
      },
      {
        text: "金額",
        border: [true, true, false, true],
        alignment: "center",
        fontSize: 10,
      },
    ]

    rows.push(th)

    this.data.forEach(project => {
      const cols = [
        {
          text: project.name,
          border: [false, true, true, true],
          alignment: "left",
          fontSize: 10
        },
        {
          text: ufn_price_formatter(this.getPrice(project["tasks_total"], project["tax"])),
          border: [true, true, false, true],
          alignment: "right",
          fontSize: 10
        },
      ]


      rows.push(cols)
    });

    return {
      table: {
        headerRows: 1,
        widths: [400, 100],
        body: rows
      },
      layout: {
        hLineWidth: function (i, node) {
          return (i === 1) ? 2 : 1;
        },
        hLineColor: function (i, node) {
          return (i === 1) ? 'black' : '#dcdde1';
        },
        vLineColor: function (i, node) {
          return (i === 0 || i === node.table.widths.length) ? '#dcdde1' : '#dcdde1';
        },
      },
      margin: [0, 15, 0, 0],
    }
  }

  setFooter() {
    const rows = {
      table: {
        headerRows: 1,
        widths: [400, 100],
        body: []
      },
      layout: {
        hLineWidth: function (i, node) {
          return (i === 0) ? 2 : 1;
        },
        hLineColor: function (i, node) {
          return (i === 0) ? 'black' : '#dcdde1';
        },
        vLineColor: function (i, node) {
          return (i === 0 || i === node.table.widths.length) ? '#dcdde1' : '#dcdde1';
        },
      },
    }


    const withoutTax = [
      {
        text: "小計",
        border: [false, true, true, true],
        alignment: "left",
        fontSize: 10
      },
      {
        text: ufn_price_formatter(this.getSumPrice().totals),
        border: [true, true, false, true],
        alignment: "right",
        fontSize: 10
      },
    ]
    const tax = [
      {
        text: "消費税 (10%)",
        border: [false, true, true, true],
        alignment: "left",
        fontSize: 10
      },
      {
        text: ufn_price_formatter(this.getSumPrice().taxes),
        border: [true, true, false, true],
        alignment: "right",
        fontSize: 10
      },
    ]

    if (!this.taxType) {
      rows.table.body.push(withoutTax, tax)
    }

    const totalWithTax = [
      {
        text: "合計金額",
        border: [false, true, true, true],
        alignment: "left",
        fontSize: 10
      },
      {
        text: ufn_price_formatter(this.getSumPrice().totalsWithTax),
        border: [true, true, false, true],
        alignment: "right",
        fontSize: 18
      },
    ]
    rows.table.body.push(totalWithTax)

    return rows
  }

  setBankInformation() {
    return {
      table: {
        widths: [420],
        body: [
          [
            {
              text: this.setting.invoice_text1,
              fontSize: 9, alignment: 'left',
              paddingTop: 2,
              paddingBottom: 2,
              border: [false, false, false, false],
            },
          ],
          [
            {
              text: this.setting.invoice_text2,
              fontSize: 9, alignment: 'left',
              paddingTop: 2,
              paddingBottom: 2,
              border: [false, false, false, false],

            },
          ],
          [
            {
              text: this.setting.invoice_text3,
              fontSize: 9, alignment: 'left',
              paddingTop: 2,
              paddingBottom: 2,
            }
          ],
        ],
      },
      layout: {
        defaultBorder: false,
        paddingTop: function (i, node) {
          return 0;
        },
        paddingBottom: function (i, node) {
          return 0;
        },
      },
      margin: [0, 25, 0, 0],

    }
  }
}
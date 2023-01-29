export default class UseFormatter {
  get priceFormatter() {
    return this.setCurrency()
  }

  setCurrency() {
    setTimeout(() => {
      const price_elements = document.querySelectorAll(".price-format")
      if (price_elements) {
        price_elements.forEach(item => {
          const price = parseInt(item.innerText)
          if (price)
            item.innerHTML = price.toLocaleString("ja-JP", {style: "currency", currency: "JPY"})
        })
      }
    }, 1000)
  }
}
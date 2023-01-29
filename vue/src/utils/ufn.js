export const ufn_price_formatter = (num) => {
  /* yen currency formatter with regex */
  if (num !== null) {
    let numer = num.toString();
    let num_parts = numer.split(".");
    num_parts = num_parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return "¥ " + num_parts;
  }
}

export const ufn_invoice_date_formatter = (date) => {
  const month = date.substring(5, 7)
  const day = date.substring(8, 10)
  return month + "/" + day
}

export const ufn_sum_object_value = (array, value) => {
  let sum = 0;
  array.forEach(item => {
    sum += parseInt(item[value]) ?? 0;
  });
  return sum;
}

export const ufn_get_end_of_months = (year) => {
  let months = []
  for (let i = 0; i < 12; i++) {
    const d = new Date(year, i + 1, 1);
    const dateObj = {name:d.toISOString().substring(0,7), value:d.toISOString().substring(0,10)}
    months.push(dateObj)
  }
  return months
}
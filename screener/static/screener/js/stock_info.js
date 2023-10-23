/** @type {HTMLElement} */
const stock_change_value_element = document.querySelector('[data-field="stock_change_value"]')
/** @type {HTMLElement} */
const stock_change_percent_element = document.querySelector('[data-field="stock_change_percent"]')

if (stock_change_value_element.innerHTML.includes("+")) {
  stock_change_value_element.style.color = "#007560"
  stock_change_percent_element.style.color = "#007560"
} else if (stock_change_value_element.innerHTML.includes("-")) {
  stock_change_value_element.style.color = "#d60a22"
  stock_change_percent_element.style.color = "#d60a22"
} 
else {
  stock_change_value_element.style.color = "#5b636a"
  stock_change_percent_element.style.color = "#5b636a"
}

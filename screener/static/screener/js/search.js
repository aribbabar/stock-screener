/**
 *
 * @param {KeyboardEvent} e
 */
function search(e) {
  const search_input = e.target.value;
  const url = `${window.location.href}search/${search_input}`;

  /** @type {HTMLUListElement} */
  const search_results_list_element = document.querySelector(
    ".search-results-list"
  );
  search_results_list_element.style.display = "flex"

  for (const child of Array.from(search_results_list_element.children)) {
    child.remove();
  }

  if (!search_input) {
    return;
  }

  fetch(url)
    .then((res) => {
      if (res.ok) return res.json();
    })
    .then((json) => {
      /** @type {string[]} */
      const search_results_list = json["data"];

      for (let i = 0; i < search_results_list.length; i++) {
        const search_result = search_results_list[i];

        const li_wrapper_element = document.createElement("li");

        const line_break = document.createElement("div");
        line_break.classList.add("line-break");

        const btn_element = document.createElement("button");
        btn_element.type = "submit";
        btn_element.innerText = `${search_result.substring(0, 25)}...`;

        li_wrapper_element.appendChild(btn_element);

        search_results_list_element.appendChild(li_wrapper_element);

        // To avoid putting in the line at the end of the box
        if (i < search_results_list.length - 1)
          search_results_list_element.appendChild(line_break);
      }

      if (search_results_list.length === 0) {
        search_results_list_element.style.display = "None"
      }
    })
    .catch((err) => {});
}

document.querySelector("form").addEventListener("submit", (e) => {
  e.preventDefault();

  const stock = e.submitter.innerText;
  const symbol = /[^|]*/.exec(stock)[0].trim();

  const url = `${window.location.href}stock_info/${symbol}`;

  window.location.href = url
});

"use strict";
let table = document.getElementById("table");
let columns = ["name", "last_modified", "size"];
let column_compare = {
  'name': (a, b) => (a.localeCompare(b, undefined, {'sensitivity': 'base'})),
  'last_modified': (a, b) => (Date.parse(a) - Date.parse(b)),
  'size': (a, b) => (Number.parseInt(a) - Number.parseInt(b)),
}
let column_positions = {};
let column_state = {};

function sort_column(name, reverse) {
  let data = []

  let index = 0;
  let tbody = table.querySelector("tbody");
  tbody.querySelectorAll("tr").forEach(row => {
    let attribute = row.children[column_positions[name]].getAttribute("data-sort");
    data.push({'row': row, 'value': attribute});
    index++;
  });
  data.sort((a, b) => column_compare[name](a['value'], b['value']));

  if (reverse) {
    data.reverse();
  }

  index = 0;
  data.forEach(elm => {
    tbody.appendChild(elm['row']);
  });
}

columns.forEach(colname => {
  let col_header = document.getElementById(colname + "_header");
  column_positions[colname] = col_header.cellIndex;
  column_state[colname] = null;
  let sort_button_down = document.createElement("button");
  sort_button_down.setAttribute("type", "button");
  sort_button_down.append("↓");
  sort_button_down.addEventListener("click", (_e) => {sort_column(colname, false)});
  col_header.appendChild(sort_button_down);
  let sort_button_up = document.createElement("button");
  sort_button_up.setAttribute("type", "button");
  sort_button_up.append("↑");
  sort_button_up.addEventListener("click", (_e) => {sort_column(colname, true)});
  col_header.appendChild(sort_button_up);
});

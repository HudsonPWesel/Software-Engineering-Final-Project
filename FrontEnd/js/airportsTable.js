// js/airportsTable.js

// URL of the airports JSON file
const DATA_URL = "http://127.0.0.1:5500/JSONs/airports.json";

// ID of the div where the table will be rendered
const ROOT_ID = "airports-root";

// Columns to display in the table
const COLS = [
  "ident", "name", "type", "municipality",
  "iso_region", "iso_country", "iata_code", "icao_code",
  "latitude_deg", "longitude_deg", "elevation_ft"
];

// Fetch the JSON data from the server
fetch(DATA_URL)
  .then((r) => {
    // Ensure the request succeeded
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return r.json();
  })
  .then((data) => {
    // Convert the object of airports into an array
    const rows = Object.values(data);

    // Get the table mount point
    const root = document.getElementById(ROOT_ID);
    if (!root) return;

   
    const head = `<tr>${COLS.map(c => `<th>${c}</th>`).join("")}</tr>`;
    const body = rows.map((a) =>
      `<tr>${COLS.map(c => `<td>${a?.[c] ?? ""}</td>`).join("")}</tr>`
    ).join("");

    // Inject the table into the page
    root.innerHTML = `
      <table border="1" cellspacing="0" cellpadding="6">
        <thead>${head}</thead>
        <tbody>${body}</tbody>
      </table>
    `;
  })
  .catch((e) => {
    // Display an error message if the fetch fails
    const root = document.getElementById(ROOT_ID);
    if (root) root.textContent = `Failed to load airports: ${e.message}`;
    console.error(e);
  });

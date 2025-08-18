const CSV_URL = "https://raw.githubusercontent.com/Lupilgaming/consportdaysite/refs/heads/main/points.csv";


let rawData = [];
let filteredData = [];

document.addEventListener("DOMContentLoaded", () => {
  Papa.parse(CSV_URL, {
    download: true,
    header: true,
    complete: (results) => {
      rawData = results.data;
      populateActivityTypes();
      applyFilters();
    }
  });

  document.getElementById("theme-selector").addEventListener("change", (e) => {
    document.body.className = e.target.value + "-theme";
  });

  document.getElementById("start-date").addEventListener("change", applyFilters);
  document.getElementById("end-date").addEventListener("change", applyFilters);
  document.getElementById("activity-type-filter").addEventListener("change", applyFilters);
});

function populateActivityTypes() {
  const types = [...new Set(rawData.map(d => d.activitytype))];
  const select = document.getElementById("activity-type-filter");
  types.forEach(type => {
    const option = document.createElement("option");
    option.value = type;
    option.textContent = type;
    select.appendChild(option);
  });
}

function applyFilters() {
  const startDate = new Date(document.getElementById("start-date").value);
  const endDate = new Date(document.getElementById("end-date").value);
  const activityType = document.getElementById("activity-type-filter").value;

  filteredData = rawData.filter(d => {
    const date = new Date(d.datetime);
    const inDateRange = (!isNaN(startDate) ? date >= startDate : true) &&
                        (!isNaN(endDate) ? date <= endDate : true);
    const matchesType = activityType === "all" || d.activitytype === activityType;
    return inDateRange && matchesType;
  });

  renderLeaderboard();
  renderCharts();
}
function renderLeaderboard() {
    const leaderboard = {};
    filteredData.forEach(d => {
      const name = d.athletename;
      const points = parseFloat(d.points) || 0;
      leaderboard[name] = (leaderboard[name] || 0) + points;
    });
  
    const sorted = Object.entries(leaderboard)
      .sort((a, b) => b[1] - a[1]);
  
    const tbody = document.querySelector("#leaderboard tbody");
    tbody.innerHTML = "";
  
    sorted.forEach(([name, points], index) => {
      let rank = index + 1;
      let flair = "";
  
      if (rank === 1) flair = "🥇";
      else if (rank === 2) flair = "🥈";
      else if (rank === 3) flair = "🥉";
  
      const row = `<tr>
        <td>#${rank} ${flair}</td>
        <td>${name}</td>
        <td>${points.toFixed(2)}</td>
      </tr>`;
      tbody.innerHTML += row;
    });
  }
  
  

function renderCharts() {
  const avgPoints = {};
  const totalPoints = {};
  const counts = {};

  filteredData.forEach(d => {
    const type = d.activitytype;
    const points = parseFloat(d.points) || 0;
    totalPoints[type] = (totalPoints[type] || 0) + points;
    counts[type] = (counts[type] || 0) + 1;
  });

  Object.keys(totalPoints).forEach(type => {
    avgPoints[type] = totalPoints[type] / counts[type];
  });

  drawBarChart("#avg-points-chart", avgPoints, "Average Points");
  drawBarChart("#total-points-chart", totalPoints, "Total Points");
}

function drawBarChart(containerId, data, label) {
  const container = d3.select(containerId);
  container.selectAll("*").remove();

  const width = 500;
  const height = 300;
  const margin = { top: 20, right: 20, bottom: 50, left: 60 };

  const svg = container.append("svg")
    .attr("width", width)
    .attr("height", height);

  const x = d3.scaleBand()
    .domain(Object.keys(data))
    .range([margin.left, width - margin.right])
    .padding(0.2);

  const y = d3.scaleLinear()
    .domain([0, d3.max(Object.values(data))])
    .nice()
    .range([height - margin.bottom, margin.top]);

  svg.append("g")
    .selectAll("rect")
    .data(Object.entries(data))
    .join("rect")
    .attr("x", d => x(d[0]))
    .attr("y", d => y(d[1]))
    .attr("height", d => y(0) - y(d[1]))
    .attr("width", x.bandwidth())
    .attr("fill", "#0077cc");

  svg.append("g")
    .attr("transform", `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(x));

  svg.append("g")
    .attr("transform", `translate(${margin.left},0)`)
    .call(d3.axisLeft(y));
}

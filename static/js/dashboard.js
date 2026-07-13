// =========================================
// GLOBAL VARIABLES
// =========================================

let dashboardData = {};

let vendorChart = null;
let categoryChart = null;

let monthlyChart = null;
let matchedChart = null;
let receivedChart = null;

let buyerChart = null;

if (buyerChart) {
  buyerChart.destroy();
}

let predictionChart = null;
let anomalyChart = null;

// =========================================
// APPLICATION START
// =========================================

document.addEventListener("DOMContentLoaded", () => {
  loadDashboard();
});

// =========================================
// LOAD DASHBOARD
// =========================================

async function loadDashboard() {
  try {
    const response = await fetch("/dashboard/data");

    if (!response.ok) {
      throw new Error("Failed to load dashboard data.");
    }

    dashboardData = await response.json();

    updateSummaryCards(dashboardData.summary);

    createVendorChart(dashboardData.vendors);

    createCategoryChart(dashboardData.categories);

    createMonthlyChart(dashboardData.monthlySpend);

    createMatchedChart(dashboardData.matchedStatus);

    createReceivedChart(dashboardData.receivedStatus);

    updateStatistics(dashboardData.statistics);

    createBuyerChart(dashboardData.buyers);

    renderRecentInvoices(dashboardData.recentInvoices);

    createPredictionChart(dashboardData.prediction);

    createAnomalyChart(dashboardData.anomaly);
  } catch (error) {
    console.error("Dashboard Error:", error);

    alert("Unable to load dashboard.");
  }
}

// =========================================
// SUMMARY CARDS
// =========================================

function updateSummaryCards(summary) {
  document.getElementById("totalInvoices").innerText = summary.totalInvoices;

  document.getElementById("totalSpend").innerText =
    "₹ " + Number(summary.totalSpend).toLocaleString();

  document.getElementById("totalVendors").innerText = summary.totalVendors;

  document.getElementById("totalPOs").innerText = summary.totalPOs;

  document.getElementById("duplicateInvoices").innerText =
    summary.duplicateInvoices;

  document.getElementById("averageInvoice").innerText =
    "₹ " + Number(summary.averageInvoice).toLocaleString();
}

// =========================================
// VENDOR CHART
// =========================================

function createVendorChart(vendors) {
  if (vendorChart) {
    vendorChart.destroy();
  }

  vendorChart = new Chart(
    document.getElementById("vendorChart"),

    {
      type: "bar",

      data: {
        labels: vendors.map((v) => v.vendor),

        datasets: [
          {
            label: "Total Spend (₹)",

            data: vendors.map((v) => v.amount),
          },
        ],
      },

      options: {
        responsive: true,

        indexAxis: "y",

        plugins: {
          legend: {
            display: false,
          },
        },
      },
    },
  );
}

// =========================================
// CATEGORY CHART
// =========================================

function createCategoryChart(categories) {
  if (categoryChart) {
    categoryChart.destroy();
  }

  categoryChart = new Chart(
    document.getElementById("categoryChart"),

    {
      type: "doughnut",

      data: {
        labels: categories.map((c) => c.category),

        datasets: [
          {
            data: categories.map((c) => c.amount),
          },
        ],
      },

      options: {
        responsive: true,
      },
    },
  );
}

// =========================================
// MONTHLY SPEND
// =========================================

function createMonthlyChart(monthlySpend) {
  if (monthlyChart) {
    monthlyChart.destroy();
  }

  monthlyChart = new Chart(
    document.getElementById("monthlyChart"),

    {
      type: "line",

      data: {
        labels: monthlySpend.map((m) => m.month),

        datasets: [
          {
            label: "Monthly Spend",

            data: monthlySpend.map((m) => m.amount),

            fill: false,

            tension: 0.3,
          },
        ],
      },

      options: {
        responsive: true,
      },
    },
  );
}

// =========================================
// MATCHED STATUS
// =========================================

function createMatchedChart(statusData) {
  if (matchedChart) {
    matchedChart.destroy();
  }

  matchedChart = new Chart(
    document.getElementById("matchedChart"),

    {
      type: "pie",

      data: {
        labels: statusData.map((s) => s.status),

        datasets: [
          {
            data: statusData.map((s) => s.count),
          },
        ],
      },

      options: {
        responsive: true,
      },
    },
  );
}

// =========================================
// RECEIVED STATUS
// =========================================

function createReceivedChart(statusData) {
  if (receivedChart) {
    receivedChart.destroy();
  }

  receivedChart = new Chart(
    document.getElementById("receivedChart"),

    {
      type: "pie",

      data: {
        labels: statusData.map((s) => s.status),

        datasets: [
          {
            data: statusData.map((s) => s.count),
          },
        ],
      },

      options: {
        responsive: true,
      },
    },
  );
}
// =========================================
// NUMPY STATISTICS
// =========================================

function updateStatistics(statistics) {
  document.getElementById("meanInvoice").innerText =
    "₹ " + statistics.mean.toLocaleString();

  document.getElementById("medianInvoice").innerText =
    "₹ " + statistics.median.toLocaleString();

  document.getElementById("stdInvoice").innerText =
    statistics.std.toLocaleString();

  document.getElementById("maxInvoice").innerText =
    "₹ " + statistics.maximum.toLocaleString();

  document.getElementById("minInvoice").innerText =
    "₹ " + statistics.minimum.toLocaleString();

  document.getElementById("percentile95").innerText =
    "₹ " + statistics.percentile95.toLocaleString();
}

function createBuyerChart(buyers) {
  new Chart(
    document.getElementById("buyerChart"),

    {
      type: "bar",

      data: {
        labels: buyers.map((b) => b.buyer),

        datasets: [
          {
            label: "Spend",

            data: buyers.map((b) => b.amount),
          },
        ],
      },
    },
  );
}

function createBuyerChart(buyers) {
  if (buyerChart) {
    buyerChart.destroy();
  }

  buyerChart = new Chart(
    document.getElementById("buyerChart"),

    {
      type: "bar",

      data: {
        labels: buyers.map((b) => b.buyer),

        datasets: [
          {
            label: "Buyer Spend",

            data: buyers.map((b) => b.amount),
          },
        ],
      },

      options: {
        responsive: true,

        plugins: {
          legend: {
            display: false,
          },
        },
      },
    },
  );
}
function renderRecentInvoices(invoices) {
  const tbody = document.getElementById("invoiceTable");

  tbody.innerHTML = "";

  if (invoices.length === 0) {
    tbody.innerHTML = `
        <tr>
            <td colspan="6" class="text-center">
                No invoices available
            </td>
        </tr>
    `;

    return;
  }

  invoices.forEach((inv) => {
    tbody.innerHTML += `

        <tr>

            <td>${inv.invoiceNo}</td>

            <td>${inv.vendor}</td>

            <td>${inv.category}</td>

            <td>₹ ${Number(inv.amount).toLocaleString()}</td>

            <td>${inv.status}</td>

            <td>${inv.date}</td>

        </tr>

        `;
  });
}

document
  .getElementById("refreshDashboard")
  .addEventListener("click", loadDashboard);
document.getElementById("lastUpdated").innerText =
  "Updated : " + new Date().toLocaleString();

function createPredictionChart(data) {
  if (predictionChart) {
    predictionChart.destroy();
  }

  predictionChart = new Chart(
    document.getElementById("predictionChart"),

    {
      type: "line",

      data: {
        labels: data.labels,

        datasets: [
          {
            label: "Actual Spend",

            data: data.actual,

            borderWidth: 3,

            tension: 0.4,
          },

          {
            label: "Predicted Spend",

            data: data.predicted,

            borderWidth: 3,

            borderDash: [10, 5],

            tension: 0.4,
          },
        ],
      },

      options: {
        responsive: true,

        plugins: {
          legend: {
            position: "bottom",
          },
        },
      },
    },
  );
}
function createAnomalyChart(data) {
  if (anomalyChart) {
    anomalyChart.destroy();
  }

  anomalyChart = new Chart(
    document.getElementById("anomalyChart"),

    {
      type: "bar",

      data: {
        labels: data.labels,

        datasets: [
          {
            label: "Invoice Amount",

            data: data.amounts,

            backgroundColor: "#ef4444",

            borderRadius: 6,
          },
        ],
      },

      options: {
        responsive: true,

        indexAxis: "y",

        plugins: {
          legend: {
            display: false,
          },

          tooltip: {
            callbacks: {
              afterLabel: function (context) {
                return "Vendor : " + data.vendors[context.dataIndex];
              },
            },
          },
        },
      },
    },
  );
}


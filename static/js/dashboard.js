// =========================================
// GLOBAL VARIABLES
// =========================================

let allInvoices = [];

let supplierChart = null;
let categoryChart = null;
let agingChart = null;
let riskChart = null;

// =========================================
// START APPLICATION
// =========================================

document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
});



// =========================================
// LOAD DASHBOARD DATA
// =========================================

async function loadDashboard() {

    try {

        const response = await fetch("/dashboard-data");

        allInvoices = await response.json();

        populateFilters(allInvoices);

        renderDashboard(allInvoices);

        attachEvents();

    } catch (error) {

        console.error("Dashboard Load Error:", error);

    }

}


// =========================================
// RENDER DASHBOARD
// =========================================

function renderDashboard(invoices) {

    updateKPIs(invoices);

    createSupplierChart(invoices);

    createCategoryChart(invoices);

    createAgingChart(invoices);

    createRiskChart(invoices);

    renderInvoiceTable(invoices);

}


// =========================================
// KPI
// =========================================

function updateKPIs(invoices) {

    const totalInvoices = invoices.length;

    const matchedPosted =
        invoices.filter(i => i.status === "Matched").length;

    const pendingApproval =
        invoices.filter(i => i.approval === "Pending").length;

    const exceptions =
        invoices.filter(i => i.exception).length;

    const duplicates =
        invoices.filter(i => i.duplicate).length;

    const totalValue =
        invoices.reduce((sum, i) => sum + i.amount, 0);

    document.getElementById("totalInvoices").innerText =
        totalInvoices;

    document.getElementById("matchedPosted").innerText =
        matchedPosted;

    document.getElementById("pendingApproval").innerText =
        pendingApproval;

    document.getElementById("exceptions").innerText =
        exceptions;

    document.getElementById("duplicates").innerText =
        duplicates;

    document.getElementById("totalValue").innerText =
        "₹" + totalValue.toLocaleString();

}

// =========================================
// SUPPLIER CHART
// =========================================

function createSupplierChart(invoices) {

    if (supplierChart) {
        supplierChart.destroy();
    }

    const supplierTotals = {};

    invoices.forEach(inv => {

        supplierTotals[inv.supplier] =
            (supplierTotals[inv.supplier] || 0) + inv.amount;

    });

    supplierChart = new Chart(
        document.getElementById("supplierChart"),
        {
            type: "bar",

            data: {

                labels: Object.keys(supplierTotals),

                datasets: [{

                    label: "Invoice Value",

                    data: Object.values(supplierTotals),

                    backgroundColor: "#2563EB"

                }]

            },

            options: {

                responsive: true,

                indexAxis: "y",

                plugins: {

                    legend: {

                        display: false

                    }

                }

            }

        }

    );

}

// =========================================
// CATEGORY CHART
// =========================================

function createCategoryChart(invoices) {

    if (categoryChart) {
        categoryChart.destroy();
    }

    const categories = {};

    invoices.forEach(inv => {

        categories[inv.category] =
            (categories[inv.category] || 0) + 1;

    });

    categoryChart = new Chart(
        document.getElementById("categoryChart"),
        {

            type: "doughnut",

            data: {

                labels: Object.keys(categories),

                datasets: [{

                    data: Object.values(categories),

                    backgroundColor: [

                        "#2563EB",
                        "#16A34A",
                        "#F59E0B",
                        "#EF4444",
                        "#8B5CF6",
                        "#06B6D4"

                    ]

                }]

            },

            options: {

                responsive: true

            }

        }

    );

}

// =========================================
// AGING CHART
// =========================================

function createAgingChart(invoices) {

    if (agingChart) {
        agingChart.destroy();
    }

    const aging = {

        "0-7":0,
        "8-15":0,
        "16-30":0,
        "31-60":0,
        "60+":0

    };

    invoices.forEach(inv=>{

        if(inv.days<=7)

            aging["0-7"]++;

        else if(inv.days<=15)

            aging["8-15"]++;

        else if(inv.days<=30)

            aging["16-30"]++;

        else if(inv.days<=60)

            aging["31-60"]++;

        else

            aging["60+"]++;

    });

    agingChart = new Chart(

        document.getElementById("agingChart"),

        {

            type:"bar",

            data:{

                labels:Object.keys(aging),

                datasets:[{

                    label:"Invoices",

                    data:Object.values(aging),

                    backgroundColor:[
                        "#22C55E",
                        "#3B82F6",
                        "#FACC15",
                        "#F97316",
                        "#DC2626"
                    ]

                }]

            },

            options:{

                responsive:true,

                plugins:{

                    legend:{

                        display:false

                    }

                }

            }

        }

    );

}

// =========================================
// RISK CHART
// =========================================

function createRiskChart(invoices) {

    if (riskChart) {

        riskChart.destroy();

    }

    const supplierRisk = {};

    invoices.forEach(inv=>{

        if(!supplierRisk[inv.supplier]){

            supplierRisk[inv.supplier]={

                spending:0,

                risk:0

            };

        }

        supplierRisk[inv.supplier].spending += inv.amount;

        if(inv.exception)

            supplierRisk[inv.supplier].risk +=2;

        if(inv.duplicate)

            supplierRisk[inv.supplier].risk +=3;

    });

    const bubbleData = Object.entries(supplierRisk).map(

        ([supplier,data])=>({

            x:data.spending,

            y:data.risk,

            r:Math.max(10,Math.sqrt(data.spending)/60),

            supplier

        })

    );

    riskChart = new Chart(

        document.getElementById("riskChart"),

        {

            type:"bubble",

            data:{

                datasets:[{

                    label:"Supplier Risk",

                    data:bubbleData,

                    backgroundColor:"#EF4444"

                }]

            },

            options:{

                responsive:true,

                plugins:{

                    tooltip:{

                        callbacks:{

                            label(context){

                                const p=context.raw;

                                return [

                                    p.supplier,

                                    "Spending : ₹"+p.x.toLocaleString(),

                                    "Risk Score : "+p.y

                                ];

                            }

                        }

                    }

                },

                scales:{

                    x:{

                        title:{

                            display:true,

                            text:"Supplier Spending (₹)"

                        }

                    },

                    y:{

                        beginAtZero:true,

                        title:{

                            display:true,

                            text:"Risk Score"

                        }

                    }

                }

            }

        }

    );

}

// =========================================
// RECENT INVOICE TABLE
// =========================================

function renderInvoiceTable(invoices) {

    const tbody = document.getElementById("invoiceTable");

    tbody.innerHTML = "";

    invoices.slice(0, 10).forEach(inv => {

        tbody.innerHTML += `
            <tr>

                <td>${inv.invoice_number}</td>

                <td>${inv.supplier}</td>

                <td>${inv.category}</td>

                <td>₹${inv.amount.toLocaleString()}</td>

                <td>

                    <span class="badge ${
                        inv.status === "Matched"
                            ? "bg-success"
                            : "bg-warning text-dark"
                    }">

                        ${inv.status}

                    </span>

                </td>

            </tr>
        `;

    });

}

// =========================================
// POPULATE FILTERS
// =========================================

function populateFilters(invoices) {

    const supplierFilter =
        document.getElementById("supplierFilter");

    const categoryFilter =
        document.getElementById("categoryFilter");

    supplierFilter.innerHTML =
        '<option value="">All Suppliers</option>';

    categoryFilter.innerHTML =
        '<option value="">All Categories</option>';

    const suppliers =
        [...new Set(invoices.map(i => i.supplier))];

    const categories =
        [...new Set(invoices.map(i => i.category))];

    suppliers.forEach(supplier => {

        supplierFilter.innerHTML +=

        `<option value="${supplier}">
            ${supplier}
        </option>`;

    });

    categories.forEach(category => {

        categoryFilter.innerHTML +=

        `<option value="${category}">
            ${category}
        </option>`;

    });

}

// =========================================
// APPLY FILTERS
// =========================================

function applyFilters() {

    let filtered = [...allInvoices];

    const supplier =
        document.getElementById("supplierFilter").value;

    const category =
        document.getElementById("categoryFilter").value;

    const status =
        document.getElementById("statusFilter").value;

    const search =
        document
        .getElementById("invoiceSearch")
        .value
        .toLowerCase();

    if (supplier) {

        filtered =
            filtered.filter(i => i.supplier === supplier);

    }

    if (category) {

        filtered =
            filtered.filter(i => i.category === category);

    }

    if (status) {

        filtered =
            filtered.filter(i => i.status === status);

    }

    if (search) {

        filtered =
            filtered.filter(i =>
                i.invoice_number
                .toLowerCase()
                .includes(search)
            );

    }

    renderDashboard(filtered);

}

// =========================================
// FILTER EVENTS
// =========================================

function attachEvents() {

    document
        .getElementById("supplierFilter")
        .onchange = applyFilters;

    document
        .getElementById("categoryFilter")
        .onchange = applyFilters;

    document
        .getElementById("statusFilter")
        .onchange = applyFilters;

    document
        .getElementById("invoiceSearch")
        .oninput = applyFilters;

}
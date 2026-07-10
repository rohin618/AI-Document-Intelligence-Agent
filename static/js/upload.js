const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const uploadBtn = document.getElementById("uploadBtn");

const fileDetails = document.getElementById("fileDetails");
const fileName = document.getElementById("fileName");
const fileSize = document.getElementById("fileSize");

const uploadIcon = document.getElementById("uploadIcon");
const uploadTitle = document.getElementById("uploadTitle");
const uploadSubTitle = document.getElementById("uploadSubTitle");

const statusText = document.getElementById("statusText");
const statusSpinner = document.getElementById("statusSpinner");

const result = document.getElementById("result");

// --------------------------
// Upload Area
// --------------------------

dropZone.onclick = () => fileInput.click();

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (e) => {

    e.preventDefault();

    dropZone.classList.remove("drag-over");

    fileInput.files = e.dataTransfer.files;

    updateFile();

});

fileInput.addEventListener("change", updateFile);

function updateFile() {

    if (!fileInput.files.length) return;

    const file = fileInput.files[0];

    fileDetails.classList.remove("d-none");

    fileName.innerText = file.name;

    fileSize.innerText = (file.size / 1024 / 1024).toFixed(2) + " MB";

    uploadIcon.className =
        "bi bi-check-circle-fill display-3 text-success mb-3 d-block";

    uploadTitle.innerText = "Document Ready";

    uploadSubTitle.innerText = "Click Process Document";

    dropZone.classList.add("file-loaded");

}

// --------------------------
// Process Button
// --------------------------

uploadBtn.addEventListener("click", async () => {

    if (!fileInput.files.length) {

        alert("Please choose a document.");

        return;

    }

    uploadBtn.disabled = true;

    uploadBtn.innerHTML = `
        <span class="spinner-border spinner-border-sm"></span>
        Processing...
    `;

    statusSpinner.classList.remove("d-none");

    statusText.innerText = "Uploading document...";

    const formData = new FormData();

    formData.append("file", fileInput.files[0]);

    try {

        const response = await fetch("/extract", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        statusSpinner.classList.add("d-none");

        statusText.innerText = "Completed";

        uploadBtn.disabled = false;

        uploadBtn.innerHTML =
            '<i class="bi bi-lightning-charge-fill"></i> Process Document';

        result.innerHTML = `
        <div class="row g-3">

            <div class="col-md-6">
                <div class="card bg-light border-0">
                    <div class="card-body">
                        <small class="text-muted">Invoice Number</small>
                        <h6>${data.invoice.invoice_number}</h6>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card bg-light border-0">
                    <div class="card-body">
                        <small class="text-muted">Supplier</small>
                        <h6>${data.invoice.supplier}</h6>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card bg-light border-0">
                    <div class="card-body">
                        <small class="text-muted">Amount</small>
                        <h6>${data.invoice.currency} ${data.invoice.amount}</h6>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card bg-light border-0">
                    <div class="card-body">
                        <small class="text-muted">OCR Engine</small>
                        <h6>${data.ocr_engine}</h6>
                    </div>
                </div>
            </div>

            <div class="col-12">
                <div class="card bg-dark text-white">
                    <div class="card-body">
                        <pre class="mb-0">${JSON.stringify(data.invoice, null, 4)}</pre>
                    </div>
                </div>
            </div>

        </div>
        `;

    }
    catch (err) {

        console.error(err);

        uploadBtn.disabled = false;

        uploadBtn.innerHTML =
            '<i class="bi bi-lightning-charge-fill"></i> Process Document';

        statusSpinner.classList.add("d-none");

        statusText.innerText = "Processing Failed";

        alert("Error while processing document.");

    }

});
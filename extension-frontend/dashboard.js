const statusText = document.getElementById('statusText');
const resultTable = document.getElementById('resultTable');
const tbody = document.getElementById('tableBody');

// Helper function to draw rows
function addRowToTable(r) {
    const row = document.createElement('tr');
    if (r.error) {
        row.innerHTML = `<td>${r.url}</td><td class="error" colspan="3">Error: ${r.error}</td>`;
    } else {
        const statusClass = r.is_safe ? "safe" : "phishing";
        const statusTextLabel = r.is_safe ? "SAFE ✅" : "PHISHING 🚨";
        row.innerHTML = `
            <td>${r.url}</td>
            <td class="${statusClass}">${statusTextLabel}</td>
            <td>${r.confidence_safe_percentage}%</td>
            <td>${r.confidence_phishing_percentage}%</td>
        `;
    }
    tbody.appendChild(row);
}

// 1. EXCEL UPLOAD LOGIC
document.getElementById('uploadBtn').addEventListener('click', async () => {
    const fileInput = document.getElementById('fileInput');
    if (fileInput.files.length === 0) {
        statusText.style.color = "red";
        statusText.innerText = "Please select an Excel file first.";
        return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    statusText.style.color = "#333";
    statusText.innerText = "Scanning Excel file... Please wait.";
    tbody.innerHTML = ""; 
    resultTable.style.display = "none";

    try {
        const response = await fetch("http://127.0.0.1:8000/predict-batch", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        
        if (data.detail || data.error) {
            statusText.style.color = "red";
            statusText.innerText = "Error: " + (data.detail || data.error);
            return;
        }

        data.results.forEach(addRowToTable);
        statusText.style.color = "green";
        statusText.innerText = `Scan Complete! Processed ${data.results.length} URLs.`;
        resultTable.style.display = "table";

    } catch (error) {
        statusText.style.color = "red";
        statusText.innerText = "Failed to connect to the server.";
    }
});

// 2. TEXT PASTE LOGIC
document.getElementById('scanTextBtn').addEventListener('click', async () => {
    const textInput = document.getElementById('textInput').value;
    
    if (!textInput.trim()) {
        statusText.style.color = "red";
        statusText.innerText = "Please paste at least one URL.";
        return;
    }

    const urls = textInput.split(',').map(u => u.trim()).filter(u => u.length > 0);
    
    statusText.style.color = "#333";
    statusText.innerText = `Scanning ${urls.length} pasted URL(s)... Please wait.`;
    tbody.innerHTML = ""; 
    resultTable.style.display = "table";

    let successCount = 0;

    for (const url of urls) {
        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: url })
            });
            
            if (response.ok) {
                const data = await response.json();
                addRowToTable(data);
                successCount++;
            } else {
                addRowToTable({ url: url, error: "Server error. Invalid URL format?" });
            }
        } catch (error) {
             addRowToTable({ url: url, error: "Connection failed." });
        }
    }

    statusText.style.color = "green";
    statusText.innerText = `Scan Complete! Processed ${successCount} URLs.`;
});
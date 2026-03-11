document.getElementById('scanCurrentBtn').addEventListener('click', () => {
    const resultDiv = document.getElementById('result');
    const statusLabel = document.getElementById('statusLabel');
    const confidenceLabel = document.getElementById('confidenceLabel');

    statusLabel.innerText = "Analyzing...";
    resultDiv.style.display = "block";
    resultDiv.className = ""; // Reset colors

    chrome.tabs.query({active: true, currentWindow: true}, async function(tabs) {
        const currentUrl = tabs[0].url;
        
        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ url: currentUrl })
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.is_safe) {
                    statusLabel.innerText = "SAFE WEBSITE";
                    resultDiv.className = "result-safe";
                } else {
                    statusLabel.innerText = "PHISHING ALERT";
                    resultDiv.className = "result-phish";
                }
                confidenceLabel.innerText = `${data.confidence_safe_percentage}% Confidence Score`;
            } else {
                statusLabel.innerText = "Error Analyzing";
            }
        } catch (error) {
            statusLabel.innerText = "Backend Offline";
        }
    });
});
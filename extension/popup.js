document.getElementById("checkBtn").addEventListener("click", async () => {
    let url = document.getElementById("urlInput").value;
    let resultDiv = document.getElementById("result");

    if (!url) {
        resultDiv.innerText = "Please enter a URL!";
        resultDiv.style.color = "orange";
        return;
    }

    // Show loading state
    resultDiv.innerText = "Checking...";
    resultDiv.style.color = "blue";

    try {
        // First check if API is running
        let healthCheck = await fetch("http://localhost:8000/", {
            method: "GET"
        }).catch(() => null);

        if (!healthCheck) {
            resultDiv.innerText = "Error: API server is not running. Start it with: uvicorn src.api_fastapi:app --reload --port 8001";
            resultDiv.style.color = "red";
            return;
        }

        let response = await fetch("http://localhost:8000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: url,
                email_text: "",
                html: ""
            })
        });

        if (!response.ok) {
            let error = await response.json();
            resultDiv.innerText = "Error: " + (error.detail || "Unknown error");
            resultDiv.style.color = "red";
            return;
        }

        let data = await response.json();
        let prediction = data.prediction;
        
        if (prediction === "phishing") {
            resultDiv.innerText = "⚠️ WARNING: This appears to be a PHISHING site!";
            resultDiv.style.color = "red";
        } else {
            resultDiv.innerText = "✓ This appears to be a LEGITIMATE site";
            resultDiv.style.color = "green";
        }
    } catch (err) {
        console.error(err);
        resultDiv.innerText = "Error: " + err.message + "\n\nMake sure the API server is running:\nuvicorn src.api_fastapi:app --reload --port 8001";
        resultDiv.style.color = "red";
    }
});

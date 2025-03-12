document.addEventListener("DOMContentLoaded", function () {
    const generateBtn = document.getElementById("generate");
    const queryInput = document.getElementById("query");
    const asciiContainer = document.getElementById("ascii-container");
    const asciiArt = document.getElementById("ascii-art");
    const loading = document.getElementById("loading");

    generateBtn.addEventListener("click", function () {
        let query = queryInput.value.trim();
        if (!query) return alert("Please enter a valid object (e.g., horse, cat, dog)");

        loading.style.display = "block";
        asciiArt.textContent = "";

        fetch(`/generate_ascii?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    asciiArt.textContent = data.ascii;
                } else {
                    asciiArt.textContent = "Error generating ASCII art.";
                }
            })
            .catch(() => {
                asciiArt.textContent = "Failed to connect to server.";
            })
            .finally(() => {
                loading.style.display = "none";
            });
    });

    queryInput.addEventListener("keypress", function (event) {
        if (event.key === "Enter") generateBtn.click();
    });
});

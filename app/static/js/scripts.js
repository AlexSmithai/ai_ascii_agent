function generateASCII() {
    let text = document.getElementById("text-input").value;
    
    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("ascii-output").innerText = data.ascii_art;
    });
}

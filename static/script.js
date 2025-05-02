document.getElementById("pdfForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/upload-pdf/", {
        method: "POST",
        body: formData,
    });

    const result = await response.json();

    if (result.audio_url) {
        const audioPlayer = document.getElementById("audioPlayer");
        audioPlayer.innerHTML = `<audio controls src="${result.audio_url}"></audio>`;

        const stats = document.getElementById("stats");
        stats.innerHTML = `
            <p><strong>Words:</strong> ${result.word_count}</p>
            <p><strong>Characters:</strong> ${result.char_count}</p>
            <p><strong>Estimated Cost:</strong> $${result.estimated_cost}</p>
        `;
    } else {
        alert("Upload failed.");
    }
});
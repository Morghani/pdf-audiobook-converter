const form = document.getElementById("uploadForm");
const message = document.getElementById("message");

form.addEventListener("submit", async (e) => {
    e.preventDefault();
    message.textContent = "Processing...";

    const formData = new FormData(form);

    try {
        const response = await fetch("/upload-pdf/", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Failed to convert PDF.");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const audio = new Audio(url);
        audio.controls = true;
        audio.autoplay = true;

        message.innerHTML = "";
        message.appendChild(audio);
    } catch (error) {
        message.textContent = error.message;
    }
});

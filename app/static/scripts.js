async function submitImage() {
    const fileInput = document.getElementById("imageInput");
    const resultDiv = document.getElementById("result");
    const loader = document.getElementById("loader");

    if (!fileInput.files.length) {
        resultDiv.textContent = "Please upload an image first.";
        return;
    }


    loader.style.display = "block";
    resultDiv.textContent = "";

    const formData = new FormData();
    formData.append("image", fileInput.files[0]);

    console.log(fileInput.files[0]);

    try {
        const response = await fetch("/get_books", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            if (data.predictions && data.predictions.length > 0) {
                // Display predictions in a formatted list
                const predictionsList = data.predictions
                    .map((book) => `<li>${book}</li>`)
                    .join("");
                resultDiv.innerHTML = `
                    <h3>Detected Books:</h3>
                    <ul>${predictionsList}</ul>
                `;
            } else {
                resultDiv.innerHTML = "<h3>No books detected.</h3>";
            }
        } else {
            resultDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        resultDiv.textContent = `Error: ${error.message}`;
    } finally {
        loader.style.display = "none";
    }
}

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


async function submitBookForRecommendation() {
    const recommendationInput = document.getElementById("csvDropdown").value;
    const recommendationResults = document.getElementById("recommendationResults");
    const loader = document.getElementById("loader");

    console.log(recommendationInput); // Changed from print to console.log


    // Display loader and clear previous results
    loader.style.display = "block";
    recommendationResults.textContent = "";

    try {
        // Send the text input to the Flask backend
        const response = await fetch("/get_recommendations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ book_name: recommendationInput }),
        });

        const data = await response.json();

        if (response.ok) {
            if (data.recommended_books && data.recommended_books.length > 0) {
                // Display recommendations as a list
                const recommendationsList = data.recommended_books
                    .map((book) => `<li>${book}</li>`)
                    .join("");
                    recommendationResults.innerHTML = `
                    <h3>Recommended Books:</h3>
                    <ul>${recommendationsList}</ul>
                `;
            } else {
                recommendationResults.innerHTML = "<h3>No recommendations found. Try another book.</h3>";
            }
        } else {
            recommendationResults.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        recommendationResults.textContent = `Error: ${error.message}`;
    } finally {
        loader.style.display = "none";
    }
}
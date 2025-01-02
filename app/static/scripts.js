document.addEventListener("DOMContentLoaded", async function () {
    const dropdown = document.getElementById("csvDropdown");
    const errorDiv = document.getElementById("error");

    dropdown.innerHTML = `<option value="" disabled selected>-- Select an option --</option>`;
    errorDiv.textContent = "";

    try {
        const response = await fetch("/get_dropdown_data");

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.unique_elements && data.unique_elements.length > 0) {
            data.unique_elements.forEach((element) => {
                const option = document.createElement("option");
                option.value = element;
                option.textContent = element;
                dropdown.appendChild(option);
            });
        } else {
            errorDiv.textContent = "No unique elements found in the CSV file.";
        }
    } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
    }
});

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

async function populateDropdown() {
    const dropdown = document.getElementById("csvDropdown");
    const errorDiv = document.getElementById("error");

    // Clear any previous error
    errorDiv.textContent = "";

    try {
        const response = await fetch("/get_dropdown_data");
        const data = await response.json();

        if (response.ok) {
            if (data.unique_elements && data.unique_elements.length > 0) {
                // Populate dropdown with unique elements
                data.unique_elements.forEach((element) => {
                    const option = document.createElement("option");
                    option.value = element;
                    option.textContent = element;
                    dropdown.appendChild(option);
                });
            } else {
                errorDiv.textContent = "No unique elements found in the CSV file.";
            }
        } else {
            errorDiv.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
    }
}

async function submitBookForRecommendation() {
    const recommendationInput = document.getElementById("recommendationInput").value;
    const recommendationResult = document.getElementById("recommendationResult");
    const loader = document.getElementById("loader");

    // Validate input
    if (!recommendationInput.trim()) {
        recommendationResult.textContent = "Please enter the name of a book.";
        return;
    }

    // Display loader and clear previous results
    loader.style.display = "block";
    recommendationResult.textContent = "";

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
                recommendationResult.innerHTML = `
                    <h3>Recommended Books:</h3>
                    <ul>${recommendationsList}</ul>
                `;
            } else {
                recommendationResult.innerHTML = "<h3>No recommendations found. Try another book.</h3>";
            }
        } else {
            recommendationResult.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        recommendationResult.textContent = `Error: ${error.message}`;
    } finally {
        loader.style.display = "none";
    }
}



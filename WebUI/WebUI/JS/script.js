function addSymptomFromInput() {
    var input = document.getElementById("symptomInput");
    var symptom = input.value.trim();
    if (symptom !== "") {
        addSymptom(symptom);
        input.value = ""; // Clear input field after adding the symptom
    }
}

function addSymptom(symptom) {

    var symptomsList = document.getElementById("symptomsList");
    var listItem = document.createElement("li");
    listItem.textContent = symptom;
    listItem.className = "symptom-item"; // Add class for styling
    // Create dustbin icon and append it to the list item
    var dustbinIcon = document.createElement("span");
    dustbinIcon.className = "dustbin-icon";
    dustbinIcon.innerHTML = "&#128465;"; // Unicode character for dustbin icon
    dustbinIcon.onclick = function() { removeSymptom(listItem); }; // Attach click event to remove the symptom
    listItem.appendChild(dustbinIcon);
    symptomsList.appendChild(listItem); // Append new symptom below the previous one
}

function removeSymptom(item) {
    item.remove(); // Remove the symptom from the list
}

function clearInput() {
    document.getElementById("symptomInput").value = ""; // Clear the input field
}

function toggleProfileDetails() {
    var profileDetails = document.getElementById("profileDetails");
    profileDetails.classList.toggle("show");
}

// Assuming this is the JavaScript file that handles the request responses

// Function to display request results
function displayRequestResult(result) {
    const requestResults = document.getElementById('requestResults');
    const resultMessage = document.createElement('div');
    resultMessage.textContent = result;
    requestResults.appendChild(resultMessage);
}

// Example usage:
// If a request is accepted
const acceptResult = 'Request accepted!';
displayRequestResult(acceptResult);

// If a request is declined
const declineResult = 'Request declined!';
displayRequestResult(declineResult);
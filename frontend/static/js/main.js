// ==========================================================================
// Schedule Generator Form Handler
// This script manages the schedule generation form, handles API interactions,
// and provides user feedback through loading states and alerts
// ==========================================================================

document.addEventListener("DOMContentLoaded", function () {
  // Cache DOM Elements
  // Get references to frequently used DOM elements to avoid repeated queries
  const form = document.getElementById("gridForm");
  const errorAlert = document.getElementById("errorAlert");
  const successAlert = document.getElementById("successAlert");
  const submitButton = form.querySelector('button[type="submit"]');

  // Initialize Loading Spinner
  // Create and configure the loading spinner element for the submit button
  const spinner = document.createElement("span");
  spinner.className = "spinner-border spinner-border-sm me-2 d-none";
  spinner.setAttribute("role", "status");
  submitButton.prepend(spinner);

  // Loading State Management
  // Controls the visual feedback during form submission
  function setLoading(isLoading) {
    spinner.classList.toggle("d-none", !isLoading);
    submitButton.disabled = isLoading;
    submitButton.classList.toggle("loading", isLoading);

    // Update button text and maintain styling during loading state
    if (isLoading) {
      submitButton.innerHTML =
        '<span class="spinner-border spinner-border-sm me-2"></span>Generating...';
    } else {
      submitButton.innerHTML = "Generate Schedule";
    }
  }

  // Button Factory Function
  // Creates consistent action buttons with specified properties
  function createActionButton(text, className, clickHandler) {
    const button = document.createElement("button");
    button.textContent = text;
    button.className = `btn ${className} me-2`;
    button.onclick = clickHandler;
    return button;
  }

  // Form Submission Handler
  // Manages the entire form submission process and response handling
  form.addEventListener("submit", async function (e) {
    e.preventDefault(); // Prevent default form submission behavior

    // Reset UI State
    // Clear any existing alerts and action buttons
    errorAlert.style.display = "none";
    successAlert.style.display = "none";
    const existingButtons = document.getElementById("actionButtons");
    if (existingButtons) existingButtons.remove();

    // Get Form Data
    const externalId = document.getElementById("external_id").value;

    setLoading(true); // Activate loading state

    try {
      // API Request
      // Send schedule generation request to backend
      const response = await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ external_id: externalId }),
      });

      const data = await response.json();

      // Success Handler
      // Display success message and create download button
      if (response.ok) {
        successAlert.textContent = data.message;
        successAlert.style.display = "block";
        successAlert.className = "alert alert-success";

        // Create and append download button
        const buttonContainer = document.createElement("div");
        buttonContainer.id = "actionButtons";
        buttonContainer.className = "mt-3";

        const downloadButton = createActionButton(
          "📥 Download Schedule",
          "btn-primary",
          () => (window.location.href = `/download/${data.external_id}`)
        );

        buttonContainer.appendChild(downloadButton);
        successAlert.after(buttonContainer);
      }
      // Error Handler
      // Display appropriate error messages based on response status
      else {
        errorAlert.textContent = data.error;
        errorAlert.style.display = "block";

        // Special case for 404 (no schedule found)
        if (response.status === 404) {
          errorAlert.className = "alert alert-warning";
        } else {
          errorAlert.className = "alert alert-danger";
        }
      }
    } catch (error) {
      // Network Error Handler
      // Handle cases where the server cannot be reached
      errorAlert.textContent = "Failed to connect to server";
      errorAlert.style.display = "block";
      errorAlert.className = "alert alert-danger";
    } finally {
      // Cleanup
      setLoading(false); // Reset loading state regardless of outcome
    }
  });
});

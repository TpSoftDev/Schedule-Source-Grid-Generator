// Wait for the HTML document to be fully loaded before running any code
document.addEventListener("DOMContentLoaded", function () {
  // Get references to HTML elements we need to interact with
  const form = document.getElementById("gridForm");
  const errorAlert = document.getElementById("errorAlert");
  const successAlert = document.getElementById("successAlert");
  const submitButton = form.querySelector('button[type="submit"]');

  // Add loading spinner to button
  const spinner = document.createElement("span");
  spinner.className = "spinner-border spinner-border-sm me-2 d-none";
  spinner.setAttribute("role", "status");
  submitButton.prepend(spinner);

  function setLoading(isLoading) {
    // Show/hide loading spinner and disable/enable button
    spinner.classList.toggle("d-none", !isLoading);
    submitButton.disabled = isLoading;
    submitButton.textContent = isLoading
      ? "Generating..."
      : "Generate Schedule";
  }

  function createActionButton(text, className, clickHandler) {
    const button = document.createElement("button");
    button.textContent = text;
    button.className = `btn ${className} me-2`;
    button.onclick = clickHandler;
    return button;
  }

  // Add event listener for form submission
  form.addEventListener("submit", async function (e) {
    // Prevent the default form submission (page reload)
    e.preventDefault();

    // Hide any existing alert messages
    errorAlert.style.display = "none";
    successAlert.style.display = "none";
    const existingButtons = document.getElementById("actionButtons");
    if (existingButtons) existingButtons.remove();

    // Get the employee ID from the input field
    const externalId = document.getElementById("external_id").value;

    // Show loading state
    setLoading(true);

    try {
      // Send POST request to our backend
      const response = await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Tell server we're sending JSON
        },
        // Convert our data to JSON string
        body: JSON.stringify({ external_id: externalId }),
      });

      // Parse the JSON response from the server
      const data = await response.json();

      if (response.ok) {
        // If request was successful, show success message
        successAlert.textContent = data.message;
        successAlert.style.display = "block";
        successAlert.className = "alert alert-success";

        // Create container for buttons
        const buttonContainer = document.createElement("div");
        buttonContainer.id = "actionButtons";
        buttonContainer.className = "mt-3";

        // Create download button with direct download
        const downloadButton = createActionButton(
          "📥 Download Schedule",
          "btn-primary",
          () => (window.location.href = `/download/${data.external_id}`)
        );

        // Add button to container
        buttonContainer.appendChild(downloadButton);
        successAlert.after(buttonContainer);
      } else {
        // If server returned an error, show error message
        errorAlert.textContent = data.error;
        errorAlert.style.display = "block";

        // Special styling for "no schedule" case
        if (response.status === 404) {
          errorAlert.className = "alert alert-warning";
        } else {
          errorAlert.className = "alert alert-danger";
        }
      }
    } catch (error) {
      // If something went wrong with the request, show error
      errorAlert.textContent = "Failed to connect to server";
      errorAlert.style.display = "block";
      errorAlert.className = "alert alert-danger";
    } finally {
      // Hide loading state
      setLoading(false);
    }
  });
});

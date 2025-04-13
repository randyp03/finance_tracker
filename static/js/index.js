const transactionForm = document.getElementById("transaction-form");
const successMessage = document.getElementById("success-message");

transactionForm.addEventListener("submit", function(event) {
    event.preventDefault(); // prevent page reload

    const form = event.target;
    const formData = new FormData(transactionForm);
    const data = Object.fromEntries(formData.entries());
})
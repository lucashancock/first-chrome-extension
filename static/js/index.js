document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const loading = document.querySelector("#loading");

    form.addEventListener("submit", function () {
        // Show the loading symbol when the form is submitted
        loading.style.display = "block";
    });
});

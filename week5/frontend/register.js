document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("register-form");

  form.addEventListener("submit", function (event) {
    event.preventDefault(); // stop form from automatically submitting, required

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;

    // Option 1: storing data in the url (exposing sensitive info)
    // if (name.trim() === "" || email.trim() === "") {
    //   alert("Please enter your name and email.");
    // } else {
    //   // Redirect to welcome page with name in URL
    //   window.location.href = `welcome.html?name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}`;
    // }

    // Option 2: storing data in sessionStorage
    const user = {"name":name, "email":email}
    sessionStorage.setItem("user", JSON.stringify(user))
    window.location.href = "welcome.html"
  });
});

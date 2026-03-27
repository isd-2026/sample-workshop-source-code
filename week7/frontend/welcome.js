document.addEventListener("DOMContentLoaded", function () {
  const welcomeMessage = document.getElementById("welcome-message");
  const logoutButton = document.getElementById("logoutBtn");

  // Option 1: retriving user details from url
  // const params = new URLSearchParams(window.location.search);
  // const name = params.get("name");
  // const email = params.get("email");

  // if (welcomeMessage) {
  //   if (name) {
  //     welcomeMessage.textContent = `Welcome, ${name}! \n Your email address is ${email}.`;
  //   } else {
  //     welcomeMessage.textContent = "Please register!";
  //   }
  // }

  // Option 2: retrieving user details from sessionStorage
  const user = JSON.parse(sessionStorage.getItem("user"));

  if (user) {
    welcomeMessage.textContent = `Welcome, ${user.name}! \n Your email address is ${user.email}.`;
  } else {
    welcomeMessage.textContent = "Please register!";
  }

  logoutButton.addEventListener("click", function () {
    sessionStorage.clear();
    window.location.href = "logout.html"
  })
});

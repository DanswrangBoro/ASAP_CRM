var selectionVariableData = {};
var selectionVariableData = {};

function setActive(index) {
  var spans = document.querySelectorAll(".booking__nav span");
  var selectedClassType = spans[index].dataset.classType;
  // Remove "active" class from all spans
  spans.forEach(function (span) {
    span.classList.remove("active");
  });

  // Add "active" class to the clicked span
  spans[index].classList.add("active");
  var selectFiled = document.getElementById("class");
  selectFiled.value = selectedClassType;
  var selectFiledM = document.getElementById("Mclass");
  selectFiledM.value = selectedClassType;
  localStorage.setItem("class", selectFiled);
}

document.addEventListener("DOMContentLoaded", function () {
  setActive(0);
});
// Add this to your script.js
document.addEventListener("DOMContentLoaded", function () {
  const travellersInput = document.getElementById("travellersInput");
  const passengerModal = document.getElementById("passengerModal");
  const closeModalBtn = document.getElementById("closeModal");
  const submitBtnModal = document.getElementById("submitBtnModal");
  const adultsModal = document.getElementById("adultsModal");

  travellersInput.addEventListener("click", function () {
    passengerModal.style.display = "block";
  });

  closeModalBtn.addEventListener("click", function () {
    passengerModal.style.display = "none";
  });

  submitBtnModal.addEventListener("click", function () {
    // Retrieve the value from the modal form
    const adultsValue = adultsModal.value;

    // Perform actions with the captured value (e.g., display or use it)
    console.log("Number of Adults from Modal:", adultsValue);

    // Close the modal
    passengerModal.style.display = "none";
  });

  // Close the modal if the user clicks outside of it
  window.addEventListener("click", function (event) {
    if (event.target === passengerModal) {
      passengerModal.style.display = "none";
    }
  });
});

async function openModal() {
  // Open the modal
  document.getElementById("travelersModal").style.display = "block";

  // Wait for a short delay to ensure the modal is displayed
  await delay(100);

  // Add click event listener after opening the modal
  document.addEventListener("click", closeModalIfOutside);
}

function closeModalIfOutside(event) {
  var modal = document.getElementById("travelersModal");

  if (event.target !== modal && !modal.contains(event.target)) {
    // Remove the click event listener
    document.removeEventListener("click", closeModalIfOutside);

    // Close the modal
    modal.style.display = "none";
    updateInput();
  }
}

function updateInput() {
  // const travelClass = document.getElementById("travelClass").value;
  const adults = parseInt(document.getElementById("adults").value, 10) || 0;
  const children = parseInt(document.getElementById("children").value, 10) || 0;
  const infants = parseInt(document.getElementById("infants").value, 10) || 0;

  const totalTravelers = adults + children + infants;

  const travelDetailsInput = document.getElementById("travelDetails");
  // travelDetailsInput.value = `${totalTravelers}|${travelClass}`;
  travelDetailsInput.value = `${totalTravelers}`;

  closeModal();
}

function closeModal() {
  document.getElementById("travelersModal").style.display = "none";
}

async function getCurrency() {
  const currency = document.getElementById("currency");
  const Mcurrency = document.getElementById("Mcurrency");
  const data = await fetch("https://ipapi.co/currency/");
  const response = await data.text();
  currency.value = response;
  Mcurrency.value = response;
  console.log(response);
}

async function signup() {
  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const requestBody = {
    username: username,
    email: email,
    password: password,
  };

  const signupUrl = document.getElementById("signUp");
  const signUpPage = signupUrl.getAttribute("data-base-url");

  const response = await fetch(`${signUpPage}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(requestBody),
  });
  const data = await response.json();
  if (data.message === "success") {
    const alertMessage1 = document.getElementById("successAlert");
    alertMessage1.style.display = "block";
    const alertMessage2 = document.getElementById("dangerAlert");
    alertMessage2.style.display = "none";

    console.log(data.message);
  } else {
    const alertMessage1 = document.getElementById("dangerAlert");
    alertMessage1.style.display = "block";
    const alertMessage2 = document.getElementById("successAlert");
    alertMessage2.style.display = "none";
    alertMessage1.textContent = `${data.message}`;
    console.log(data.message);
  }

  console.log(username, email, password);
}

async function login() {
  const username = document.getElementById("loginUsername").value;
  const password = document.getElementById("loginPassword").value;

  const requestBody = {
    username: username,
    password: password,
  };

  const loginUrl = document.getElementById("login");
  const loginPage = loginUrl.getAttribute("data-base-url");

  const response = await fetch(`${loginPage}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(requestBody),
  });

  const data = await response.json();
  if (data.message === "success") {
    const loginModal = document.getElementById("loginFields");
    loginModal.style.display = "none";
    const overlay = document.getElementById("overlay");
    overlay.style.display = "none";
    const overlaySignup = document.getElementById("signupSec");
    overlaySignup.style.display = "none";
  }
  console.log(data);
}

function getCookie(name) {
  const cookies = document.cookie.split(";").map((cookie) => cookie.trim());
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i];
    const cookieName = cookie.split("=")[0];
    if (cookieName.toLowerCase() === name.toLowerCase()) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

function checkSession() {
  // Log the raw cookie string
  console.log("Raw cookie string:", document.cookie);

  // Check if a session cookie exists
  const sessionId = getCookie("sessionid");
  console.log("Extracted session ID:", sessionId);

  if (sessionId) {
    // Session exists, user is logged in
    console.log("User is logged in");
  } else {
    // Session doesn't exist, user is not logged in
    console.log("User is not logged in");
  }
}

// function getCookie(name) {
//   const cookies = document.cookie.split(";");
//   for (let i = 0; i < cookies.length; i++) {
//     const cookie = cookies[i].trim();
//     if (cookie.startsWith(name + "=")) {
//       return decodeURIComponent(cookie.substring(name.length + 1));
//     }
//   }
//   return null;
// }

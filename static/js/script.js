//initilise jarallax
jarallax(document.querySelectorAll(".jarallax"));

//Message alerts
document.addEventListener("DOMContentLoaded", function () {
  let messageContainer = document.getElementById("message-container");
  let alerts = messageContainer.querySelectorAll(".alert");

  function showMessage() {
    messageContainer.style.display = "block";
    messageContainer.style.transition = "transform 0.3s ease-in-out";
    messageContainer.style.transform = "translateY(0)";
  }

  function hideMessage() {
    messageContainer.style.transition = "transform 0.3s ease-in-out";
    messageContainer.style.transform = "translateY(-100%)";

    // Delay hiding the message container after the animation completes
    setTimeout(function () {
      messageContainer.style.display = "none";
    }, 300);
  }

  // Function to hide the message container after 3 seconds
  function autoHideMessage() {
    setTimeout(function () {
      hideMessage();
    }, 3000); // 3 seconds
  }

  // Check if there are messages to display
  if (alerts.length > 0) {
    showMessage();
    autoHideMessage(); // Automatically hide after 3 seconds
  }

  // Add click event listener to each close button
  alerts.forEach(function (alert) {
    let closeButton = alert.querySelector(".btn-close");

    closeButton.addEventListener("click", function () {
      hideMessage();
    });
  });
});

//map

// Retrieve latitude and longitude from the HTML element
let carLocationElement = document.getElementById("car-location");
let latitude = carLocationElement.getAttribute("data-latitude");
let longitude = carLocationElement.getAttribute("data-longitude");
let locationName = carLocationElement.textContent;

// Initialize the map
let carLocation = [parseFloat(latitude), parseFloat(longitude)];
let map = L.map("map").setView(carLocation, 15);

// Add the tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Add a marker with a popup
L.marker(carLocation)
  .addTo(map)
  .bindPopup("Location: " + locationName);

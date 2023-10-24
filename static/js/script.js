// Initialize the jarallax plugin for parallax scrolling
jarallax(document.querySelectorAll(".jarallax"));

// Functionality for displaying message alerts
document.addEventListener("DOMContentLoaded", function () {
  let messageContainer = document.getElementById("message-container");
  let alerts = messageContainer.querySelectorAll(".alert");

  function showMessage() {
    // Show the message container
    messageContainer.style.display = "block";
    messageContainer.style.transition = "transform 0.3s ease-in-out";
    messageContainer.style.transform = "translateY(0)";
  }

  function hideMessage() {
    // Hide the message container with animation
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

// Filtering options using jQuery
$(document).ready(function () {
  // Function to update dropdown options
  function updateDropdown(dropdown, data, placeholder) {
    dropdown.empty();
    dropdown.append(
      $("<option>", {
        value: "",
        text: placeholder,
      })
    );
    $.each(data, function (index, item) {
      dropdown.append(
        $("<option>", {
          value: item.value,
          text: item.text,
        })
      );
    });
  }

  // AJAX request to populate car makes when page loads
  $.ajax({
    url: "/get_car_makes/",
    success: function (data) {
      updateDropdown($("#car_make"), data, "Select Manufacturer");
    },
  });

  // Event handlers for filtering car models, years, types, and fuel types
  // These make additional AJAX requests to populate dropdowns
  $("#car_make").change(function () {
    let selectedMake = $(this).val();
    if (selectedMake) {
      $.ajax({
        url: "/get_car_models/",
        data: {
          make: selectedMake,
        },
        success: function (data) {
          updateDropdown($("#car_model"), data, "Select Model");
        },
      });
    }
  });

  // Event handler for car model selection
  $("#car_model").change(function () {
    let selectedModel = $(this).val();
    if (selectedModel) {
      $.ajax({
        url: "/get_car_years/",
        data: {
          model: selectedModel,
        },
        success: function (data) {
          updateDropdown($("#car_year"), data, "Select Year");
        },
      });
    }
  });

  // Event handler for car year selection
  $("#car_year").change(function () {
    let selectedYear = $(this).val();
    if (selectedYear) {
      $.ajax({
        url: "/get_car_types/",
        data: {
          year: selectedYear,
        },
        success: function (data) {
          updateDropdown($("#car_type"), data, "Select Car Type");
        },
      });
    }
  });

  // Event handler for car type selection
  $("#car_type").change(function () {
    let selectedCarType = $(this).val();
    if (selectedCarType) {
      $.ajax({
        url: "/get_fuel_types/",
        data: {
          car_type: selectedCarType,
        },
        success: function (data) {
          updateDropdown($("#fuel_type"), data, "Select Fuel Type");
        },
      });
    }
  });

  // Event handler for fuel type selection
  $("#fuel_type").change(function () {
    let selectedFuelType = $(this).val();
    if (selectedFuelType) {
      $.ajax({
        url: "/get_car_locations/",
        data: {
          fuel_type: selectedFuelType,
        },
        success: function (data) {
          updateDropdown($("#car_location"), data, "Select Location");
        },
      });
    }
  });
});

// Display car location on a map
let carLocationElement = document.getElementById("car-location");

if (carLocationElement) {
  // Retrieve latitude and longitude from the HTML element
  let latitude = carLocationElement.getAttribute("data-latitude");
  let longitude = carLocationElement.getAttribute("data-longitude");
  let locationName = carLocationElement.textContent;

  // Initialize the map using Leaflet
  let carLocation = [parseFloat(latitude), parseFloat(longitude)];
  let map = L.map("map").setView(carLocation, 15);

  // Uses OpenStreetMap for the base layer
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Add a marker for the car's location
  L.marker(carLocation)
    .addTo(map)
    .bindPopup("Location: " + locationName);
}

// Payment handling
const formElement = document.getElementById("payment-form");
const stripePublishableKey = formElement.getAttribute("data-pk");
const bookingId = formElement.getAttribute("data-booking-id");
const carId = formElement.getAttribute("data-car-id");
const clientSecret = formElement.getAttribute("data-client-secret");
const siteUrl = window.location.protocol + "//" + window.location.hostname

const stripe = Stripe(stripePublishableKey);

let elements;

initialize();

document
  .querySelector("#payment-form")
  .addEventListener("submit", handleSubmit);

let emailAddress = "";

// Initialize Stripe elements and link authentication
async function initialize() {
  // Configure the appearance of Stripe elements
  const appearance = {
    theme: 'night',
    variables: {
      fontFamily: 'Sohne, system-ui, sans-serif',
      fontWeightNormal: '500',
      borderRadius: '8px',
      colorPrimary: '#f2f2f2',
      colorText: '#9c8c73',
      colorTextPlaceholder: '#727F96',
    },
    rules: {
      '.Input, .Block': {
        backgroundColor: '#f2f2f2',
        border: '1.5px solid var(--colorPrimary)'
      }
    }
  };
  elements = stripe.elements({ appearance, clientSecret });

  // Create and mount the link authentication element
  const linkAuthenticationElement = elements.create("linkAuthentication");
  linkAuthenticationElement.mount("#link-authentication-element");

  // Update the email address when it changes in the link authentication element
  linkAuthenticationElement.on("change", (event) => {
    emailAddress = event.value.email;
  });

  // Configure options for the payment element
  const paymentElementOptions = {
    layout: "tabs",
  };

  // Create and mount the payment element
  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element");
}

// Handle the form submission for payment confirmation
async function handleSubmit(e) {
  e.preventDefault();

  // Confirm the payment using Stripe
  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: `${siteUrl}/booking/${bookingId}/confirmation/`,
      receipt_email: emailAddress,
    },
  });

  // Show appropriate messages based on the payment outcome
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }
}

// UI helper to display messages
function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  // Show the message container and set the message text
  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  // Hide the message container after 4 seconds
  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageContainer.textContent = "";
  }, 4000);
}

// Show a loading spinner during payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    // Enable the button and hide the spinner
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}


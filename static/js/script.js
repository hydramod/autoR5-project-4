
//initilise jarallax
jarallax(document.querySelectorAll('.jarallax'));


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


//filter
$(document).ready(function() {
    // Function to update dropdown options
    function updateDropdown(dropdown, data, placeholder) {
        dropdown.empty();
        dropdown.append($('<option>', {
            value: '',
            text: placeholder
        }));
        $.each(data, function(index, item) {
            dropdown.append($('<option>', {
                value: item.value,
                text: item.text
            }));
        });
    }

    // AJAX request to populate car makes when page loads
    $.ajax({
        url: '/get_car_makes/',
        success: function(data) {
            updateDropdown($('#car_make'), data, 'Select Manufacturer');
        }
    });

    // Event handler for car make selection
    $('#car_make').change(function() {
        let selectedMake = $(this).val();
        if (selectedMake) {
            $.ajax({
                url: '/get_car_models/',
                data: {
                    'make': selectedMake
                },
                success: function(data) {
                    updateDropdown($('#car_model'), data, 'Select Model');
                }
            });
        }
    });

    // Event handler for car model selection
    $('#car_model').change(function() {
        let selectedModel = $(this).val();
        if (selectedModel) {
            $.ajax({
                url: '/get_car_years/',
                data: {
                    'model': selectedModel
                },
                success: function(data) {
                    updateDropdown($('#car_year'), data, 'Select Year');
                }
            });
        }
    });

    // Event handler for car year selection
    $('#car_year').change(function() {
        let selectedYear = $(this).val();
        if (selectedYear) {
            $.ajax({
                url: '/get_car_types/',
                data: {
                    'year': selectedYear
                },
                success: function(data) {
                    updateDropdown($('#car_type'), data, 'Select Car Type');
                }
            });
        }
    });

    // Event handler for car type selection
    $('#car_type').change(function() {
        let selectedCarType = $(this).val();
        if (selectedCarType) {
            $.ajax({
                url: '/get_fuel_types/',
                data: {
                    'car_type': selectedCarType
                },
                success: function(data) {
                    updateDropdown($('#fuel_type'), data, 'Select Fuel Type');
                }
            });
        }
    });

    // Event handler for fuel type selection
    $('#fuel_type').change(function() {
        let selectedFuelType = $(this).val();
        if (selectedFuelType) {
            $.ajax({
                url: '/get_car_locations/',
                data: {
                    'fuel_type': selectedFuelType
                },
                success: function(data) {
                    updateDropdown($('#car_location'), data, 'Select Location');
                }
            });
        }
    });
});


//map
// Retrieve latitude and longitude from the HTML element
let carLocationElement = document.getElementById('car-location');

if (carLocationElement) {
    let latitude = carLocationElement.getAttribute('data-latitude');
    let longitude = carLocationElement.getAttribute('data-longitude');
    let locationName = carLocationElement.textContent;

    // Initialize the map
    let carLocation = [parseFloat(latitude), parseFloat(longitude)];
    let map = L.map('map').setView(carLocation, 15);

    // Add the tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Add a marker with a popup
    L.marker(carLocation).addTo(map).bindPopup("Location: " + locationName);
}

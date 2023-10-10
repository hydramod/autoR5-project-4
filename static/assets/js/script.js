
//initilise jarallax
jarallax(document.querySelectorAll('.jarallax'));

//Message alerts
document.addEventListener("DOMContentLoaded", function () {
    var messageContainer = document.getElementById("message-container");
    var alerts = messageContainer.querySelectorAll(".alert");

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
        var closeButton = alert.querySelector(".btn-close");

        closeButton.addEventListener("click", function () {
            hideMessage();
        });
    });
});




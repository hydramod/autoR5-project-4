//**navbar**//

//Select the button element
var button = document.querySelector(".navbar-toggler");

//Select the menu element
var menu = document.querySelector(".navbar-collapse");

//Add a click event listener to the button element
button.addEventListener("click", function () {
  //Toggle the "collapse" class on the menu element
  menu.classList.toggle("collapse");
});

//**smooth scrolling**//

// Select all links with "#" href
var links = document.querySelectorAll('a[href^="#"]');

// Iterate through the links
for (var i = 0; i < links.length; i++) {
  var link = links[i];

  // Add click event listener to each link
  link.addEventListener("click", function (event) {
    event.preventDefault();

    // Get the target element's id
    var targetId = this.getAttribute("href");
    var target = document.querySelector(targetId);

    // Animate the scroll to the target element
    var scrollOptions = {
      left: 0,
      top: target.getBoundingClientRect().top + window.pageYOffset,
      behavior: "smooth"
    };
    window.scrollTo(scrollOptions);
  });
}
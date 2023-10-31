const puppeteer = require("puppeteer");

describe("Webpage Loading Test", () => {
  it('Should load the webpage successfully and contain an element with ID "jarallax-container-0"', async () => {
    const browser = await puppeteer.launch({ headless: "new" });
    const page = await browser.newPage();

    // Replace with the URL of the webpage you want to check
    const urlToCheck = "http://localhost:8000"; // Replace with the actual URL

    await page.goto(urlToCheck);

    // Check if an element with ID "jarallax-container-0" is present
    const elementExists = await page.evaluate(() => {
      return !!document.getElementById("jarallax-container-0");
    });

    expect(elementExists).toBe(true);

    await browser.close();
  }, 10000);
});

describe("Submit form and Display Message Test", () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({ headeless: "new" });
    page = await browser.newPage();
  });

  afterAll(async () => {
    await browser.close();
  });

  it("Should send a contact form and display a success message", async () => {
    const baseUrl = "http://localhost:8000";
    const pageUrl = `${baseUrl}/contact/`;

    await page.goto(pageUrl);

    // Fill in the contact form
    await page.type("#id_first_name", "john");
    await page.type("#id_last_name", "doe");
    await page.type("#id_email", "123@email.com");
    await page.type("#id_subject", "test subject");
    await page.type("#id_message", "test message");
    await page.click('button[type="submit"]');

    // Check for the success message
    const successMessage = await page.evaluate(() => {
      return document.getElementsByClassName("alert-success");
    });

    expect(successMessage).not.toBeNull();
  }, 10000);
});

describe("Filtering Options Test", () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({ headless: "new" });
    page = await browser.newPage();
  });

  afterAll(async () => {
    await browser.close();
  });

  it("Should update dropdown options based on selection", async () => {
    const baseUrl = "http://localhost:8000";
    const pageUrl = `${baseUrl}/cars_list/`;

    await page.goto(pageUrl);

    // Select a car make
    await page.select("#car_make", "Honda");

    // Wait for AJAX request and dropdown update
    await page.waitForTimeout(1000);

    // Check if the car model dropdown is updated
    const carModelDropdownOptions = await page.evaluate(() => {
      const carModelDropdown = document.getElementById("car_model");
      return Array.from(carModelDropdown.options).map((option) => option.value);
    });

    expect(carModelDropdownOptions).toContain("Civic");

    // Check if the car year dropdown is updated
    const carYearDropdownOptions = await page.evaluate(() => {
      const carYearDropdown = document.getElementById("car_year");
      return Array.from(carYearDropdown.options).map((option) => option.value);
    });

    expect(carYearDropdownOptions).toContain("2022");

    // Check if the car type dropdown is updated
    const carTypeDropdownOptions = await page.evaluate(() => {
      const carTypeDropdown = document.getElementById("car_type");
      return Array.from(carTypeDropdown.options).map((option) => option.value);
    });

    expect(carTypeDropdownOptions).toContain("Hatchback");

    // Check if the car fuel type dropdown is updated
    const carFuelDropdownOptions = await page.evaluate(() => {
      const carFuelDropdown = document.getElementById("fuel_type");
      return Array.from(carFuelDropdown.options).map((option) => option.value);
    });

    expect(carFuelDropdownOptions).toContain("Petrol");

    // Check if the car type dropdown is updated
    const carLocationDropdownOptions = await page.evaluate(() => {
      const carLocationDropdown = document.getElementById("car_location");
      return Array.from(carLocationDropdown.options).map(
        (option) => option.value
      );
    });

    expect(carLocationDropdownOptions).toContain("Dublin");
  }, 10000);
});

describe("Login and Display Map Marker Test", () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({ headeless: "new" });
    page = await browser.newPage();
  });

  afterAll(async () => {
    await browser.close();
  });

  it("Should log in, navigate to the confirmation page, and check for map markers", async () => {
    const baseUrl = "http://localhost:8000";

    // Log in
    await page.goto(`${baseUrl}/account/login/`);
    await page.type("#id_login", "teststaff");
    await page.type("#id_password", "staffpass");
    await page.click('button[type="submit"]');

    // Navigate to the dashboard
    await page.goto(`${baseUrl}/dashboard/`);

    // Find the URL for the booking confirmation page
    const confirmationLink = await page.evaluate(() => {
      const linkElement = document.querySelector(
        'a[href^="/booking/2/confirmation/"]'
      );
      return linkElement ? linkElement.getAttribute("href") : null;
    });

    if (confirmationLink) {
      // Go to the booking confirmation page
      await page.goto(`${baseUrl}${confirmationLink}`);
    } else {
      fail("Confirmation link not found.");
      return;
    }

    // Check for map markers
    const markersExist = await page.evaluate(() => {
      const map = document.getElementById("map");
      if (map) {
        document.getElementsByClassName("leaflet-marker-icon");
        return true;
      }
      return false;
    });

    expect(markersExist).toBe(true);
  }, 10000);
});

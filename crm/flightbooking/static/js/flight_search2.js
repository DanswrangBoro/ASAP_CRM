console.log(flightOffer);
console.log(flightOffer.flight_offers_departure[0].price.currency);
console.log(flightOffer.airlines2);
localStorage.setItem("airline", JSON.stringify(flightOffer.airlines2));
var nonStopOption = false;
const selectedFlight = {
  flight_offers_departure: [], // Array to store selected departure flight offers
  flight_offers_return: [], // Array to store selected return flight offers
};
const curencySymbol = `${flightOffer.symbol}`;
function formatDateTime(dateTimeString) {
  const options = {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  };
  const date = new Date(dateTimeString);
  const formattedDateTime = date.toLocaleString("en-US", options);

  return formattedDateTime;
}

const dateTimeString = "2023-11-26T06:55:00";
const formattedDateTime = formatDateTime(dateTimeString);
console.log(formattedDateTime); // Output: 26 Nov 2023, 06:55 AM

function formatDuration(durationString) {
  const durationRegex = /PT(\d+H)?(\d+M)?/; // Regex to extract hours and minutes
  const matches = durationString.match(durationRegex);

  if (!matches) {
    return "Invalid duration format";
  }

  const hours = matches[1] ? parseInt(matches[1], 10) : 0;
  const minutes = matches[2] ? parseInt(matches[2], 10) : 0;

  let formattedDuration = "";
  if (hours > 0) {
    formattedDuration += `${hours}h `;
  }
  if (minutes > 0) {
    formattedDuration += `${minutes}M`;
  }

  return formattedDuration.trim();
}
function extractDate(dateTimeString) {
  // Split the dateTimeString at "T" to separate date and time
  const parts = dateTimeString.split("T");

  // The first part (parts[0]) will be the date
  return parts[0];
}

function formatDateString(inputDateString) {
  // Convert the input string to a Date object
  const inputDate = new Date(inputDateString);

  // Options for formatting the date
  const options = { day: "numeric", month: "short", year: "numeric" };

  // Format the date using toLocaleString
  const formattedDate = inputDate.toLocaleString("en-US", options);

  return formattedDate;
}
function extractTimeFromDate(inputDate) {
  const dateObject = new Date(inputDate);

  // Get hours, minutes, and AM/PM indicator
  const hours = dateObject.getHours();
  const minutes = dateObject.getMinutes();
  const amPm = hours >= 12 ? "PM" : "AM";

  // Convert hours to 12-hour format
  const formattedHours = hours % 12 || 12;

  // Format the time with AM/PM
  const formattedTime = `${formattedHours.toString().padStart(2, "0")}:${minutes
    .toString()
    .padStart(2, "0")} ${amPm}`;

  return formattedTime;
}

// Function to display flight results ---------------------------------------------------------------------------

// Add event listeners to the departure and return buttons
// Add event listeners to the departure and return buttons
document.addEventListener("DOMContentLoaded", function () {
  // Your JavaScript code here
  displayFlightResults(flightOffer);

  const departureButton = document.getElementById("departureButton");
  const returnButton = document.getElementById("returnButton");

  departureButton.addEventListener("click", function () {
    departureButton.classList.add("active");
    returnButton.classList.remove("active");

    // Clear existing data and display departure data
    clearFlightResults();
    displayFlightResults(flightOffer, "departure");
  });

  returnButton.addEventListener("click", function () {
    returnButton.classList.add("active");
    departureButton.classList.remove("active");

    // Clear existing data and display return data
    clearFlightResults();
    displayFlightResults(flightOffer, "return");
  });
});

function clearFlightResults() {
  const container = document.getElementById("flightResults");
  const containerReturn = document.getElementById("flightResultsReturn");
  container.innerHTML = "";
  containerReturn.innerHTML = "";
}
// test end ------------------------------------------------------------------------------------------------------------

// Add a global variable to track the active section
let activeSection = "departure"; // Default to departure
document.addEventListener("DOMContentLoaded", function () {
  // Your JavaScript code here
  displayFlightResults(flightOffer, "departure"); // Display departure data by default

  const departureButton = document.getElementById("departureButton");
  const returnButton = document.getElementById("returnButton");
  // Update event listeners for the buttons
  departureButton.addEventListener("click", function () {
    if (activeSection !== "departure") {
      activeSection = "departure";
      departureButton.classList.add("active");
      returnButton.classList.remove("active");
      clearFlightResults();
      displayFlightResults(flightOffer, "departure");
    }
  });

  returnButton.addEventListener("click", function () {
    if (activeSection !== "return") {
      activeSection = "return";
      returnButton.classList.add("active");
      departureButton.classList.remove("active");
      clearFlightResults();
      displayFlightResults(flightOffer, "return");
    }
  });
});

// Function to display the result header
function displayResultHeader(
  departure,
  arrival,
  departureTime,
  arrivalTime,
  type
) {
  const headerContainer = document.getElementById("flightResultsHeader");
  headerContainer.innerHTML = ""; // Clear existing content

  // Create header elements
  const departureInfo = document.createElement("div");
  departureInfo.textContent = `Departure: ${departure} (${departureTime})`;
  departureInfo.classList.add("header-info");

  const svgIcon = document.createElement("span");
  svgIcon.innerHTML = "&rarr;";
  svgIcon.classList.add("arrow-icon");

  const arrivalInfo = document.createElement("div");
  arrivalInfo.textContent = `Arrival: ${arrival} (${arrivalTime})`;
  arrivalInfo.classList.add("header-info");

  // Append elements to the header container
  headerContainer.appendChild(departureInfo);
  headerContainer.appendChild(svgIcon);
  headerContainer.appendChild(arrivalInfo);
}

function displayFlightResults(data, type) {
  // Get departure and arrival details based on the type (departure or return)
  let departurePlace, arrivalPlace, departureDate, arrivalDate;
  if (type === "departure") {
    departurePlace = data.origin;
    arrivalPlace = flightOffer.destination;
    departureDate = extractDate(
      data.flight_offers_departure[0].itineraries[0].segments[0].departure.at
    ); // Assuming flightOffer has a departure date property
    arrivalDate = extractDate(
      data.flight_offers_departure[0].itineraries[0].segments[0].arrival.at
    ); // Assuming flightOffer has an arrival date property
  } else if (type === "return") {
    departurePlace = flightOffer.destination;
    arrivalPlace = flightOffer.origin;
    departureDate = extractDate(
      data.flight_offers_return[0].itineraries[0].segments[0].departure.at
    ); // Assuming flightOffer has a departure date property
    arrivalDate = extractDate(
      data.flight_offers_return[0].itineraries[0].segments[0].arrival.at
    ); // Assuming flightOffer has an arrival date property
  }

  // Call displayResultHeader function to display the header
  displayResultHeader(
    departurePlace,
    arrivalPlace,
    departureDate,
    arrivalDate,
    type
  );

  // Get the container where you want to display the flight results
  if (nonStopOption == false) {
    if (type == "departure" && data && data.flight_offers_departure) {
      const condition = false;
      data.flight_offers_departure.forEach((element, index) => {
        const container = document.getElementById("flightResults");

        // Create a div element for the main container
        const fData = document.createElement("div");
        fData.classList.add("mainCont");
        const length = element.itineraries[0].segments.length - 1;
        // Create parent div
        const logoDiv = document.createElement("div");
        logoDiv.classList.add("logo-area");

        //---------------------------------------------------------------------------------------------------------------

        // Create first child div with text "Airline" and a background color
        const airlineDiv = document.createElement("div");
        code =
          flightOffer.airlines[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];
        airlineDiv.textContent = `${code}`;
        airlineDiv.classList.add("airlineDiv");

        // Create second child div with text "logo" and a different background color
        const logoChildDiv = document.createElement("div");

        const inputText = `${element.itineraries[0].segments[0].carrierCode}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
        const hashedText = CryptoJS.MD5(inputText).toString();

        // logoChildDiv.innerHTML = `<img id='logoI' src="https://content.airhex.com/content/logos/airlines_${element.itineraries[0].segments[0].carrierCode}_2000_1000_t.png?md5apikey=${hashedText}">`;
        const temp =
          flightOffer.airlines2[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];
        console.log(temp);
        logoChildDiv.innerHTML = `<img id='logoI' src='https://thimpu.pythonanywhere.com/logo/api/airline/${temp}' alt='not found'>`;
        logoChildDiv.classList.add("logoChildDiv");

        // Append child divs to parent logoDiv
        logoDiv.appendChild(airlineDiv);
        logoDiv.appendChild(logoChildDiv);

        //--------------------------------------------------------------------------------------------------------------

        const locaTimeDiv = document.createElement("div");
        locaTimeDiv.classList.add("locaTime-area");

        // Create first child div with text "Airline" and a background color
        const orDiv = document.createElement("div");
        orDiv.textContent = `${flightOffer.origin}`;
        orDiv.classList.add("orDiv");

        // Create second child div with text "logo" and a different background color
        const timeDiv = document.createElement("div");
        const timeDepart = extractTimeFromDate(
          element.itineraries[0].segments[0].departure.at
        );
        timeDiv.textContent = `${timeDepart}`;
        timeDiv.classList.add("timeDiv");

        // Append child divs to parent logoDiv
        locaTimeDiv.appendChild(orDiv);
        locaTimeDiv.appendChild(timeDiv);

        // ---------------------------------------------------------------------------------------------------------------------

        const stopsDiv = document.createElement("div");
        stopsDiv.classList.add("stops-area");

        // Create first child div with text "Airline" and a background color
        const durDiv = document.createElement("div");
        const duration = formatDuration(`${element.itineraries[0].duration}`);
        durDiv.textContent = `${duration}`;
        durDiv.classList.add("durDiv");

        //Create an arrow Div
        const arrowDiv = document.createElement("div");
        arrowDiv.textContent = "→";
        arrowDiv.classList.add("arrowDiv");

        // Create second child div with text "logo" and a different background color
        const stopDiv = document.createElement("div");
        stopDiv.textContent = `${length} stops`;
        stopDiv.classList.add("stopDiv");

        // Append child divs to parent logoDiv
        stopsDiv.appendChild(durDiv);
        stopsDiv.appendChild(arrowDiv);
        stopsDiv.appendChild(stopDiv);

        //--------------------------------------------------------------------------------------------------------------

        const arriTimeDiv = document.createElement("div");
        arriTimeDiv.classList.add("arriTime-area");

        // Create first child div with text "Airline" and a background color
        const destDiv = document.createElement("div");
        destDiv.textContent = `${flightOffer.destination}`;
        destDiv.classList.add("durDiv");

        // Create second child div with text "logo" and a different background color
        const destTimeDiv = document.createElement("div");

        // console.log(length);
        const timeReturn = extractTimeFromDate(
          element.itineraries[0].segments[length].arrival.at
        );
        destTimeDiv.textContent = `${timeReturn}`;
        destTimeDiv.classList.add("destTimeDiv");

        // Append child divs to parent logoDiv
        arriTimeDiv.appendChild(destDiv);
        arriTimeDiv.appendChild(destTimeDiv);

        //--------------------------------------------------------------------------------------------------------------

        const priceDiv = document.createElement("div");
        priceDiv.classList.add("price-area");
        console.log(curencySymbol);
        priceDiv.textContent = `${markupCalculator(
          Number(element.price.grandTotal)
        )} ${curencySymbol}`; // Sample content

        // Append child div elements to the main container div
        fData.appendChild(logoDiv);
        fData.appendChild(locaTimeDiv);
        fData.appendChild(stopsDiv);
        fData.appendChild(arriTimeDiv);
        fData.appendChild(priceDiv);

        // Append the main container div to the container
        container.appendChild(fData);
        // =========================================================================(DATA ACTIVE)================================================================
        // Add event listener to the flight result div
        fData.addEventListener("click", function () {
          // Toggle active state
          handleClick(index, condition);
          if (fData.classList.contains("active")) {
            fData.classList.remove("active");
          } else {
            // Remove active class from all other flight result divs before setting this one as active
            const allFlightResults = document.querySelectorAll(".mainCont");
            allFlightResults.forEach((result) => {
              result.classList.remove("active");
            });
            fData.classList.add("active");
          }
        });
      });
      // =========================================================================(DATA ACTIVE)================================================================
    }
    if (type == "return" && data && data.flight_offers_return) {
      const condition = true;
      data.flight_offers_return.forEach((element, index) => {
        const container = document.getElementById("flightResultsReturn");

        // Create a div element for the main container
        const fData = document.createElement("div");
        fData.classList.add("mainCont");
        const length = element.itineraries[0].segments.length - 1;
        // Create parent div
        const logoDiv = document.createElement("div");
        logoDiv.classList.add("logo-area");

        //---------------------------------------------------------------------------------------------------------------

        // Create first child div with text "Airline" and a background color
        const airlineDiv = document.createElement("div");
        code =
          flightOffer.airlines[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];
        airlineDiv.textContent = `${code}`;
        airlineDiv.classList.add("airlineDiv");

        // Create second child div with text "logo" and a different background color
        const logoChildDiv = document.createElement("div");
        logoChildDiv.textContent = "Logo";
        logoChildDiv.classList.add("logoChildDiv");

        // .........................encryption .......................
        const inputText = `${element.itineraries[0].segments[0].carrierCode}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
        const hashedText = CryptoJS.MD5(inputText).toString();
        const temp =
          flightOffer.airlines2[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];

        console.log("re", temp);

        // logoChildDiv.innerHTML = `<img id='logoI' src="https://content.airhex.com/content/logos/airlines_${element.itineraries[0].segments[0].carrierCode}_2000_1000_t.png?md5apikey=${hashedText}">`;
        logoChildDiv.innerHTML = `<img id='logoI' src="https://thimpu.pythonanywhere.com/logo/api/airline/${temp}">`;
        logoChildDiv.classList.add("logoChildDiv");

        // Append child divs to parent logoDiv
        logoDiv.appendChild(airlineDiv);
        logoDiv.appendChild(logoChildDiv);

        //--------------------------------------------------------------------------------------------------------------

        const locaTimeDiv = document.createElement("div");
        locaTimeDiv.classList.add("locaTime-area");

        // Create first child div with text "Airline" and a background color
        const orDiv = document.createElement("div");
        orDiv.textContent = `${flightOffer.destination}`;
        orDiv.classList.add("orDiv");

        // Create second child div with text "logo" and a different background color
        const timeDiv = document.createElement("div");
        const timeDepart = extractTimeFromDate(
          element.itineraries[0].segments[0].departure.at
        );
        timeDiv.textContent = `${timeDepart}`;
        timeDiv.classList.add("timeDiv");

        // Append child divs to parent logoDiv
        locaTimeDiv.appendChild(orDiv);
        locaTimeDiv.appendChild(timeDiv);

        //--------------------------------------------------------------------------------------------------------------

        const stopsDiv = document.createElement("div");
        stopsDiv.classList.add("stops-area");

        // Create first child div with text "Airline" and a background color
        const durDiv = document.createElement("div");
        const duration = formatDuration(`${element.itineraries[0].duration}`);
        durDiv.textContent = `${duration}`;
        durDiv.classList.add("durDiv");

        //Create an arrow Div
        const arrowDiv = document.createElement("div");
        arrowDiv.textContent = "→";
        arrowDiv.classList.add("arrowDiv");

        // Create second child div with text "logo" and a different background color
        const stopDiv = document.createElement("div");
        stopDiv.textContent = `${length} stops`;
        stopDiv.classList.add("stopDiv");

        // Append child divs to parent logoDiv
        stopsDiv.appendChild(durDiv);
        stopsDiv.appendChild(arrowDiv);
        stopsDiv.appendChild(stopDiv);

        //--------------------------------------------------------------------------------------------------------------

        const arriTimeDiv = document.createElement("div");
        arriTimeDiv.classList.add("arriTime-area");

        // Create first child div with text "Airline" and a background color
        const destDiv = document.createElement("div");
        destDiv.textContent = `${flightOffer.origin}`;
        destDiv.classList.add("durDiv");

        // Create second child div with text "logo" and a different background color
        const destTimeDiv = document.createElement("div");

        // console.log(length);
        const timeReturn = extractTimeFromDate(
          element.itineraries[0].segments[length].arrival.at
        );
        destTimeDiv.textContent = `${timeReturn}`;
        destTimeDiv.classList.add("destTimeDiv");

        // Append child divs to parent logoDiv
        arriTimeDiv.appendChild(destDiv);
        arriTimeDiv.appendChild(destTimeDiv);

        //--------------------------------------------------------------------------------------------------------------

        const priceDiv = document.createElement("div");
        priceDiv.classList.add("price-area");
        console.log(curencySymbol);
        priceDiv.textContent = `${markupCalculator(
          Number(element.price.grandTotal)
        )} ${curencySymbol}`; // Sample content

        // Append child div elements to the main container div
        fData.appendChild(logoDiv);
        fData.appendChild(locaTimeDiv);
        fData.appendChild(stopsDiv);
        fData.appendChild(arriTimeDiv);
        fData.appendChild(priceDiv);

        // Append the main container div to the container
        container.appendChild(fData);

        // Add event listener to the flight result div
        fData.addEventListener("click", function () {
          // Toggle active state
          handleClick(index, condition);
          if (fData.classList.contains("active")) {
            fData.classList.remove("active");
          } else {
            // Remove active class from all other flight result divs before setting this one as active
            const allFlightResults = document.querySelectorAll(".mainCont");
            allFlightResults.forEach((result) => {
              result.classList.remove("active");
            });
            fData.classList.add("active");
          }
        });
      });
    }
  } else if (nonStopOption == true) {
    if (type == "departure" && data && data.flight_offers_departure) {
      const condition = false;
      data.flight_offers_departure.forEach((element, index) => {
        const container = document.getElementById("flightResults");

        // Create a div element for the main container
        const fData = document.createElement("div");
        fData.classList.add("mainCont");
        const length = element.itineraries[0].segments.length - 1;
        // Create parent div
        if (length > 0) {
          return;
        }
        const logoDiv = document.createElement("div");
        logoDiv.classList.add("logo-area");

        //---------------------------------------------------------------------------------------------------------------

        // Create first child div with text "Airline" and a background color
        const airlineDiv = document.createElement("div");
        code =
          flightOffer.airlines[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];
        console.log(element.itineraries[0].segments[0].carrierCode);
        airlineDiv.textContent = `${code}`;
        airlineDiv.classList.add("airlineDiv");

        // Create second child div with text "logo" and a different background color
        const logoChildDiv = document.createElement("div");
        const inputText = `${element.itineraries[0].segments[0].carrierCode}}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
        const hashedText = CryptoJS.MD5(inputText).toString();
        const temp =
          flightOffer.airlines2[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];

        // logoChildDiv.innerHTML = `<img id='logoI' src="https://content.airhex.com/content/logos/airlines_${element.itineraries[0].segments[0].carrierCode}_2000_1000_t.png?md5apikey=${hashedText}">`;
        logoChildDiv.innerHTML = `<img id='logoI' src="https://thimpu.pythonanywhere.com/logo/api/airline/${temp}">`;
        logoChildDiv.classList.add("logoChildDiv");

        // Append child divs to parent logoDiv
        logoDiv.appendChild(airlineDiv);
        logoDiv.appendChild(logoChildDiv);

        //--------------------------------------------------------------------------------------------------------------

        const locaTimeDiv = document.createElement("div");
        locaTimeDiv.classList.add("locaTime-area");

        // Create first child div with text "Airline" and a background color
        const orDiv = document.createElement("div");
        orDiv.textContent = `${flightOffer.origin}`;
        orDiv.classList.add("orDiv");

        // Create second child div with text "logo" and a different background color
        const timeDiv = document.createElement("div");
        const timeDepart = extractTimeFromDate(
          element.itineraries[0].segments[0].departure.at
        );
        timeDiv.textContent = `${timeDepart}`;
        timeDiv.classList.add("timeDiv");

        // Append child divs to parent logoDiv
        locaTimeDiv.appendChild(orDiv);
        locaTimeDiv.appendChild(timeDiv);

        // ---------------------------------------------------------------------------------------------------------------------

        const stopsDiv = document.createElement("div");
        stopsDiv.classList.add("stops-area");

        // Create first child div with text "Airline" and a background color
        const durDiv = document.createElement("div");
        const duration = formatDuration(`${element.itineraries[0].duration}`);
        durDiv.textContent = `${duration}`;
        durDiv.classList.add("durDiv");

        //Create an arrow Div
        const arrowDiv = document.createElement("div");
        arrowDiv.textContent = "→";
        arrowDiv.classList.add("arrowDiv");

        // Create second child div with text "logo" and a different background color
        const stopDiv = document.createElement("div");
        stopDiv.textContent = `${length} stops`;
        stopDiv.classList.add("stopDiv");

        // Append child divs to parent logoDiv
        stopsDiv.appendChild(durDiv);
        stopsDiv.appendChild(arrowDiv);
        stopsDiv.appendChild(stopDiv);

        //--------------------------------------------------------------------------------------------------------------

        const arriTimeDiv = document.createElement("div");
        arriTimeDiv.classList.add("arriTime-area");

        // Create first child div with text "Airline" and a background color
        const destDiv = document.createElement("div");
        destDiv.textContent = `${flightOffer.destination}`;
        destDiv.classList.add("durDiv");

        // Create second child div with text "logo" and a different background color
        const destTimeDiv = document.createElement("div");

        // console.log(length);
        const timeReturn = extractTimeFromDate(
          element.itineraries[0].segments[length].arrival.at
        );
        destTimeDiv.textContent = `${timeReturn}`;
        destTimeDiv.classList.add("destTimeDiv");

        // Append child divs to parent logoDiv
        arriTimeDiv.appendChild(destDiv);
        arriTimeDiv.appendChild(destTimeDiv);

        //--------------------------------------------------------------------------------------------------------------

        const priceDiv = document.createElement("div");
        priceDiv.classList.add("price-area");
        priceDiv.textContent = `${markupCalculator(
          Number(element.price.grandTotal)
        )} ${curencySymbol}`; // Sample content

        // Append child div elements to the main container div
        fData.appendChild(logoDiv);
        fData.appendChild(locaTimeDiv);
        fData.appendChild(stopsDiv);
        fData.appendChild(arriTimeDiv);
        fData.appendChild(priceDiv);

        // Append the main container div to the container
        container.appendChild(fData);

        // Add event listener to the flight result div
        fData.addEventListener("click", function () {
          // Toggle active state
          handleClick(index, condition);
          if (fData.classList.contains("active")) {
            fData.classList.remove("active");
          } else {
            // Remove active class from all other flight result divs before setting this one as active
            const allFlightResults = document.querySelectorAll(".mainCont");
            allFlightResults.forEach((result) => {
              result.classList.remove("active");
            });
            fData.classList.add("active");
          }
        });
      });
    }
    if (type == "return" && data && data.flight_offers_return) {
      const condition = true;
      data.flight_offers_return.forEach((element, index) => {
        const container = document.getElementById("flightResultsReturn");

        // Create a div element for the main container
        const fData = document.createElement("div");
        fData.classList.add("mainCont");
        const length = element.itineraries[0].segments.length - 1;
        // Create parent div
        if (length > 0) {
          return;
        }
        const logoDiv = document.createElement("div");
        logoDiv.classList.add("logo-area");

        //---------------------------------------------------------------------------------------------------------------

        // Create first child div with text "Airline" and a background color
        const airlineDiv = document.createElement("div");
        code =
          flightOffer.airlines[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];
        airlineDiv.textContent = `${code}`;
        airlineDiv.classList.add("airlineDiv");

        // Create second child div with text "logo" and a different background color
        const logoChildDiv = document.createElement("div");
        const inputText = `${element.itineraries[0].segments[0].carrierCode}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
        const hashedText = CryptoJS.MD5(inputText).toString();
        const temp =
          flightOffer.airlines2[
            `${element.itineraries[0].segments[0].carrierCode}`
          ];

        // logoChildDiv.innerHTML = `<img id='logoI' src="https://content.airhex.com/content/logos/airlines_${element.itineraries[0].segments[0].carrierCode}_2000_1000_t.png?md5apikey=${hashedText}">`;
        logoChildDiv.innerHTML = `<img id='logoI' src="https://thimpu.pythonanywhere.com/logo/api/airline/${temp}">`;
        logoChildDiv.classList.add("logoChildDiv");

        // Append child divs to parent logoDiv
        logoDiv.appendChild(airlineDiv);
        logoDiv.appendChild(logoChildDiv);

        //--------------------------------------------------------------------------------------------------------------

        const locaTimeDiv = document.createElement("div");
        locaTimeDiv.classList.add("locaTime-area");

        // Create first child div with text "Airline" and a background color
        const orDiv = document.createElement("div");
        orDiv.textContent = `${flightOffer.destination}`;
        orDiv.classList.add("orDiv");

        // Create second child div with text "logo" and a different background color
        const timeDiv = document.createElement("div");
        const timeDepart = extractTimeFromDate(
          element.itineraries[0].segments[0].departure.at
        );
        timeDiv.textContent = `${timeDepart}`;
        timeDiv.classList.add("timeDiv");

        // Append child divs to parent logoDiv
        locaTimeDiv.appendChild(orDiv);
        locaTimeDiv.appendChild(timeDiv);

        //--------------------------------------------------------------------------------------------------------------

        const stopsDiv = document.createElement("div");
        stopsDiv.classList.add("stops-area");

        // Create first child div with text "Airline" and a background color
        const durDiv = document.createElement("div");
        const duration = formatDuration(`${element.itineraries[0].duration}`);
        durDiv.textContent = `${duration}`;
        durDiv.classList.add("durDiv");

        //Create an arrow Div
        const arrowDiv = document.createElement("div");
        arrowDiv.textContent = "→";
        arrowDiv.classList.add("arrowDiv");

        // Create second child div with text "logo" and a different background color
        const stopDiv = document.createElement("div");
        stopDiv.textContent = `${length} stops`;
        stopDiv.classList.add("stopDiv");

        // Append child divs to parent logoDiv
        stopsDiv.appendChild(durDiv);
        stopsDiv.appendChild(arrowDiv);
        stopsDiv.appendChild(stopDiv);

        //--------------------------------------------------------------------------------------------------------------

        const arriTimeDiv = document.createElement("div");
        arriTimeDiv.classList.add("arriTime-area");

        // Create first child div with text "Airline" and a background color
        const destDiv = document.createElement("div");
        destDiv.textContent = `${flightOffer.origin}`;
        destDiv.classList.add("durDiv");

        // Create second child div with text "logo" and a different background color
        const destTimeDiv = document.createElement("div");

        // console.log(length);
        const timeReturn = extractTimeFromDate(
          element.itineraries[0].segments[length].arrival.at
        );
        destTimeDiv.textContent = `${timeReturn}`;
        destTimeDiv.classList.add("destTimeDiv");

        // Append child divs to parent logoDiv
        arriTimeDiv.appendChild(destDiv);
        arriTimeDiv.appendChild(destTimeDiv);

        //--------------------------------------------------------------------------------------------------------------

        const priceDiv = document.createElement("div");
        priceDiv.classList.add("price-area");
        priceDiv.textContent = `${markupCalculator(
          Number(element.price.grandTotal)
        )} ${curencySymbol}`; // Sample content

        // Append child div elements to the main container div
        fData.appendChild(logoDiv);
        fData.appendChild(locaTimeDiv);
        fData.appendChild(stopsDiv);
        fData.appendChild(arriTimeDiv);
        fData.appendChild(priceDiv);

        // Append the main container div to the container
        container.appendChild(fData);

        // Add event listener to the flight result div
        fData.addEventListener("click", function () {
          // Toggle active state
          handleClick(index, condition);
          if (fData.classList.contains("active")) {
            fData.classList.remove("active");
          } else {
            // Remove active class from all other flight result divs before setting this one as active
            const allFlightResults = document.querySelectorAll(".mainCont");
            allFlightResults.forEach((result) => {
              result.classList.remove("active");
            });
            fData.classList.add("active");
          }
        });
      });
    }
  }
}
//--------------------------------------------------------------------------------------------------------------

function handleClick(index, condition) {
  // Log the selected index based on the condition
  if (condition === false) {
    console.log("Selected Departure Index:", index);
  } else {
    console.log("Selected Return Index:", index);
  }
  if (condition === false) {
    // If condition is false, replace the array with the selected departure flight offer
    selectedFlight["flight_offers_departure"] = [
      flightOffer.flight_offers_departure[index],
    ];
    const deplength =
      selectedFlight.flight_offers_departure[0].itineraries[0].segments.length -
      1;
    const air = document.getElementById("airline");
    const logoDeprtElement = document.getElementById("departLogo");
    const code =
      selectedFlight.flight_offers_departure[0].itineraries[0].segments[0]
        .carrierCode;
    // console.log(code);
    const temp =
      flightOffer.airlines2[
        `${selectedFlight.flight_offers_departure[0].itineraries[0].segments[0].carrierCode}`
      ];

    const inputText = `${code}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
    const hashedText = CryptoJS.MD5(inputText).toString();

    logoDeprtElement.src = `https://thimpu.pythonanywhere.com/logo/api/airline/${temp}`;
    logoDeprtElement.alt = `logo`;
    air.textContent = `${flightOffer.origin}`;
    const dtime = document.getElementById("dtime");
    dtime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_departure[0].itineraries[0].segments[0].departure.at}`
      )
    );
    const atime = document.getElementById("atime");
    atime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_departure[0].itineraries[0].segments[deplength].arrival.at}`
      )
    );
  } else {
    // If condition is true, replace the array with the selected return flight offer
    selectedFlight["flight_offers_return"] = [
      flightOffer.flight_offers_return[index],
    ];
    const retlength =
      selectedFlight.flight_offers_return[0].itineraries[0].segments.length - 1;
    const rair = document.getElementById("rairline");
    const logoReturnElement = document.getElementById("returnLogo");
    const code =
      selectedFlight.flight_offers_return[0].itineraries[0].segments[0]
        .carrierCode;
    // console.log(code);
    const temp =
      flightOffer.airlines2[
        `${selectedFlight.flight_offers_return[0].itineraries[0].segments[0].carrierCode}`
      ];

    const inputText = `${code}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
    const hashedText = CryptoJS.MD5(inputText).toString();
    // logoReturnElement.src = `https://content.airhex.com/content/logos/airlines_${code}_2000_1000_t.png?md5apikey=${hashedText}`;
    logoReturnElement.src = `https://thimpu.pythonanywhere.com/logo/api/airline/${temp}`;
    logoReturnElement.alt = `logo`;
    rair.textContent = `${flightOffer.destination}`;
    const rdtime = document.getElementById("rdtime");
    rdtime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_return[0].itineraries[0].segments[0].departure.at}`
      )
    );
    const ratime = document.getElementById("ratime");
    ratime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_return[0].itineraries[0].segments[retlength].arrival.at}`
      )
    );
  }
  console.log(selectedFlight);

  var modal = document.getElementById("totalPriceModal");
  modal.style.display = "block";
  var departPrice = document.getElementById("departurePrice");
  var returnPrice = document.getElementById("returnPrice");
  var totalPrice = document.getElementById("totalPrice");

  // Check the length of departure flight offers
  const departureLength = selectedFlight.flight_offers_departure.length;

  // Check the length of return flight offers
  const returnLength = selectedFlight.flight_offers_return.length;

  if (departureLength > 0) {
    // Display departure price
    departPrice.textContent = `${markupCalculator(
      selectedFlight.flight_offers_departure[0].price.total
    )} ${curencySymbol}`;
    totalPrice.textContent = Number(
      markupCalculator(selectedFlight.flight_offers_departure[0].price.total)
    ).toFixed(2);

    if (returnLength > 0) {
      // Add return price if available
      returnPrice.textContent = `${markupCalculator(
        selectedFlight.flight_offers_return[0].price.total
      )} ${curencySymbol}`;
      totalPrice.textContent += Number(
        Number(totalPrice.textContent) +
          Number(
            markupCalculator(selectedFlight.flight_offers_return[0].price.total)
          )
      ).toFixed(2);
    }
    totalPrice.textContent += ` ${curencySymbol}`;
  }
}

async function check_available() {
  // const data = await search_flight();
  // const jsonData = data.flight_offers_departure[index];
  const jsonData = selectedFlight;
  // const departureDate = document.getElementById("departureDate");
  // const returnDate = document.getElementById("returnDate");
  // const originIataCode = document.getElementById("originIataCode").value;
  // const adult = document.getElementById("adults").value;
  // const children = document.getElementById("children").value;
  // const infants = document.getElementById("infants").value;
  // const destinationIataCode = document.getElementById(
  //   "destinationIataCode"
  // ).value;
  // // jsonData = data[index]
  const searchAvailURLComponent = document.getElementById(
    "searchAvailable-url"
  );
  const apiEndpointSearch =
    searchAvailURLComponent.getAttribute("data-base-url");
  // const apiEndpointSearch = '{% url 'flightbooking:search_available' %}';
  const response = await fetch(`${apiEndpointSearch}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(jsonData),
  });
  const responseData = await response.json();
  console.log("this is ", responseData);
  if (responseData.status === 400) {
    console.log(responseData[0].detail);
  } else {
    console.log(responseData);
    const queryString = `json_data=${encodeURIComponent(
      JSON.stringify(responseData.flightOffers)
    )}`;

    // Use Django template tag to generate the URL
    const customURLComponent = document.getElementById("customCredentials-url");
    const customCredentialsURL =
      customURLComponent.getAttribute("data-base-url");
    // Convert the JSON data to a string using JSON.stringify
    const flightsData = {
      departureFlight: responseData.departureFlight,
      returnFlight: responseData.returnFlight,
      airlines: flightOffer.airlines,
      bookingRequirements: responseData.bookingRequirements,
      // seats: responseData.seats,
    };

    // Convert the JSON object to a string using JSON.stringify
    const jsonString = JSON.stringify(flightsData);

    // Store the string in local storage with a specific key
    localStorage.setItem("flightsData", jsonString);

    console.log("Flights data has been stored in local storage.");
    console.log(responseData);
    // To retrieve the data later

    window.location.href = `${customCredentialsURL}?${queryString}`;
  }
  // const customCredentialsURL = `{% url 'flightbooking:customCredentials' %}';

  // console.log("Response data:", response);
}

document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("apply").addEventListener("click", function () {
    // Get the selected sort option
    var sortOption = document.querySelector('input[name="sortOption"]:checked');

    // Get the value of non-stop checkbox
    nonStopOption = document.getElementById("nonStopOption").checked;

    // Display the selected values (you can modify this part based on your use case)
    if (sortOption) {
      console.log("Sort Option: " + sortOption.value);
    } else {
      console.log("Sort Option not selected");
    }

    console.log("Non-stop Option: " + nonStopOption);
    clearFlightResults();
    displayFlightResults(flightOffer, "departure");
  });
});

// ---------------------------------------------------------------------------------------------------------------------------------------

function displayFootAir() {
  var ret = document.querySelector(".returnAirline");
  ret.style.display = "block";
}
// =================================================================================================

document.addEventListener("DOMContentLoaded", function () {
  var airlineList = Object.keys(flightOffer.airlines);
  var airlineListVal = Object.values(flightOffer.airlines);
  var airlineListDiv = document.getElementById("airlineList");

  if (airlineListDiv) {
    var length = airlineList.length;
    console.log("Airline has " + length + " Airlines");

    // Create checkboxes and spans for each airline
    var checkboxesHTML = "";
    for (var i = 0; i < airlineList.length; i++) {
      checkboxesHTML +=
        '<div style="font-size: 0.8rem; display: flex; justify-content: space-between; align-items: center;"><div class="cinp"><input type="checkbox" name="selectedAirlines" value="' +
        airlineListVal[i] +
        '"> ' +
        airlineListVal[i] +
        '</div><div class="lowest-price">Loading...</div></div><br>';
    }

    airlineListDiv.innerHTML =
      "<strong>Filter Flights</strong><br><br>" + checkboxesHTML;

    console.log("Here is the airline list: " + airlineList);

    var codeLength = flightOffer.flight_offers_departure.length;

    // Array to store carrier codes and prices
    const carrierPrices = [];

    for (let i = 0; i < codeLength; i++) {
      const currentCarrierCode =
        flightOffer.flight_offers_departure[i].itineraries[0].segments[0]
          .carrierCode;
      const currentPrice =
        flightOffer.flight_offers_departure[i].price.grandTotal;

      carrierPrices.push({
        carrierCode: currentCarrierCode,
        price: currentPrice,
      });
    }

    // Sort carrierPrices array based on prices in ascending order
    carrierPrices.sort((a, b) => a.price - b.price);

    // Create an object to store the lowest price for each carrier code
    const lowestPriceByCarrierCode = {};

    // Populate lowestPriceByCarrierCode with the lowest price for each carrier code
    carrierPrices.forEach((item) => {
      if (!lowestPriceByCarrierCode[item.carrierCode]) {
        lowestPriceByCarrierCode[item.carrierCode] = item.price;
      }
    });

    // Update the spans with the lowest prices
    var spans = document.querySelectorAll(".lowest-price");
    spans.forEach((span, index) => {
      var carrierCode = airlineList[index];
      span.textContent =
        lowestPriceByCarrierCode[carrierCode] !== undefined
          ? lowestPriceByCarrierCode[carrierCode] + " " + flightOffer.symbol
          : "N/A";
    });

    console.log(carrierPrices);
    console.log(lowestPriceByCarrierCode);
  } else {
    console.error("Element with ID 'airlineList' not found.");
  }
});

// ---------------------------------------------------------------------------------------------------------------------------------------
function getCookie(name) {
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

// calculate prices with markups
function markupCalculator(price) {
  var total = 0;
  if ("amount" in flightOffer.markup) {
    total = Number(price) + flightOffer.markup.amount;
    // console.log("amount");
  }
  if ("percentage" in flightOffer.markup) {
    var addMarkup = (Number(price) * flightOffer.markup.percentage) / 100;
    total = Number(price) + addMarkup;
    // console.log("percentage");
  }
  return total;
}

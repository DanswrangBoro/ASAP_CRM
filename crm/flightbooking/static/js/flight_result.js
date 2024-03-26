function displayFlightOffers(data) {
  const flightOffersContainer = document.getElementById(
    "flightOffersContainer"
  );
  //   flightOffersContainer.classList.add("tableHolder");
  const originCode = origin;
  const departDate = formatDateString(departure_date);
  console.log("hello", departDate);
  const returnDate = formatDateString(return_date);
  console.log("hello", returnDate);
  // const originCityName = extractCityName(originCode.value)
  const destinationCode = destination;
  // Clear previous content
  //   flightOffersContainer.innerHTML = "";

  // Check if there are flight offers to display
  if (data && data.flight_offers_departure) {
    const departureTable = createFlightTable(
      data.flight_offers_departure,
      false
    );
    const table1 = document.createElement("div");
    table1.classList.add("table1");

    const tableHead1 = document.createElement("div");
    tableHead1.classList.add("tableHead1");

    //Create table head1 child div
    const tableHead1Child1 = document.createElement("div");
    tableHead1Child1.classList.add("tHC1");

    //Creating more childs inside tHC1
    const originDestination = document.createElement("div");
    originDestination.classList.add("originDestination");

    const originTravelDate = document.createElement("div");
    originTravelDate.classList.add("originTravelDate");

    //append originDestination & originTravelDate in tHC1
    tableHead1Child1.appendChild(originDestination);

    //create content inside originDestination
    var originPara = document.createElement("p");
    originPara.textContent = originCode;

    var originDestinationSpan = document.createElement("span");
    originDestinationSpan.textContent = "→";

    var destinationPara = document.createElement("p");
    destinationPara.textContent = destinationCode;

    //append para and span in originDestination div

    originDestination.appendChild(originPara);
    originDestination.appendChild(originDestinationSpan);
    originDestination.appendChild(destinationPara);

    tableHead1Child1.appendChild(originTravelDate);

    //create content inside originTravelDate

    var originTravelDatePara = document.createElement("p");
    originTravelDatePara.textContent = departDate;
    originTravelDatePara.style.float = "right";

    //append para in originTravelDate

    originTravelDate.appendChild(originTravelDatePara);

    const tableHead1Child2 = document.createElement("div");
    tableHead1Child2.classList.add("tHC2");

    flightOffersContainer.appendChild(table1);

    table1.appendChild(tableHead1);
    tableHead1.appendChild(tableHead1Child1);

    tableHead1.appendChild(tableHead1Child2);

    //create content inside tableHead1Child2

    const myLabelTable1 = document.createElement("label");
    myLabelTable1.setAttribute("for", "sort-options");
    myLabelTable1.textContent = "Sort By:";

    const sortRecommendedTable1 = document.createElement("a");
    sortRecommendedTable1.classList.add("recommend");
    sortRecommendedTable1.textContent = "Recommended";
    sortRecommendedTable1.style.textDecoration = "none";
    sortRecommendedTable1.style.color = "black";

    const sortCheapestTable1 = document.createElement("a");
    sortCheapestTable1.classList.add("cheap");
    sortCheapestTable1.textContent = "Cheapeast";
    sortCheapestTable1.style.textDecoration = "none";
    sortCheapestTable1.style.color = "black";

    const sortFilterTable1 = document.createElement("a");
    sortFilterTable1.classList.add("filter");
    sortFilterTable1.textContent = "Filter";
    sortFilterTable1.style.textDecoration = "none";
    sortFilterTable1.style.color = "black";

    //append created content for TableHead1Child2

    tableHead1Child2.appendChild(myLabelTable1);
    tableHead1Child2.appendChild(sortRecommendedTable1);
    tableHead1Child2.appendChild(sortCheapestTable1);
    tableHead1Child2.appendChild(sortFilterTable1);

    table1.appendChild(departureTable);
  }

  if (data && data.flight_offers_return) {
    const returnTable = createFlightTable(data.flight_offers_return, true);

    const table2 = document.createElement("div");
    table2.classList.add("table2");

    const tableHead2 = document.createElement("div");
    tableHead2.classList.add("tableHead2");

    //Create table head1 child div
    const tableHead2Child1 = document.createElement("div");
    tableHead2Child1.classList.add("tH2C1");

    //Creating more childs inside tH2C1
    const originReturnDestination = document.createElement("div");
    originReturnDestination.classList.add("originReturnDestination");

    const returnTravelDate = document.createElement("div");
    returnTravelDate.classList.add("returnTravelDate");

    //append originReturnDestination & returnTravelDate in tH2C1
    tableHead2Child1.appendChild(originReturnDestination);

    //create content inside originReturnDestination
    var returnPara = document.createElement("p");
    returnPara.textContent = destinationCode;

    var originReturnDestinationSpan = document.createElement("span");
    originReturnDestinationSpan.textContent = "→";

    var returnDestinationPara = document.createElement("p");
    returnDestinationPara.textContent = originCode;

    //append para and span in originDestination div

    originReturnDestination.appendChild(returnPara);
    originReturnDestination.appendChild(originReturnDestinationSpan);
    originReturnDestination.appendChild(returnDestinationPara);

    tableHead2Child1.appendChild(returnTravelDate);

    //create content inside returnTravelDate

    var originReturnTravelDatePara = document.createElement("p");
    originReturnTravelDatePara.textContent = returnDate;
    originReturnTravelDatePara.style.float = "right";

    //append para in originTravelDate

    returnTravelDate.appendChild(originReturnTravelDatePara);

    const tableHead2Child2 = document.createElement("div");
    tableHead2Child2.classList.add("tH2C2");

    flightOffersContainer.appendChild(table2);

    table2.appendChild(tableHead2);
    tableHead2.appendChild(tableHead2Child1);
    tableHead2.appendChild(tableHead2Child2);

    //create content inside tableHead1Child2

    const myLabelTable2 = document.createElement("label");
    myLabelTable2.setAttribute("for", "sort-options");
    myLabelTable2.textContent = "Sort By:";

    const sortRecommendedTable2 = document.createElement("a");
    sortRecommendedTable2.classList.add("recommend");
    sortRecommendedTable2.textContent = "Recommended";
    sortRecommendedTable2.style.textDecoration = "none";
    sortRecommendedTable2.style.color = "black";

    const sortCheapestTable2 = document.createElement("a");
    sortCheapestTable2.classList.add("cheap");
    sortCheapestTable2.textContent = "Cheapeast";
    sortCheapestTable2.style.textDecoration = "none";
    sortCheapestTable2.style.color = "black";

    const sortFilterTable2 = document.createElement("a");
    sortFilterTable2.classList.add("filter");
    sortFilterTable2.textContent = "Filter";
    sortFilterTable2.style.textDecoration = "none";
    sortFilterTable2.style.color = "black";

    //append created content for TableHead1Child2

    tableHead2Child2.appendChild(myLabelTable2);
    tableHead2Child2.appendChild(sortRecommendedTable2);
    tableHead2Child2.appendChild(sortCheapestTable2);
    tableHead2Child2.appendChild(sortFilterTable2);

    table2.appendChild(returnTable);
  }
}

function createFlightTable(flightOffers, condition) {
  const destinationCodeInputSearch = destination;
  const originCodeInputSearch = origin;
  console.log(flightOffers[0]);

  const table = document.createElement("table");
  table.classList.add("table");

  // Create table header
  const thead = document.createElement("thead");
  thead.classList.add("thead-dark");

  const headerRow = document.createElement("tr");
  headerRow.innerHTML =
    '<th scope="col">Select</th><th scope="col">Airline</th><th scope="col">Departure Airport</th><th scope="col">Duration</th><th scope="col">Arrival Airport</th>';
  thead.appendChild(headerRow);
  table.appendChild(thead);

  // Create table body
  const tbody = document.createElement("tbody");

  flightOffers.forEach((offer, index) => {
    const row = document.createElement("tr");

    // Create a single radio button for the entire set of segments
    const radioInput = document.createElement("input");
    radioInput.type = "radio";
    radioInput.name = condition ? "returnRadioGroup" : "departureRadioGroup";
    radioInput.id = condition
      ? `returnRadio-${index}`
      : `departureRadio-${index}`;
    radioInput.setAttribute(
      "onclick",
      `handleRadioClick(${index}, ${condition})`
    );
    offer.itineraries[0].segments.forEach((segment, index) => {
      const row = document.createElement("tr");

      if (index === 0) {
        // Only append the radio button to the first row
        const radioCell = document.createElement("td");
        radioCell.appendChild(radioInput);
        row.appendChild(radioCell);
      } else {
        // For subsequent rows, add an empty cell for consistency
        row.appendChild(document.createElement("td"));
      }

      /* console.log("Segment Information:");
          console.log(`Departure: ${segment.departure.iataCode}`);
          console.log(`Arrival: ${segment.arrival.iataCode}`);
          console.log(`Carrier: ${segment.carrierCode} ${segment.number}`);
          console.log(`Aircraft: ${segment.aircraft.code}`);
          console.log(`Duration: ${segment.duration}`);
          console.log(`Number of Stops: ${segment.numberOfStops}`);
          console.log("------------");*/

      const airlineName = `${segment.carrierCode} ${segment.number}`;
      const departureAirport = `${segment.departure.iataCode}`;
      const departureDuration = `${segment.duration}`;
      const durationFormat = formatDuration(departureDuration);
      const arrivalAirport = `${segment.arrival.iataCode}`;
      const departureTime = `${segment.departure.at}`;
      const dateTimeFormatDeparture = formatDateTime(departureTime);
      const arrivalTime = `${segment.arrival.at}`;
      const dateTimeFormatArrival = formatDateTime(arrivalTime);

      row.innerHTML += `<td scope="row">
                            <p>${airlineName}</P>
                            <p><img id="tail-logo" src="https://img.freepik.com/free-psd/view-3d-supply-chain-representation-illustration_23-2150766713.jpg?w=900&t=st=1702728805~exp=1702729405~hmac=e4173be99d86f27bde5f75cb7204278006b22bef6a56f494656e8b368ac4ee68"></p>
                          </td>
                          <td scope="row">
                            <p>${departureAirport}</p>
                            <p>${dateTimeFormatDeparture}</P>
                          </td>
                          <td scope="row">${durationFormat}</td>
                          <td scope="row">
                            <p>${arrivalAirport}</p>
                            <p>${dateTimeFormatArrival}</p>
                          </td>`;
      tbody.appendChild(row);
    });

    const price = offer.price ? offer.price.total : "N/A";
    row.innerHTML += `<td scope="row">${price}</td>`;
    tbody.appendChild(row);
  });
  table.appendChild(tbody);
  return table;
}
//global variable
const selectedFlight = {
  flight_offers_departure: [], // Array to store selected departure flight offers
  flight_offers_return: [], // Array to store selected return flight offers
};

function handleRadioClick(index, condition) {
  if (condition === false) {
    // If condition is false, replace the array with the selected departure flight offer
    selectedFlight["flight_offers_departure"] = [
      selectionVariableData.flight_offers_departure[index],
    ];
    const air = document.getElementById("airline");
    air.textContent = `${selectedFlight.flight_offers_departure[0].itineraries[0].segments[0].carrierCode}`;
    const dtime = document.getElementById("dtime");
    dtime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_departure[0].itineraries[0].segments[0].departure.at}`
      )
    );
    const atime = document.getElementById("atime");
    atime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_departure[0].itineraries[0].segments[0].arrival.at}`
      )
    );
  } else {
    // If condition is true, replace the array with the selected return flight offer
    selectedFlight["flight_offers_return"] = [
      selectionVariableData.flight_offers_return[index],
    ];
    const rair = document.getElementById("rairline");
    rair.textContent = `${selectedFlight.flight_offers_return[0].itineraries[0].segments[0].carrierCode}`;
    const rdtime = document.getElementById("rdtime");
    rdtime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_return[0].itineraries[0].segments[0].departure.at}`
      )
    );
    const ratime = document.getElementById("ratime");
    ratime.textContent = extractTimeFromDate(
      formatDateTime(
        `${selectedFlight.flight_offers_return[0].itineraries[0].segments[0].arrival.at}`
      )
    );
  }
  console.log(selectedFlight);
  var modal = document.getElementById("totalPriceModal");
  modal.style.display = "block";
  var departPrice = document.getElementById("departurePrice");
  var returnPrice = document.getElementById("returnPrice");
  var totalPrice = document.getElementById("totalPrice");

  departPrice.textContent = `${selectedFlight.flight_offers_departure[0].price.total} ${selectedFlight.flight_offers_departure[0].price.currency}`;
  returnPrice.textContent = `${selectedFlight.flight_offers_return[0].price.total} ${selectedFlight.flight_offers_return[0].price.currency}`;
  totalPrice.textContent = Number(
    Number(selectedFlight.flight_offers_departure[0].price.total) +
      Number(selectedFlight.flight_offers_return[0].price.total)
  ).toFixed(2);
}

async function check_available() {
  // const data = await search_flight();
  // const jsonData = data.flight_offers_departure[index];
  const jsonData = selectedFlight;
  const departureDate = document.getElementById("departureDate");
  const returnDate = document.getElementById("returnDate");
  const originIataCode = document.getElementById("originIataCode").value;
  const adult = document.getElementById("adults").value;
  const children = document.getElementById("children").value;
  const infants = document.getElementById("infants").value;
  const destinationIataCode = document.getElementById(
    "destinationIataCode"
  ).value;
  // jsonData = data[index]
  const searchAvailURLComponent = document.getElementById(
    "searchAvailable-url"
  );
  const apiEndpointSearch =
    searchAvailURLComponent.getAttribute("data-base-url");
  // const apiEndpointSearch = '{% url 'flightbooking:search_available' %}';
  try {
    const response = await fetch(`${apiEndpointSearch}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify(jsonData),
    });

    if (!response.ok) {
      throw new Error(response);
    }
    const responseData = await response.json();
    console.log(responseData);
    const queryString = `json_data=${encodeURIComponent(
      JSON.stringify(responseData)
    )}&departureDate=${encodeURIComponent(
      JSON.stringify(departureDate.value)
    )}&returnDate=${encodeURIComponent(
      JSON.stringify(returnDate.value)
    )}&origin=${encodeURIComponent(
      JSON.stringify(originIataCode)
    )}&destination=${encodeURIComponent(
      JSON.stringify(destinationIataCode)
    )}&adults=${encodeURIComponent(adult)}&children=${encodeURIComponent(
      children
    )}&infants=${encodeURIComponent(infants)}`;

    // Use Django template tag to generate the URL
    const customURLComponent = document.getElementById("customCredentials-url");
    const customCredentialsURL =
      customURLComponent.getAttribute("data-base-url");
    // const customCredentialsURL = `{% url 'flightbooking:customCredentials' %}';

    // Redirect to the generated URL with query parameters
    window.location.href = `${customCredentialsURL}?${queryString}`;
    // console.log("Response data:", response);
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

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

// Check if the elements exist before attempting to hide them

// Show Element Label & Input

// Handle Select Change
function handleSelectChange() {
  const selectedOption = document.querySelector(".typeTrip").value;

  if (selectedOption === "One Way") {
    hideElements();
  } else if (selectedOption === "Round Trip") {
    showElements();
  } else if (selectedOption === "Multi-City") {
    multiDisplay();
  }
}

// Hide elements by default when the page loads

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

displayFlightOffers(flightOffer);

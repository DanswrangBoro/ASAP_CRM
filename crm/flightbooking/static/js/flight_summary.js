// =============================================================(fetch data)==============================================================================================
const data1 = JSON.parse(localStorage.getItem("order-data"));
const airlines = JSON.parse(localStorage.getItem("airline"));
console.log(data1);
console.log(airlines);
const data = data1.flight_order_data;
console.log(data);
var no = data.flightOffers.length;
console.log("Length is " + no);
// console.log(data.user_Address)
// ===============================================================(ending data fetch)============================================================================================

// Create a div element with class "bs"
var dynamicDiv = document.createElement("div");
dynamicDiv.className = "bs";

// Set inner HTML for the "bs" div
dynamicDiv.innerHTML = `<h2>BOOKING SUMMARY</h2>`;

for (let i = 0; i < no; i++) {
  // Format the date
  const segmentlength = data.flightOffers[i].itineraries[0].segments.length;

  for (let j = 0; j < segmentlength; j++) {
    const departureDate = new Date(
      data.flightOffers[i].itineraries[0].segments[j].departure.at
    );
    const formattedDate = `${getDayName(
      departureDate.getDay()
    )} , ${getMonthName(
      departureDate.getMonth()
    )} ${departureDate.getDate()} , ${departureDate.getFullYear()}`;
    const terValue =
      data.flightOffers[i]?.itineraries[0]?.segments[j]?.departure?.terminal ||
      "Not specified";
    const departureTime = extractTime(
      data.flightOffers[i].itineraries[0].segments[j].departure.at
    );

    dynamicDiv.innerHTML += `
              <div class="flight">
                <div class="departing">
                  <div class="iTholder">
                    <div class="iSpaceHolder">
                      <div class="iSpace">
                        <div class="iconReview">
                          <img src="https://thimpu.pythonanywhere.com/logo/api/airline/${
                            airlines[
                              data.flightOffers[i].itineraries[0].segments[j]
                                .carrierCode
                            ]
                          }" alt="airline-icon" />
                        </div>
                        <div class="iconText">
                          <p id="aName">${
                            data.flightOffers[i].itineraries[0].segments[j]
                              .carrierCode
                          }</p>
                          <p id="aNumber">Flight <span id="no">${
                            data.flightOffers[i].itineraries[0].segments[j]
                              .number
                          }</span></p>
                          <p id="airCraft">Aircraft <span id="airNo">${
                            data.flightOffers[i].itineraries[0].segments[j]
                              .aircraft.code
                          }</span></p>
                        </div>
                      </div>
                      <div class="operationText">
                        <p>${data.flightOffers[i].aircraftModel}</p>
                        <p>${data.flightOffers[i].seatInfo}</p>
                        <p>Operated by <span id="aName">${
                          data.flightOffers[i].operatedBy
                        }</span></p>
                        <p>Stops|Cabin: ${
                          data.flightOffers[i].itineraries[0].segments.length -
                          1
                        } | ${
      data.flightOffers[i].travelerPricings[0].fareDetailsBySegment[0].cabin
    }</p>
                      </div>
                    </div>
                    <div class="tSpace">
                      <div class="sumDate">${formattedDate}</div>
                      <div class="sumOrDept">${
                        data.flightOffers[i].itineraries[0].segments[j]
                          .departure.iataCode
                      } to ${
      data.flightOffers[i].itineraries[0].segments[j].arrival.iataCode
    }</div>
                      <div class="showDest">${
                        data.flightOffers[i].itineraries[0].segments[j]
                          .departure.iataCode
                      } to ${
      data.flightOffers[i].itineraries[0].segments[j].arrival.iataCode
    }</div>
                      <div class="sumTerminal">Terminal : ${terValue}</div>
                      <div class="sumDeptTime">Departing Time : ${departureTime}</div>
                    </div>
                  </div>
                </div>
              </div>
            `;
  }
}

// Calculate total cost
var totalCost = data1.total_base + data1.baggage_fee + data1.seat_selection_fee;
var taxCost =
  data1.airport_tax + data1.security_fee + data1.agency_fee + data1.other_fees;
var grandCost = totalCost + taxCost;

const travelersSize = data.travelers.length;
console.log(`Number of travelers for this flight offer: ${travelersSize}`);
// console.log(data.flightOffers[0].travelerPricings[2].travelerType);

dynamicDiv.innerHTML += `
    <div class="travelerInformation">
      <h3>Traveller Information</h3>
      <table>
      <thead>
        <th></th>
        <th>Traveller Name</th>
        <th>DOB</th>
        <th>Traveller Type</th>
        <th>Gender</th>
      </thead>
      <tbody>
      ${data.travelers
        .map((traveler, index) => {
          const flightOffer = data.flightOffers[0];
          console.log(index);
          const flightOfferTravelerType =
            flightOffer?.travelerPricings[index]?.travelerType ||
            "Not Specified";

          return `
          <tr>
            <td>${index + 1}</td>
            <td>${traveler.name.firstName} ${traveler.name.lastName}</td>
            <td>${traveler.dateOfBirth}</td>
            <td>${flightOfferTravelerType}</td>
            <td>${traveler.gender || "undefined"}</td>
          </tr>
        `;
        })
        .join("")}
    </tbody>
    </table>
      <br/><br/>
      <h3>Selected Seat</h3>
      <table>
        <thead>
          <th></th>
          <th>Traveller Name</th>
          <th>Departure Seat</th>
          <th>Returning Seat</th>
          <th>Dynamic Add</th>
        </thead>
        <tbody>
        ${data.travelers
          .map((traveler, index) => {
            return `
          <tr>
            <td>${index + 1}</td>
            <td>${traveler.name.firstName} ${traveler.name.lastName}</td>
            <td>16C</td>
            <td>17M</td>
            <td>Smile Please</td>
          </tr>`;
          })
          .join("")}
        </tbody>
      </table>
      </table>
      <br/><br/>
      <h3>Contact Details</h3>
      <table>
        <thead>
          <th>Email</th>
          <th>Phone no</th>
          <th>Address</th>
          <th>City</th>
          <th>Zip code</th>
        </thead>
        <tbody>
        <tr>
          <td>${data.travelers[0]?.contact?.emailAddress || ""}</td>
          <td>+${
            data.travelers[0]?.contact?.phones[0]?.countryCallingCode || ""
          } ${data.travelers[0]?.contact?.phones[0]?.number || ""}</td>
          <td>${data1.user_Address.address}</td>
          <td>${data1.user_Address.city}</td>
          <td>${data1.user_Address.zip}</td>
        </tr>
      </tbody>

      </table>
    </div>

    <div class="pricingDetails">
    <h3>Pricing Details<span id="openBrace">（</span><span id="currency">USD</span><span id="closeBrace">）</span></h3>
    <hr id="pricingLine" />
  
    <div class="tPrice">
      <p id="tText">Total price</p>
      <p id="tValue">${totalCost} ${data1.symbol}</p>
    </div>
    <div id="detailsTotal" class="details">
      <div id="details">
        <p id="detailsText">Base Fare:</p>
        <p id="detailsValue">${data1.total_base} ${data1.symbol}</p>
      </div>
      <div id="details">
        <p id="detailsText">Baggage Fees</p>
        <p id="detailsValue">${data1.baggage_fee} ${data1.symbol}</p>
      </div>
      <div id="details">
        <p id="detailsText">Seat Selection Fee</p>
        <p id="detailsValue">${data1.seat_selection_fee} ${data1.symbol}</p>
      </div>
    </div>
    <div class="tPrice">
      <p id="taxesFeesText">Taxes and Fees</p>
      <p id="taxesFeesValue">${taxCost} ${data1.symbol}</p>
    </div>
    <div id="detailsTaxesFees" class="details">
      <div id="details">
        <p id="detailsText">Airport Tax</p>
        <p id="detailsValue">${data1.airport_tax} ${data1.symbol}</p>
      </div>
      <div id="details">
        <p id="detailsText">Security Fee</p>
        <p id="detailsValue">${data1.security_fee} ${data1.symbol}</p>
      </div>
      <div id="details">
        <p id="detailsText">ASAP Fee</p>
        <p id="detailsValue">${data1.agency_fee} ${data1.symbol}</p>
      </div>
      <div id="details">
        <p id="detailsText">Other Fees</p>
        <p id="detailsValue">${data1.other_fees} ${data1.symbol}</p>
      </div>
    </div>
    <hr id="pricingLine" />
    <div class="grand">
      <p id="grandText">Grand Total</p>
      <p id="grandValue">${grandCost} ${data1.symbol}</p>
    </div>
  </div>
    
    <div class="form-container">
      <form>
        <label>
          <input type="checkbox" id="termsCheckbox"> I agree to terms and conditions. <span id="link">Click here</span> to read the Terms & Conditions
        </label>
  
        <button id="confirmButton" onclick="confirmBooking()" class="inactive">Continue to payment</button>
      </form>
    </div>
  `;

// Append the dynamically created div to the body of the document
document.body.appendChild(dynamicDiv);
function confirmBooking() {
  alert("Booking confirmed!");
  // Add your booking confirmation logic here
}

document
  .getElementById("termsCheckbox")
  .addEventListener("change", function () {
    var confirmButton = document.getElementById("confirmButton");

    if (this.checked) {
      confirmButton.classList.remove("inactive");
      confirmButton.classList.add("active");
    } else {
      confirmButton.classList.remove("active");
      confirmButton.classList.add("inactive");
    }
  });
// Helper function to get the day name
function getDayName(dayIndex) {
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  return days[dayIndex];
}

// Helper function to get the month name
function getMonthName(monthIndex) {
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  return months[monthIndex];
}

// =========================================================================(Time Formatter)======================================

function extractTime(dateTimeString) {
  if (!dateTimeString) {
    return "Invalid date-time";
  }

  const timeOnly = dateTimeString.substring(11, 16);
  return timeOnly;
}

// Example usage:
const dateTimeString = "2024-01-31T18:15:00";
const time = extractTime(dateTimeString);
console.log(time); // Output: "18:15"

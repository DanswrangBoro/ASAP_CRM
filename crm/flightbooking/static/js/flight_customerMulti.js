let currentTraveler = 0;
let maxTravelers = 0;
console.log(flightOfferMulti);
const flightOffer = flightOfferMulti.flightOffer;
// console.log(flightsData.bookingRequirements);
// const airlines = JSON.parse(localStorage.getItem("airline"));
// console.log("hello", airlines);
let seatData = [];
const checkedBagsBySegment =
  flightOffer[0].travelerPricings[0].fareDetailsBySegment.reduce(
    (acc, segment) => {
      acc[
        segment.segmentId
      ] = `${segment.includedCheckedBags.weight}${segment.includedCheckedBags.weightUnit}`;
      return acc;
    },
    {}
  );

console.log(checkedBagsBySegment);

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
}

const numberTraveler = document.getElementById("noTravelers");
numberTraveler.innerHTML = ` ${flightOffer[0].travelerPricings.length}`;
function generateForm() {
  if (currentTraveler === 0) {
    maxTravelers = flightOffer[0].travelerPricings.length;
    if (maxTravelers <= 0) {
      alert("Please enter a valid number of travelers.");
      return;
    }
  }
  if (currentTraveler < maxTravelers) {
    currentTraveler++;

    const formContainer = document.getElementById("bookingForm");

    const travelerForm = document.createElement("div");
    travelerForm.className = "traveler-form";

    travelerForm.innerHTML = `
            <p id="noT">${capitalizeFirstLetter(flightOffer[0].travelerPricings[currentTraveler - 1].travelerType)}
            <span id="tType">${currentTraveler}</span></p>
            <label for="name${currentTraveler}">Name:</label>
            <input type="text" id="name${currentTraveler}" placeholder="Enter name">
            
            <label id="ldob" for="dob${currentTraveler}">Date of Birth (mm-dd-yyyy):</label>
            <input type="text" class="form-control" data-date-end-date="0d"  id="dob${currentTraveler}" pattern="(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])-[0-9]{4}" placeholder="mm-dd-yyyy">
            
            <label id="lsex" for="gender${currentTraveler}">Sex:</label>
            <select id="gender${currentTraveler}">
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
            </select>
        `;
    // if ("travelerRequirements" in flightsData.bookingRequirements) {
    //   travelerForm.innerHTML += `
    //   <label for="passport${currentTraveler}">Passport No:</label>
    //   <input type="text" id="passport${currentTraveler}" name="passport">
      
    //   <label for="nationality${currentTraveler}">Nationality:</label>
    //   <select name="nationality" id="nationality${currentTraveler}">
    //   <option value="AF">Afghanistan</option>
    //   <option value="AX">Åland Islands</option>
    //   <option value="AL">Albania</option>
    //   <option value="DZ">Algeria</option>
    //   <option value="AS">American Samoa</option>
    //   <option value="AD">Andorra</option>
    //   <option value="AO">Angola</option>
    //   <option value="AI">Anguilla</option>
    //   <option value="AQ">Antarctica</option>
    //   <option value="AG">Antigua and Barbuda</option>
    //   <option value="AR">Argentina</option>
    //   <option value="AM">Armenia</option>
    //   <option value="AW">Aruba</option>
    //   <option value="AU">Australia</option>
    //   <option value="AT">Austria</option>
    //   <option value="AZ">Azerbaijan</option>
    //   <option value="BS">Bahamas</option>
    //   <option value="BH">Bahrain</option>
    //   <option value="BD">Bangladesh</option>
    //   <option value="BB">Barbados</option>
    //   <option value="BY">Belarus</option>
    //   <option value="BE">Belgium</option>
    //   <option value="BZ">Belize</option>
    //   <option value="BJ">Benin</option>
    //   <option value="BM">Bermuda</option>
    //   <option value="BT">Bhutan</option>
    //   <option value="BO">Bolivia, Plurinational State of</option>
    //   <option value="BQ">Bonaire, Sint Eustatius and Saba</option>
    //   <option value="BA">Bosnia and Herzegovina</option>
    //   <option value="BW">Botswana</option>
    //   <option value="BV">Bouvet Island</option>
    //   <option value="BR">Brazil</option>
    //   <option value="IO">British Indian Ocean Territory</option>
    //   <option value="BN">Brunei Darussalam</option>
    //   <option value="BG">Bulgaria</option>
    //   <option value="BF">Burkina Faso</option>
    //   <option value="BI">Burundi</option>
    //   <option value="KH">Cambodia</option>
    //   <option value="CM">Cameroon</option>
    //   <option value="CA">Canada</option>
    //   <option value="CV">Cape Verde</option>
    //   <option value="KY">Cayman Islands</option>
    //   <option value="CF">Central African Republic</option>
    //   <option value="TD">Chad</option>
    //   <option value="CL">Chile</option>
    //   <option value="CN">China</option>
    //   <option value="CX">Christmas Island</option>
    //   <option value="CC">Cocos (Keeling) Islands</option>
    //   <option value="CO">Colombia</option>
    //   <option value="KM">Comoros</option>
    //   <option value="CG">Congo</option>
    //   <option value="CD">Congo, the Democratic Republic of the</option>
    //   <option value="CK">Cook Islands</option>
    //   <option value="CR">Costa Rica</option>
    //   <option value="CI">Côte d'Ivoire</option>
    //   <option value="HR">Croatia</option>
    //   <option value="CU">Cuba</option>
    //   <option value="CW">Curaçao</option>
    //   <option value="CY">Cyprus</option>
    //   <option value="CZ">Czech Republic</option>
    //   <option value="DK">Denmark</option>
    //   <option value="DJ">Djibouti</option>
    //   <option value="DM">Dominica</option>
    //   <option value="DO">Dominican Republic</option>
    //   <option value="EC">Ecuador</option>
    //   <option value="EG">Egypt</option>
    //   <option value="SV">El Salvador</option>
    //   <option value="GQ">Equatorial Guinea</option>
    //   <option value="ER">Eritrea</option>
    //   <option value="EE">Estonia</option>
    //   <option value="ET">Ethiopia</option>
    //   <option value="FK">Falkland Islands (Malvinas)</option>
    //   <option value="FO">Faroe Islands</option>
    //   <option value="FJ">Fiji</option>
    //   <option value="FI">Finland</option>
    //   <option value="FR">France</option>
    //   <option value="GF">French Guiana</option>
    //   <option value="PF">French Polynesia</option>
    //   <option value="TF">French Southern Territories</option>
    //   <option value="GA">Gabon</option>
    //   <option value="GM">Gambia</option>
    //   <option value="GE">Georgia</option>
    //   <option value="DE">Germany</option>
    //   <option value="GH">Ghana</option>
    //   <option value="GI">Gibraltar</option>
    //   <option value="GR">Greece</option>
    //   <option value="GL">Greenland</option>
    //   <option value="GD">Grenada</option>
    //   <option value="GP">Guadeloupe</option>
    //   <option value="GU">Guam</option>
    //   <option value="GT">Guatemala</option>
    //   <option value="GG">Guernsey</option>
    //   <option value="GN">Guinea</option>
    //   <option value="GW">Guinea-Bissau</option>
    //   <option value="GY">Guyana</option>
    //   <option value="HT">Haiti</option>
    //   <option value="HM">Heard Island and McDonald Islands</option>
    //   <option value="VA">Holy See (Vatican City State)</option>
    //   <option value="HN">Honduras</option>
    //   <option value="HK">Hong Kong</option>
    //   <option value="HU">Hungary</option>
    //   <option value="IS">Iceland</option>
    //   <option value="IN">India</option>
    //   <option value="ID">Indonesia</option>
    //   <option value="IR">Iran, Islamic Republic of</option>
    //   <option value="IQ">Iraq</option>
    //   <option value="IE">Ireland</option>
    //   <option value="IM">Isle of Man</option>
    //   <option value="IL">Israel</option>
    //   <option value="IT">Italy</option>
    //   <option value="JM">Jamaica</option>
    //   <option value="JP">Japan</option>
    //   <option value="JE">Jersey</option>
    //   <option value="JO">Jordan</option>
    //   <option value="KZ">Kazakhstan</option>
    //   <option value="KE">Kenya</option>
    //   <option value="KI">Kiribati</option>
    //   <option value="KP">Korea, Democratic People's Republic of</option>
    //   <option value="KR">Korea, Republic of</option>
    //   <option value="KW">Kuwait</option>
    //   <option value="KG">Kyrgyzstan</option>
    //   <option value="LA">Lao People's Democratic Republic</option>
    //   <option value="LV">Latvia</option>
    //   <option value="LB">Lebanon</option>
    //   <option value="LS">Lesotho</option>
    //   <option value="LR">Liberia</option>
    //   <option value="LY">Libya</option>
    //   <option value="LI">Liechtenstein</option>
    //   <option value="LT">Lithuania</option>
    //   <option value="LU">Luxembourg</option>
    //   <option value="MO">Macao</option>
    //   <option value="MK">Macedonia, The Former Yugoslav Republic of</option>
    //   <option value="MG">Madagascar</option>
    //   <option value="MW">Malawi</option>
    //   <option value="MY">Malaysia</option>
    //   <option value="MV">Maldives</option>
    //   <option value="ML">Mali</option>
    //   <option value="MT">Malta</option>
    //   <option value="MH">Marshall Islands</option>
    //   <option value="MQ">Martinique</option>
    //   <option value="MR">Mauritania</option>
    //   <option value="MU">Mauritius</option>
    //   <option value="YT">Mayotte</option>
    //   <option value="MX">Mexico</option>
    //   <option value="FM">Micronesia, Federated States of</option>
    //   <option value="MD">Moldova, Republic of</option>
    //   <option value="MC">Monaco</option>
    //   <option value="MN">Mongolia</option>
    //   <option value="ME">Montenegro</option>
    //   <option value="MS">Montserrat</option>
    //   <option value="MA">Morocco</option>
    //   <option value="MZ">Mozambique</option>
    //   <option value="MM">Myanmar</option>
    //   <option value="NA">Namibia</option>
    //   <option value="NR">Nauru</option>
    //   <option value="NP">Nepal</option>
    //   <option value="NL">Netherlands</option>
    //   <option value="NC">New Caledonia</option>
    //   <option value="NZ">New Zealand</option>
    //   <option value="NI">Nicaragua</option>
    //   <option value="NE">Niger</option>
    //   <option value="NG">Nigeria</option>
    //   <option value="NU">Niue</option>
    //   <option value="NF">Norfolk Island</option>
    //   <option value="MP">Northern Mariana Islands</option>
    //   <option value="NO">Norway</option>
    //   <option value="OM">Oman</option>
    //   <option value="PK">Pakistan</option>
    //   <option value="PW">Palau</option>
    //   <option value="PS">Palestinian Territory, Occupied</option>
    //   <option value="PA">Panama</option>
    //   <option value="PG">Papua New Guinea</option>
    //   <option value="PY">Paraguay</option>
    //   <option value="PE">Peru</option>
    //   <option value="PH">Philippines</option>
    //   <option value="PN">Pitcairn</option>
    //   <option value="PL">Poland</option>
    //   <option value="PT">Portugal</option>
    //   <option value="PR">Puerto Rico</option>
    //   <option value="QA">Qatar</option>
    //   <option value="RE">Réunion</option>
    //   <option value="RO">Romania</option>
    //   <option value="RU">Russian Federation</option>
    //   <option value="RW">Rwanda</option>
    //   <option value="BL">Saint Barthélemy</option>
    //   <option value="SH">Saint Helena, Ascension and Tristan da Cunha</option>
    //   <option value="KN">Saint Kitts and Nevis</option>
    //   <option value="LC">Saint Lucia</option>
    //   <option value="MF">Saint Martin (French part)</option>
    //   <option value="PM">Saint Pierre and Miquelon</option>
    //   <option value="VC">Saint Vincent and the Grenadines</option>
    //   <option value="WS">Samoa</option>
    //   <option value="SM">San Marino</option>
    //   <option value="ST">Sao Tome and Principe</option>
    //   <option value="SA">Saudi Arabia</option>
    //   <option value="SN">Senegal</option>
    //   <option value="RS">Serbia</option>
    //   <option value="SC">Seychelles</option>
    //   <option value="SL">Sierra Leone</option>
    //   <option value="SG">Singapore</option>
    //   <option value="SX">Sint Maarten (Dutch part)</option>
    //   <option value="SK">Slovakia</option>
    //   <option value="SI">Slovenia</option>
    //   <option value="SB">Solomon Islands</option>
    //   <option value="SO">Somalia</option>
    //   <option value="ZA">South Africa</option>
    //   <option value="GS">South Georgia and the South Sandwich Islands</option>
    //   <option value="SS">South Sudan</option>
    //   <option value="ES">Spain</option>
    //   <option value="LK">Sri Lanka</option>
    //   <option value="SD">Sudan</option>
    //   <option value="SR">Suriname</option>
    //   <option value="SJ">Svalbard and Jan Mayen</option>
    //   <option value="SZ">Swaziland</option>
    //   <option value="SE">Sweden</option>
    //   <option value="CH">Switzerland</option>
    //   <option value="SY">Syrian Arab Republic</option>
    //   <option value="TW">Taiwan, Province of China</option>
    //   <option value="TJ">Tajikistan</option>
    //   <option value="TZ">Tanzania, United Republic of</option>
    //   <option value="TH">Thailand</option>
    //   <option value="TL">Timor-Leste</option>
    //   <option value="TG">Togo</option>
    //   <option value="TK">Tokelau</option>
    //   <option value="TO">Tonga</option>
    //   <option value="TT">Trinidad and Tobago</option>
    //   <option value="TN">Tunisia</option>
    //   <option value="TR">Turkey</option>
    //   <option value="TM">Turkmenistan</option>
    //   <option value="TC">Turks and Caicos Islands</option>
    //   <option value="TV">Tuvalu</option>
    //   <option value="UG">Uganda</option>
    //   <option value="UA">Ukraine</option>
    //   <option value="AE">United Arab Emirates</option>
    //   <option value="GB">United Kingdom</option>
    //   <option selected value="US">United States</option>
    //   <option value="UM">United States Minor Outlying Islands</option>
    //   <option value="UY">Uruguay</option>
    //   <option value="UZ">Uzbekistan</option>
    //   <option value="VU">Vanuatu</option>
    //   <option value="VE">Venezuela, Bolivarian Republic of</option>
    //   <option value="VN">Viet Nam</option>
    //   <option value="VG">Virgin Islands, British</option>
    //   <option value="VI">Virgin Islands, U.S.</option>
    //   <option value="WF">Wallis and Futuna</option>
    //   <option value="EH">Western Sahara</option>
    //   <option value="YE">Yemen</option>
    //   <option value="ZM">Zambia</option>
    //   <option value="ZW">Zimbabwe</option>
    //   </select>


    //   <label id="ldob" for="expiry${currentTraveler}">Expiry date:</label>
    //   <input type="text" class="form-control" data-date-end-date="0d"  id="expiry${currentTraveler}" pattern="(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9]|3[01])-[0-9]{4}" placeholder="mm-dd-yyyy">

    //   <label for="issuance${currentTraveler}">Issuance Country:</label>
    //     <select id="issuance${currentTraveler}">
    //       <option value="AF">Afghanistan</option>
    //       <option value="AX">Åland Islands</option>
    //       <option value="AL">Albania</option>
    //       <option value="DZ">Algeria</option>
    //       <option value="AS">American Samoa</option>
    //       <option value="AD">Andorra</option>
    //       <option value="AO">Angola</option>
    //       <option value="AI">Anguilla</option>
    //       <option value="AQ">Antarctica</option>
    //       <option value="AG">Antigua and Barbuda</option>
    //       <option value="AR">Argentina</option>
    //       <option value="AM">Armenia</option>
    //       <option value="AW">Aruba</option>
    //       <option value="AU">Australia</option>
    //       <option value="AT">Austria</option>
    //       <option value="AZ">Azerbaijan</option>
    //       <option value="BS">Bahamas</option>
    //       <option value="BH">Bahrain</option>
    //       <option value="BD">Bangladesh</option>
    //       <option value="BB">Barbados</option>
    //       <option value="BY">Belarus</option>
    //       <option value="BE">Belgium</option>
    //       <option value="BZ">Belize</option>
    //       <option value="BJ">Benin</option>
    //       <option value="BM">Bermuda</option>
    //       <option value="BT">Bhutan</option>
    //       <option value="BO">Bolivia, Plurinational State of</option>
    //       <option value="BQ">Bonaire, Sint Eustatius and Saba</option>
    //       <option value="BA">Bosnia and Herzegovina</option>
    //       <option value="BW">Botswana</option>
    //       <option value="BV">Bouvet Island</option>
    //       <option value="BR">Brazil</option>
    //       <option value="IO">British Indian Ocean Territory</option>
    //       <option value="BN">Brunei Darussalam</option>
    //       <option value="BG">Bulgaria</option>
    //       <option value="BF">Burkina Faso</option>
    //       <option value="BI">Burundi</option>
    //       <option value="KH">Cambodia</option>
    //       <option value="CM">Cameroon</option>
    //       <option value="CA">Canada</option>
    //       <option value="CV">Cape Verde</option>
    //       <option value="KY">Cayman Islands</option>
    //       <option value="CF">Central African Republic</option>
    //       <option value="TD">Chad</option>
    //       <option value="CL">Chile</option>
    //       <option value="CN">China</option>
    //       <option value="CX">Christmas Island</option>
    //       <option value="CC">Cocos (Keeling) Islands</option>
    //       <option value="CO">Colombia</option>
    //       <option value="KM">Comoros</option>
    //       <option value="CG">Congo</option>
    //       <option value="CD">Congo, the Democratic Republic of the</option>
    //       <option value="CK">Cook Islands</option>
    //       <option value="CR">Costa Rica</option>
    //       <option value="CI">Côte d'Ivoire</option>
    //       <option value="HR">Croatia</option>
    //       <option value="CU">Cuba</option>
    //       <option value="CW">Curaçao</option>
    //       <option value="CY">Cyprus</option>
    //       <option value="CZ">Czech Republic</option>
    //       <option value="DK">Denmark</option>
    //       <option value="DJ">Djibouti</option>
    //       <option value="DM">Dominica</option>
    //       <option value="DO">Dominican Republic</option>
    //       <option value="EC">Ecuador</option>
    //       <option value="EG">Egypt</option>
    //       <option value="SV">El Salvador</option>
    //       <option value="GQ">Equatorial Guinea</option>
    //       <option value="ER">Eritrea</option>
    //       <option value="EE">Estonia</option>
    //       <option value="ET">Ethiopia</option>
    //       <option value="FK">Falkland Islands (Malvinas)</option>
    //       <option value="FO">Faroe Islands</option>
    //       <option value="FJ">Fiji</option>
    //       <option value="FI">Finland</option>
    //       <option value="FR">France</option>
    //       <option value="GF">French Guiana</option>
    //       <option value="PF">French Polynesia</option>
    //       <option value="TF">French Southern Territories</option>
    //       <option value="GA">Gabon</option>
    //       <option value="GM">Gambia</option>
    //       <option value="GE">Georgia</option>
    //       <option value="DE">Germany</option>
    //       <option value="GH">Ghana</option>
    //       <option value="GI">Gibraltar</option>
    //       <option value="GR">Greece</option>
    //       <option value="GL">Greenland</option>
    //       <option value="GD">Grenada</option>
    //       <option value="GP">Guadeloupe</option>
    //       <option value="GU">Guam</option>
    //       <option value="GT">Guatemala</option>
    //       <option value="GG">Guernsey</option>
    //       <option value="GN">Guinea</option>
    //       <option value="GW">Guinea-Bissau</option>
    //       <option value="GY">Guyana</option>
    //       <option value="HT">Haiti</option>
    //       <option value="HM">Heard Island and McDonald Islands</option>
    //       <option value="VA">Holy See (Vatican City State)</option>
    //       <option value="HN">Honduras</option>
    //       <option value="HK">Hong Kong</option>
    //       <option value="HU">Hungary</option>
    //       <option value="IS">Iceland</option>
    //       <option value="IN">India</option>
    //       <option value="ID">Indonesia</option>
    //       <option value="IR">Iran, Islamic Republic of</option>
    //       <option value="IQ">Iraq</option>
    //       <option value="IE">Ireland</option>
    //       <option value="IM">Isle of Man</option>
    //       <option value="IL">Israel</option>
    //       <option value="IT">Italy</option>
    //       <option value="JM">Jamaica</option>
    //       <option value="JP">Japan</option>
    //       <option value="JE">Jersey</option>
    //       <option value="JO">Jordan</option>
    //       <option value="KZ">Kazakhstan</option>
    //       <option value="KE">Kenya</option>
    //       <option value="KI">Kiribati</option>
    //       <option value="KP">Korea, Democratic People's Republic of</option>
    //       <option value="KR">Korea, Republic of</option>
    //       <option value="KW">Kuwait</option>
    //       <option value="KG">Kyrgyzstan</option>
    //       <option value="LA">Lao People's Democratic Republic</option>
    //       <option value="LV">Latvia</option>
    //       <option value="LB">Lebanon</option>
    //       <option value="LS">Lesotho</option>
    //       <option value="LR">Liberia</option>
    //       <option value="LY">Libya</option>
    //       <option value="LI">Liechtenstein</option>
    //       <option value="LT">Lithuania</option>
    //       <option value="LU">Luxembourg</option>
    //       <option value="MO">Macao</option>
    //       <option value="MK">Macedonia, The Former Yugoslav Republic of</option>
    //       <option value="MG">Madagascar</option>
    //       <option value="MW">Malawi</option>
    //       <option value="MY">Malaysia</option>
    //       <option value="MV">Maldives</option>
    //       <option value="ML">Mali</option>
    //       <option value="MT">Malta</option>
    //       <option value="MH">Marshall Islands</option>
    //       <option value="MQ">Martinique</option>
    //       <option value="MR">Mauritania</option>
    //       <option value="MU">Mauritius</option>
    //       <option value="YT">Mayotte</option>
    //       <option value="MX">Mexico</option>
    //       <option value="FM">Micronesia, Federated States of</option>
    //       <option value="MD">Moldova, Republic of</option>
    //       <option value="MC">Monaco</option>
    //       <option value="MN">Mongolia</option>
    //       <option value="ME">Montenegro</option>
    //       <option value="MS">Montserrat</option>
    //       <option value="MA">Morocco</option>
    //       <option value="MZ">Mozambique</option>
    //       <option value="MM">Myanmar</option>
    //       <option value="NA">Namibia</option>
    //       <option value="NR">Nauru</option>
    //       <option value="NP">Nepal</option>
    //       <option value="NL">Netherlands</option>
    //       <option value="NC">New Caledonia</option>
    //       <option value="NZ">New Zealand</option>
    //       <option value="NI">Nicaragua</option>
    //       <option value="NE">Niger</option>
    //       <option value="NG">Nigeria</option>
    //       <option value="NU">Niue</option>
    //       <option value="NF">Norfolk Island</option>
    //       <option value="MP">Northern Mariana Islands</option>
    //       <option value="NO">Norway</option>
    //       <option value="OM">Oman</option>
    //       <option value="PK">Pakistan</option>
    //       <option value="PW">Palau</option>
    //       <option value="PS">Palestinian Territory, Occupied</option>
    //       <option value="PA">Panama</option>
    //       <option value="PG">Papua New Guinea</option>
    //       <option value="PY">Paraguay</option>
    //       <option value="PE">Peru</option>
    //       <option value="PH">Philippines</option>
    //       <option value="PN">Pitcairn</option>
    //       <option value="PL">Poland</option>
    //       <option value="PT">Portugal</option>
    //       <option value="PR">Puerto Rico</option>
    //       <option value="QA">Qatar</option>
    //       <option value="RE">Réunion</option>
    //       <option value="RO">Romania</option>
    //       <option value="RU">Russian Federation</option>
    //       <option value="RW">Rwanda</option>
    //       <option value="BL">Saint Barthélemy</option>
    //       <option value="SH">Saint Helena, Ascension and Tristan da Cunha</option>
    //       <option value="KN">Saint Kitts and Nevis</option>
    //       <option value="LC">Saint Lucia</option>
    //       <option value="MF">Saint Martin (French part)</option>
    //       <option value="PM">Saint Pierre and Miquelon</option>
    //       <option value="VC">Saint Vincent and the Grenadines</option>
    //       <option value="WS">Samoa</option>
    //       <option value="SM">San Marino</option>
    //       <option value="ST">Sao Tome and Principe</option>
    //       <option value="SA">Saudi Arabia</option>
    //       <option value="SN">Senegal</option>
    //       <option value="RS">Serbia</option>
    //       <option value="SC">Seychelles</option>
    //       <option value="SL">Sierra Leone</option>
    //       <option value="SG">Singapore</option>
    //       <option value="SX">Sint Maarten (Dutch part)</option>
    //       <option value="SK">Slovakia</option>
    //       <option value="SI">Slovenia</option>
    //       <option value="SB">Solomon Islands</option>
    //       <option value="SO">Somalia</option>
    //       <option value="ZA">South Africa</option>
    //       <option value="GS">South Georgia and the South Sandwich Islands</option>
    //       <option value="SS">South Sudan</option>
    //       <option value="ES">Spain</option>
    //       <option value="LK">Sri Lanka</option>
    //       <option value="SD">Sudan</option>
    //       <option value="SR">Suriname</option>
    //       <option value="SJ">Svalbard and Jan Mayen</option>
    //       <option value="SZ">Swaziland</option>
    //       <option value="SE">Sweden</option>
    //       <option value="CH">Switzerland</option>
    //       <option value="SY">Syrian Arab Republic</option>
    //       <option value="TW">Taiwan, Province of China</option>
    //       <option value="TJ">Tajikistan</option>
    //       <option value="TZ">Tanzania, United Republic of</option>
    //       <option value="TH">Thailand</option>
    //       <option value="TL">Timor-Leste</option>
    //       <option value="TG">Togo</option>
    //       <option value="TK">Tokelau</option>
    //       <option value="TO">Tonga</option>
    //       <option value="TT">Trinidad and Tobago</option>
    //       <option value="TN">Tunisia</option>
    //       <option value="TR">Turkey</option>
    //       <option value="TM">Turkmenistan</option>
    //       <option value="TC">Turks and Caicos Islands</option>
    //       <option value="TV">Tuvalu</option>
    //       <option value="UG">Uganda</option>
    //       <option value="UA">Ukraine</option>
    //       <option value="AE">United Arab Emirates</option>
    //       <option value="GB">United Kingdom</option>
    //       <option selected value="US">United States</option>
    //       <option value="UM">United States Minor Outlying Islands</option>
    //       <option value="UY">Uruguay</option>
    //       <option value="UZ">Uzbekistan</option>
    //       <option value="VU">Vanuatu</option>
    //       <option value="VE">Venezuela, Bolivarian Republic of</option>
    //       <option value="VN">Viet Nam</option>
    //       <option value="VG">Virgin Islands, British</option>
    //       <option value="VI">Virgin Islands, U.S.</option>
    //       <option value="WF">Wallis and Futuna</option>
    //       <option value="EH">Western Sahara</option>
    //       <option value="YE">Yemen</option>
    //       <option value="ZM">Zambia</option>
    //       <option value="ZW">Zimbabwe</option>
    //     </select>

    //   `;
    // }

    // const addAnotherButton = document.createElement("button");
    // addAnotherButton.type = "button";
    // addAnotherButton.innerText = "Add Another Traveler";
    // addAnotherButton.addEventListener("click", generateForm);
    // travelerForm.appendChild(addAnotherButton);

    formContainer.appendChild(travelerForm);
    // Update customer names live
    const nameInput = document.getElementById(`name${currentTraveler}`);

    if (currentTraveler == maxTravelers) {
      displayAdditionalForms();
    }
  } else {
    alert("You have reached the maximum number of travelers.");
  }
}
generateForm();

// function displayAdditionalForms() {
//   const contactForms = document.querySelectorAll(".contact-form");
//   const addressForms = document.querySelectorAll(".address-form");

//   contactForms.forEach((form) => form.classList.remove("hidden"));
//   addressForms.forEach((form) => form.classList.remove("hidden"));
// }

function findCityByZip(travelerId) {
  const zipInput = document.getElementById(`zip${travelerId}`);
  const cityInput = document.getElementById(`city${travelerId}`);

  fetch(`https://api.zippopotam.us/us/${zipInput.value}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.places && data.places.length > 0) {
        cityInput.value = data.places[0]["place name"];
      } else {
        alert("City not found for the provided ZIP code.");
      }
    })
    .catch((error) => {
      console.error("Error fetching ZIP details:", error);
      alert("Failed to fetch city details for the provided ZIP.");
    });
}
function displayAdditionalForms() {
  const contactForms = document.querySelectorAll(".contact-form");
  const addressForms = document.querySelectorAll(".address-form");

  contactForms.forEach((form) => form.classList.remove("hidden"));
  addressForms.forEach((form) => form.classList.remove("hidden"));
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

// adding the duration
function addDurations(durations) {
  // Convert each duration to minutes and sum them up
  const totalMinutes = durations.reduce((total, duration) => {
    const [hours, minutes] = duration.split("h");
    return total + parseInt(hours, 10) * 60 + parseInt(minutes, 10);
  }, 0);

  // Convert the total duration back to the 'hh hh' format
  const totalHours = Math.floor(totalMinutes / 60);
  const remainingMinutes = totalMinutes % 60;

  return `${totalHours}h ${remainingMinutes}M`;
}

//code for layover duration
function subtractDurations(durations) {
  // Convert each duration to minutes and subtract them
  const totalMinutes = durations.reduce((total, duration) => {
    const [hours, minutes] = duration.split("h");
    return total - (parseInt(hours, 10) * 60 + parseInt(minutes, 10));
  }, 0);

  // Convert the total duration back to the 'hh hh' format
  const totalHours = Math.floor(Math.abs(totalMinutes) / 60);
  const remainingMinutes = Math.abs(totalMinutes) % 60;

  return `${totalHours}h ${remainingMinutes}M`;
}

// -----------------------------------------------------------------------------------------------------------------------

// Function to disable the button
function disableActive() {
  var but = document.getElementById("continue");
  but.disabled = true;
  but.style.backgroundColor = "#B6BBC4";
}

// Function to enable the button
function enableActive() {
  var but = document.getElementById("continue");
  but.disabled = false;
}

// Add event listener to the checkbox
document
  .getElementById("termsCheckbox")
  .addEventListener("change", function () {
    var checkbox = document.getElementById("termsCheckbox");

    // Check if the checkbox is checked
    if (checkbox.checked) {
      enableActive();
    } else {
      disableActive();
    }
  });

// Initially disable the button when the page loads
disableActive();

// -----------------------------------------------------------------------------------------------------------------------
async function submitForm() {
  console.log("clicked");
  // const formData = {};

  // // Iterate over each person
  // for (
  //   let i = 1;
  //   i <= flightOffer.travelerPricings.length;
  //   i++
  // ) {
  //   const person = {
  //     name: document.getElementById(`name${i}`).value,
  //     dob: document.getElementById(`dob${i}`).value,
  //     sex: document.getElementById(`gender${i}`).value,
  //   };

  //   // Add the person object to the formData
  //   formData[`person${i}`] = person;
  // }
  // const contact = {
  //   email: document.getElementById("email").value,
  //   phone: document.getElementById("phone").value,
  // };
  // const address = {
  //   address: document.getElementById("address").value,
  //   zip: document.getElementById("zip").value,
  //   city: document.getElementById("city").value,
  // };
  // formData[`contact`] = contact;
  // formData[`address`] = address;
  const formData = {};

  // Iterate over each person
  for (let i = 1; i <= flightOffer[0].travelerPricings.length; i++) {
    const fullName = document.getElementById(`name${i}`).value;

    // Split the full name into firstName and lastName
    const [firstName, lastName] = fullName.split(" ");
    let person = {};

    // if ("travelerRequirements" in flightsData.bookingRequirements) {
    //   person = {
    //     firstName: firstName || "", // Use an empty string if firstName is undefined
    //     lastName: lastName || "", // Use an empty string if lastName is undefined
    //     dob: document.getElementById(`dob${i}`).value,
    //     sex: document.getElementById(`gender${i}`).value,
    //     passportNo: document.getElementById(`passport${i}`).value,
    //     nationality: document.getElementById(`nationality${i}`).value,
    //     expiry: document.getElementById(`expiry${i}`).value,
    //     issuance: document.getElementById(`issuance${i}`).value,
    //   };
    // } else {
      person = {
        firstName: firstName || "", // Use an empty string if firstName is undefined
        lastName: lastName || "", // Use an empty string if lastName is undefined
        dob: document.getElementById(`dob${i}`).value,
        sex: document.getElementById(`gender${i}`).value,
      };
    // }
    // Add the person object to the formData array
    formData[`person${i}`] = person;
    console.log("this is persons ", formData)
  }

  // Convert the person objects to an array
  const personsArray = Object.values(formData).filter((item) => item.firstName);

  // Add the array of persons to the formData
  formData.persons = personsArray;

  const contact = {
    email: document.getElementById("email").value,
    callingCode: document.getElementById("flag").value,
    phone: document.getElementById("phone").value,
  };
  const address = {
    address: document.getElementById("address").value,
    zip: document.getElementById("zip").value,
    city: document.getElementById("city").value,
  };
  formData.contact = contact;
  formData.address = address;

  const seatpage = document.getElementById("seatmap");
  const seatPageUrl = seatpage.getAttribute("data-base-url");
  const userResponse = window.confirm("Are you sure to continue?");

  // Check the user's response
  if (userResponse) {
    // User clicked "Continue"
    const data = await create_order(formData);
    // console.log(data);
    // if()
    localStorage.setItem("Order_data", JSON.stringify(data));
    const summaryPage = document.getElementById("summary_multi");
    const summaryUrl = summaryPage.getAttribute("data-base-url");
    localStorage.setItem("order-data", JSON.stringify(data));
    window.location.href = `${summaryUrl}`;
    // Add your logic for continuing here
  } else {
    // User clicked "Cancel" or closed the dialog
    alert("Cancelled.");
    // Add your logic for cancellation here
  }

  // Log the JSON data to the console (you can send it to the server or use it as needed)
  console.log(JSON.stringify(formData));
}

// Function to display modal
function displayModal() {
  document.getElementById("modalOverlay").style.display = "block";
  document.getElementById("blurOverlay").style.display = "block";
}

// Function to hide modal
function closeModal() {
  document.getElementById("modalOverlay").style.display = "none";
  document.getElementById("blurOverlay").style.display = "none";
}

function createFlightDetails(data) {
  const flightDetailsContainer = document.createElement("div");
  flightDetailsContainer.classList.add("flight-details");

  const logoDiv = document.createElement("div");
  logoDiv.classList.add("logo");
  const inputText = `${data.carrierCode}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
  // console.log(inputText);
  // const temp = airlines[`${data.carrierCode}`];
  const temp = "something";
  const hashedText = CryptoJS.MD5(inputText).toString();
  // logoDiv.innerHTML = `<img id='logoI' src="https://content.airhex.com/content/logos/airlines_${data.carrierCode}_2000_1000_t.png?md5apikey=${hashedText}">`;
  logoDiv.innerHTML = `<img id='logoI' src="https://thimpu.pythonanywhere.com/logo/api/airline/${temp}">`;

  const anDDiv = document.createElement("div");
  anDDiv.classList.add("anD");

  const airlineNameDiv = document.createElement("div");
  airlineNameDiv.classList.add("airline-name");
  // airlineNameDiv.textContent = `${flightsData.airlines[data.carrierCode]}`;
  airlineNameDiv.textContent = `airlinename`;

  const airlineNoDiv = document.createElement("div");
  airlineNoDiv.classList.add("airline-no");
  airlineNoDiv.textContent = `${data.number}`;

  const durationDiv = document.createElement("div");
  durationDiv.classList.add("duration");
  const duration = formatDuration(data.duration);
  durationDiv.textContent = `${duration}`;

  anDDiv.appendChild(airlineNameDiv);
  anDDiv.appendChild(airlineNoDiv);
  anDDiv.appendChild(durationDiv);

  flightDetailsContainer.appendChild(logoDiv);
  flightDetailsContainer.appendChild(anDDiv);

  return flightDetailsContainer;
}

function createFlightDetailsBaggage(data) {
  const flightDetailsContainer = document.createElement("div");
  flightDetailsContainer.classList.add("flight-details");

  const logoDiv = document.createElement("div");
  logoDiv.classList.add("logo");
  const inputText = `${data.carrierCode}_2000_1000_t_VDjfGgv8mxiTvvLLwGicD6V2eq`;
  // console.log(inputText);
  const hashedText = CryptoJS.MD5(inputText).toString();
  // const temp = airlines[`${data.carrierCode}`];
  const temp = `bags`;
  // logoDiv.innerHTML = `<img id='logoI' src="https://content.airhex.com/content/logos/airlines_${data.carrierCode}_2000_1000_t.png?md5apikey=${hashedText}">`;
  logoDiv.innerHTML = `<img id='logoI' src="https://thimpu.pythonanywhere.com/logo/api/airline/${temp}">`;

  const anDDiv = document.createElement("div");
  anDDiv.classList.add("anD");

  const airlineNameDiv = document.createElement("div");
  airlineNameDiv.classList.add("airline-name");
  // airlineNameDiv.textContent = `${flightsData.airlines[data.carrierCode]}`;
  airlineNameDiv.textContent = `carrierCode`;

  const airlineNoDiv = document.createElement("div");
  airlineNoDiv.classList.add("airline-no");
  airlineNoDiv.textContent = `${data.number}`;

  anDDiv.appendChild(airlineNameDiv);
  anDDiv.appendChild(airlineNoDiv);

  flightDetailsContainer.appendChild(logoDiv);
  flightDetailsContainer.appendChild(anDDiv);

  return flightDetailsContainer;
}

function createTimeDetails(data) {
  const timeDetailsContainer = document.createElement("div");
  timeDetailsContainer.classList.add("time-details");
  const departDateTime = formatDateTime(data.departure.at);
  const returnDateTime = formatDateTime(data.departure.at);
  const departureTimeDiv = createTimeComponent("Departure", departDateTime);
  const arrivalTimeDiv = createTimeComponent("Arrival", returnDateTime);
  const layoverTimeDiv = document.createElement("div");
  layoverTimeDiv.classList.add("layover-time");
  layoverTimeDiv.textContent = "Layover Time";

  timeDetailsContainer.appendChild(departureTimeDiv);
  timeDetailsContainer.appendChild(arrivalTimeDiv);
  timeDetailsContainer.appendChild(layoverTimeDiv);

  return timeDetailsContainer;
}

// Helper function to create time components (day, year, date)
function createTimeComponent(prefix, data) {
  const timeComponentDiv = document.createElement("div");
  timeComponentDiv.classList.add("timeAndDate");

  const dateDiv = document.createElement("div");
  dateDiv.classList.add("date");
  dateDiv.textContent = `${prefix} ${data}`;
  timeComponentDiv.appendChild(dateDiv);

  return timeComponentDiv;
}
// Function to create city details structure
function createCityDetails(data) {
  const cityDetailsContainer = document.createElement("div");
  cityDetailsContainer.classList.add("city-details");

  const departureCityDiv = createCityComponent(
    "Departure",
    data.departure.iataCode
  );
  const arrivalCityDiv = createCityComponent("Arrival", data.arrival.iataCode);

  cityDetailsContainer.appendChild(departureCityDiv);
  cityDetailsContainer.appendChild(arrivalCityDiv);

  return cityDetailsContainer;
}

// Helper function to create city components (city name, IATA code)
function createCityComponent(prefix, data) {
  const cityComponentDiv = document.createElement("div");
  cityComponentDiv.classList.add("cityDetails");

  const cityNameDiv = document.createElement("div");
  cityNameDiv.classList.add("city-name");
  cityNameDiv.textContent = `${data}`;

  const iataCodeDiv = document.createElement("div");
  iataCodeDiv.classList.add("iata-code");
  iataCodeDiv.innerHTML = `<span id="op">﹙</span>${data}<span id="op">﹚</span>`;

  cityComponentDiv.appendChild(cityNameDiv);
  cityComponentDiv.appendChild(iataCodeDiv);

  return cityComponentDiv;
}

// Function to create city details structure
function DetailsBaggage(data) {
  console.log(data.id);
  const weightcontainer = document.createElement("div");
  weightcontainer.classList.add("weight");
  weightcontainer.textContent = checkedBagsBySegment[`${data.id}`] + "/person";

  return weightcontainer;
}

// Helper function to create city components (city name, IATA code)
function createCityComponentBaggage(prefix, data) {
  const cityComponentDiv = document.createElement("div");
  cityComponentDiv.classList.add("cityDetails");

  const cityNameDiv = document.createElement("div");
  cityNameDiv.classList.add("city-name");
  cityNameDiv.textContent = `${data}`;

  const iataCodeDiv = document.createElement("div");
  iataCodeDiv.classList.add("iata-code");
  iataCodeDiv.innerHTML = `<span id="op">﹙</span>${data}<span id="op">﹚</span>`;

  cityComponentDiv.appendChild(cityNameDiv);
  cityComponentDiv.appendChild(iataCodeDiv);

  return cityComponentDiv;
}

function showBag() {
  var bag = document.getElementById("bag");
  var blurOverlay = document.getElementById("blur");

  bag.style.display = "block";
  bag.style.justifyContent = "center";
  bag.style.alignItems = "center";

  blurOverlay.style.display = "block";
}

function hideBag() {
  var bag = document.getElementById("bag");
  bag.style.transition = "transform 0.5s ease-out, opacity 0.5s ease-out";
  bag.style.animation = "slideUpAndHide 0.5s ease-out";
  var blurOverlay = document.getElementById("blur");
  blurOverlay.style.display = "none";

  // Optional: Add an event listener to reset styles after the animation ends
  bag.addEventListener(
    "animationend",
    function () {
      bag.style.display = "none";
      bag.style.animation = "";
      bag.style.transition = "";
    },
    { once: true }
  );
}

// Add event listener to hide modal when clicking outside of it
document.addEventListener("click", function (event) {
  var bag = document.getElementById("bag");
  if (event.target !== bag && !bag.contains(event.target)) {
    hideBag();
  }
});

// Function to create cabin details structure
function createCabinDetails(data) {
  const cabinDetailsContainer = document.createElement("div");
  cabinDetailsContainer.classList.add("cabin-details");

  const cabinTypeDiv = document.createElement("div");
  cabinTypeDiv.classList.add("cabin-type");

  const bagDetails = document.createElement("div");
  bagDetails.classList.add("bag");
  const svg = document.createElement("span");
  svg.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-suitcase2-fill" viewBox="0 0 16 16">
  <path d="M6.5 0a.5.5 0 0 0-.5.5V3H4.5A1.5 1.5 0 0 0 3 4.5v9a1.5 1.5 0 0 0 1.003 1.416A1 1 0 1 0 6 15h4a1 1 0 1 0 1.996-.084A1.5 1.5 0 0 0 13 13.5v-9A1.5 1.5 0 0 0 11.5 3H10V.5a.5.5 0 0 0-.5-.5zM9 3H7V1h2zM4 7V6h8v1z"/>
</svg>`;
  const bagButton = document.createElement("button");
  bagButton.classList.add("bagButton");
  bagButton.classList.add("Button");

  bagDetails.appendChild(svg);
  bagButton.textContent = "Baggage allowance";
  bagButton.style.backgroundColor = "transparent";
  bagButton.style.color = "blue";
  bagButton.style.padding = "0";

  // Trigger element to show the modal when button is clicked
  bagButton.addEventListener("click", function (event) {
    showBag();
    event.stopPropagation(); // Prevent the click event from reaching the document click listener immediately
  });

  bagDetails.appendChild(bagButton);

  cabinTypeDiv.textContent = `${flightOffer[0].travelerPricings[0].fareDetailsBySegment[0].cabin}`;

  cabinDetailsContainer.appendChild(cabinTypeDiv);
  cabinDetailsContainer.appendChild(bagDetails);

  return cabinDetailsContainer;
}

function appendSubcontainer(data) {
  // console.log(data);
  const subcontainer = document.createElement("div");
  subcontainer.classList.add("subcontainer");
  for (let i = 0; i < data.segments.length; i++) {
    const SubContainFlightDetails = document.createElement("div");
    SubContainFlightDetails.classList.add("SubContainFlightDetails");
    SubContainFlightDetails.appendChild(createFlightDetails(data.segments[i]));
    SubContainFlightDetails.appendChild(createTimeDetails(data.segments[i]));
    SubContainFlightDetails.appendChild(createCityDetails(data.segments[i]));
    SubContainFlightDetails.appendChild(createCabinDetails(data.segments[i]));
    subcontainer.appendChild(SubContainFlightDetails);
  }
  return subcontainer;
}
// Function to create and append structures based on the segment length
function createAndAppendStructures(data) {
  const itineraryContainer = document.querySelector(".itinerary-container");
  itineraryContainer.appendChild(appendSubcontainer(data));
}

function appendSubcontainerBaggage(data) {
  // console.log("iwedbiqwueb", data);
  const subcontainer = document.createElement("div");
  subcontainer.classList.add("subcontainer");
  // console.log("this is segment length", data.segments.length);
  for (let i = 0; i < data.segments.length; i++) {
    const SubContainFlightDetails = document.createElement("div");
    SubContainFlightDetails.classList.add("SubContainFlightDetails");
    SubContainFlightDetails.appendChild(
      createFlightDetailsBaggage(data.segments[i])
    );
    SubContainFlightDetails.appendChild(DetailsBaggage(data.segments[i]));
    subcontainer.appendChild(SubContainFlightDetails);
  }
  return subcontainer;
}

function createAndAppendStructuresBaggage(data) {
  const itineraryContainer = document.querySelector(".baggage");
  itineraryContainer.appendChild(appendSubcontainerBaggage(data));
}

// console.log(flightOffer);
const segmentLength = flightOffer.length;

function controlContainer() {
  for (let i = 0; i < segmentLength; i++) {
    createAndAppendStructures(flightOffer[i].itineraries[0]);
    createAndAppendStructuresBaggage(flightOffer[i].itineraries[0]);
  }
}
controlContainer();

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

function formatDateTime(dateTimeString) {
  const options = {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  const date = new Date(dateTimeString);
  const formattedDateTime = date.toLocaleString("en-US", options);
  return formattedDateTime;
}
let datas = [];
var selectedSeatMapIndex = 0;
const selectedSeats = [];
var create_order_details = {};
var chCode = [];
var coordinates = [];
var priceCharge = [];

// seatmap function========================================================================================================
async function fetchSeats() {
  const seatPage = document.getElementById("seatmapmulti");
  const seatPageUrl = seatPage.getAttribute("data-base-url");
  const response = await fetch(`${seatPageUrl}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(flightOffer),
  });
  console.log("this is called");
  const data = await response.json();
  console.log(data);
  if (data.seats[0].status === 400) {
    const mainContainer = document.getElementById("mainContainer");
    const errorDetails = document.createElement("p");
    errorDetails.textContent = `${data.seats[0].detail}`;
    mainContainer.appendChild(errorDetails);
    console.log(data.seats[0].detail);
  } else {
    datas = data.seats;
    console.log(data.seats);

    datas.forEach((airplane) => {
      airplane.decks.forEach((deck) => {
        deck.seats.forEach((seat, index) => {
          chCode.push(seat.characteristicsCodes);
          coordinates.push(seat.coordinates);
        });
      });
    });
    var carr = [];
    datas.forEach((index) => {
      carr.push(index.carrierCode);
    });
    console.log("Here is airline " + carr);
    //  const hasCH = chCode.some(code => code.includes('CH'));
    // chCode.forEach((index)=>{
    //   if (hasCH) {
    //     priceCharge.push(seat.travelerPricing[0].price.total);
    //   }
    // })

    //  console.log(priceCharge);
    // console.log(chCode);
    // console.log(coordinates);

    // Create a modal element
    const modal = document.createElement("div");
    modal.id = "seatModal";
    modal.classList.add("modal");
    document.body.appendChild(modal);

    const navbar = document.getElementById("navbar");
    const mainContainer = document.getElementById("mainContainer");
    // Create buttons for each departure and destination
    datas.forEach((seatmap, index) => {
      const button = document.createElement("button");
      button.textContent = `${seatmap.departure.iataCode} → ${seatmap.arrival.iataCode}`;
      button.addEventListener("click", () => {
        selectedSeatMapIndex = index;
        renderSeatMap();
        // updateRightInfo();
        // updateRightInfo();
      });
      navbar.appendChild(button);
    });
  }
}
document.addEventListener("DOMContentLoaded", function () {
  fetchSeats();
});
// Display the first seatmap by default
renderSeatMap();
// updateRightInfo();
// updateRightInfo();
function renderSeatMap() {
  const seatMainContainer = document.createElement("div");
  seatMainContainer.id = "seatContainer";
  seatMainContainer.classList.add("seatContainer");
  const seatmapContainer = document.createElement("div");
  seatmapContainer.classList.add("seatmap");
  const seatmap = datas[selectedSeatMapIndex];
  const segmentId = seatmap.segmentId;
  console.log(segmentId);

  const column = seatmap.decks[0].deckConfiguration.width;
  const row = seatmap.decks[0].deckConfiguration.length;

  seatmapContainer.style.display = "grid";
  seatmapContainer.style.gridTemplateColumns = `repeat(${column}, 1fr)`;
  seatmapContainer.style.gridTemplateRows = `repeat(${row}, 1fr)`;

  seatmap.decks.forEach((deck) => {
    var startWingRow = deck.deckConfiguration.startWingsX;
    //console.log("Start wing row is " + startWingRow);
    //console.log("Start wing row is " + startWingRow);
    var endWingRow = deck.deckConfiguration.endWingsX;
    //console.log("End wing row is " + endWingRow);
    //console.log("End wing row is " + endWingRow);

    deck.seats.forEach((seat, index) => {
      const seatElement = document.createElement("div");
      const travelerID = seat.travelerPricing[0].travelerId[0];
      var price = seat?.travelerPricing?.[0]?.price;

      if (price !== undefined) {
        // The 'price' property is available
        console.log("Price is available:", price);
      } else {
        // The 'price' property is not available
        console.log("Price is not available.");
        price = 0;
      }
      seatElement.classList.add("seat");

      // Add event listener for mouseover event
      seatElement.addEventListener("mouseover", () => {
        // Display chCode in the modal
        displayChCodeModal(chCode[index], seatElement);
      });

      // Add event listener for mouseout event
      seatElement.addEventListener("mouseout", () => {
        // Close the modal when the mouse is not over a seat
        closeChCodeModal();
      });

      if (
        seat.travelerPricing.some(
          (traveler) => traveler.seatAvailabilityStatus === "AVAILABLE"
        )
      ) {
        seatElement.classList.add("available");
      } else {
        seatElement.classList.add("blocked");
      }

      // Check if seat number is within the wing rows range
      const seatRow = seat.coordinates.x;
      if (seatRow >= startWingRow && seatRow <= endWingRow) {
        seatElement.classList.add("wing-seat");
      }

      // Set the seat position based on coordinates
      seatElement.style.gridRow = `${seat.coordinates.x * 2} / span 2`;
      seatElement.style.gridColumn = `${seat.coordinates.y * 2} / span 2`;

      // Add a div element for chCode value
      const chCodeElement = document.createElement("div");
      const chCodeValue = chCode[index]; // Get the chCode value for the current seat

      // Set the seat number and chCode as the content of the seat element
      seatElement.textContent = seat.number;

      // Check if chCode contains 'W' at the specific index
      //console.log("Checking seat", seat.number, "with chCode", chCodeValue);

      // seatElement.textContent = seat.number;
      seatElement.addEventListener("click", () => {
        if (!seatElement.classList.contains("blocked")) {
          seatElement.classList.toggle("selected");
          updateSelectedSeats(seat.number, segmentId, travelerID, price);
        }
      });

      seatmapContainer.appendChild(seatElement);
    });
  });

  // Function to display chCode in an attractive modal
  function displayChCodeModal(chCodeValue, seatElement) {
    const rect = seatElement.getBoundingClientRect();
    const windowHeight = window.innerHeight;

    // Check if there is enough space below the seat, otherwise, display above
    const displayAbove = rect.bottom + 300 > windowHeight;

    modal.innerHTML = `
  <div class="">
    <div class="modal-header">
      <h2>Seat Information</h2>
      <hr>
    </div>
    <div class="modal-body">
      <p><strong>Seat No:</strong> ${seatElement.textContent}</p>
      <p><strong>Seat Type:</strong> ${getSeatType(chCodeValue)}</p>
      <p><strong>Chargeable Amount:</strong> ${getChargeableAmount(
        chCodeValue
      )}</p>
    </div>
  </div>
`;

    modal.style.transition = "opacity 0.5s, top 0.5s, left 0.5s"; // Set transition duration
    modal.style.display = "block";

    if (displayAbove) {
      modal.style.top = `${rect.top - 352}px`; // Add some space above the seat
    } else {
      modal.style.top = `${rect.bottom + 10}px`; // Add some space below the seat
    }

    modal.style.left = `${rect.left - 150 + rect.width / 2}px`; // Adjust left position based on width
  }

  // Helper function to get seat type based on chCode
  function getSeatType(chCode) {
    // You can customize this function based on your specific seat types
    if (chCode.includes("CH") && chCode.includes("1A_AQC_PREMIUM_SEAT")) {
      return "Chargeable Seat, Premium Seat";
    } else if (chCode.includes("CH")) {
      return "Chargeable Seat";
    } else if (chCode.includes("1A_AQC_PREMIUM_SEAT")) {
      return "Premium Seat";
    } else {
      return "Regular Seat";
    }
  }

  // Helper function to get chargeable amount based on chCode
  function getChargeableAmount(chCode) {
    // You can customize this function based on your specific pricing logic
    if (chCode.includes("CH")) {
      return "Your custom chargeable amount";
    } else {
      return "N/A";
    }
  }

  // Function to close the modal
  function closeChCodeModal() {
    modal.style.display = "none";
  }

  seatMainContainer.appendChild(seatmapContainer);

  mainContainer.innerHTML = "";

  mainContainer.appendChild(seatMainContainer);

  // Log all loaded objects
  console.log("All Loaded Seatmaps:", datas);
}
// function updateSelectedSeats(seatNumber, indexNo) {
//   const selectedSeats = [];
//   const selectedSeatMap = seatData[selectedSeatMapIndex];
//   selectedSeatMap.decks.forEach((deck) => {
//     deck.seats.forEach((seat, index) => {
//       if (
//         seat.travelerPricing.some(
//           (traveler) => traveler.seatAvailabilityStatus === "AVAILABLE"
//         )
//       ) {
//         if (index === indexNo) {
//           selectedSeats.push(seat.number);
//         }
//       }
//     });
//   });
//   if (selectedSeats.length >= 9) {
//     alert("Max seats reached");
//   }
//   console.log("Selected Seats:", selectedSeats);
// }
// Function to update right-info div content with selected seats and other details

// Function to update right-info div content with selected seats and other details
// function updateRightInfo() {
//   const rightInfoDiv = document.querySelector(".rInfo");

//   // Get the selected seatmap
//   const selectedSeatMap = seatData[selectedSeatMapIndex];

//   // Get information for the selected flight
//   const airlineName = carr[0]; // Replace with actual data
//   // const passengerNames = `${customer.personalInformation.firstName} ${customer.personalInformation.lastName}`;
//   let checkedBags;
//   const includedCheckedBagsOnly =
//     flightData.pricingOptions.includedCheckedBagsOnly;
//   // console.log(includedCheckedBagsOnly);
//   if (includedCheckedBagsOnly) {
//     checkedBags = `${flightData.travelerPricings[0].fareDetailsBySegment[0].includedCheckedBags.weight} ${flightData.travelerPricings[0].fareDetailsBySegment[0].includedCheckedBags.weightUnit}/adult`;
//   } else {
//     checkedBags = "Not Available";
//   }
//   const selectedSeatNumbers = selectedSeats
//     .flatMap((entry) =>
//       entry.fareDetailsBySegment
//         .filter((segment) => segment.segmentId === selectedSeatMap.segmentId)
//         .flatMap((segment) => segment.additionalServices.chargeableSeatNumber)
//     )
//     .join(", ");
//   const luggageInfo = "Luggage Info"; // Replace with actual data

//   // Update the right-info div content
//   rightInfoDiv.innerHTML = `
//   <h2>${airlineName}</h2>
//   <hr>
//   <p>Passengers: ${passengerNames}</p>
//   <p>Selected Seats: ${selectedSeatNumbers}</p>
//   <p>Included Checked Bags: ${checkedBags}</p>

// `;
// }
function updateSelectedSeats(seatNumber, segmentId, travelerId, price) {
  // if (!selectedSeats[segmentId]) {
  //   selectedSeats[segmentId] = []; // Initialize the array for the deckIndex if not exists
  // }
  // const index = selectedSeats[segmentId].indexOf(seatNumber);
  // console.log(segmentId);
  // if (index !== -1) {
  //   selectedSeats[segmentId].splice(index, 1); // Deselect the seat if already selected
  // } else {
  //   selectedSeats[segmentId].push(seatNumber); // Select the seat
  // }
  // if (selectedSeats.length >= 9) {
  //   alert("maxed reasched");
  //   console.log("max reached");
  // }

  // // console.log("Selected Seats:", selectedSeats);

  // Find the traveler entry in selectedSeats array
  // Find the traveler entry in selectedSeats array
  console.log(price);
  let travelerEntry = selectedSeats.find(
    (entry) => entry.travelerId === travelerId
  );

  // If traveler entry doesn't exist, create a new one
  if (!travelerEntry) {
    travelerEntry = {
      travelerId: travelerId,
      fareDetailsBySegment: [],
    };
    selectedSeats.push(travelerEntry);
  }

  // Find the segment entry in the traveler's fareDetailsBySegment array
  let segmentEntry = travelerEntry.fareDetailsBySegment.find(
    (entry) => entry.segmentId === segmentId
  );

  // If segment entry doesn't exist, create a new one
  if (!segmentEntry) {
    segmentEntry = {
      segmentId: segmentId,
      additionalServices: {
        chargeableSeatNumber: [],
      },
    };
    travelerEntry.fareDetailsBySegment.push(segmentEntry);
  }

  // Toggle the selected seat
  const seatIndex =
    segmentEntry.additionalServices.chargeableSeatNumber.indexOf(seatNumber);
  if (seatIndex !== -1) {
    segmentEntry.additionalServices.chargeableSeatNumber.splice(seatIndex, 1);
  } else {
    segmentEntry.additionalServices.chargeableSeatNumber.push(seatNumber);
  }

  // Log the selectedSeats array
  console.log("Selected Seats:", selectedSeats);
  // Update the right-info div content
  // updateRightInfo();
}

// document
//   .getElementById("Payment-continue")
//   .addEventListener("click", async function () {
//     const urlElement = document.getElementById("create-order-url");
//     const createOrderEndPoint = urlElement.getAttribute("data-base-url");
//     // console.log("This is clicked");
//     // for (const segmentId in selectedSeats) {
//     //   if (selectedSeats.hasOwnProperty(segmentId)) {
//     //     const seatNumber = selectedSeats[segmentId];
//     //     addAdditionalServices(segmentId, seatNumber);
//     //   }
//     // }
//     // console.log(flightData);
//     const selectedSeatsOutput = Object.entries(selectedSeats).map(
//       ([segmentId, seatNumbers]) => ({
//         segmentId,
//         seatNumber: seatNumbers,
//       })
//     );
//     console.log(selectedSeatsOutput);
//     const requestData = {
//       flightData,
//       selectedSeatsOutput,
//     };
//     const response = await fetch(`${createOrderEndPoint}`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//         "X-CSRFToken": getCookie("csrftoken"),
//       },
//       body: JSON.stringify(requestData),
//     });
//     const data = await response.json();

//     console.log(data);
//   });

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

async function create_order(traveler) {
  const urlElement = document.getElementById("create-order-url-multi");
  const createOrderEndPoint = urlElement.getAttribute("data-base-url");
  const selectedSeatsOutput = Object.entries(selectedSeats).map(
    ([segmentId, seatNumbers]) => ({
      segmentId,
      seatNumber: seatNumbers,
    })
  );
  console.log(selectedSeatsOutput);
  var requestBody = {
    flightOffer: flightOffer,
    traveler: traveler,
    selectedSeats: selectedSeatsOutput,
  };
  const response = await fetch(`${createOrderEndPoint}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify(requestBody),
  });
  const data = await response.json();

  console.log(traveler);
  console.log(data);
  return data;
}

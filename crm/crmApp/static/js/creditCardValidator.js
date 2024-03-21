var $cc = {}
$cc.validate = function (e) {

  //if the input is empty reset the indicators to their default classes
  if (e.target.value == '') {
    e.target.previousElementSibling.className = 'card-type';
    e.target.nextElementSibling.className = 'card-valid';
    return
  }

  //Retrieve the value of the input and remove all non-number characters
  var number = String(e.target.value);
  var cleanNumber = '';
  for (var i = 0; i < number.length; i++) {
    if (/^[0-9]+$/.test(number.charAt(i))) {
      cleanNumber += number.charAt(i);
    }
  }

  //Only parse and correct the input value if the key pressed isn't backspace.
  if (e.key != 'Backspace') {
    //Format the value to include spaces in the correct locations
    var formatNumber = '';
    for (var i = 0; i < cleanNumber.length; i++) {
      if (i == 3 || i == 7 || i == 11) {
        formatNumber = formatNumber + cleanNumber.charAt(i) + ' '
      } else {
        formatNumber += cleanNumber.charAt(i)
      }
    }
    e.target.value = formatNumber;
  }

  //run the Luhn algorithm on the number if it is at least equal to the shortest card length
  if (cleanNumber.length >= 12) {
    var isLuhn = luhn(cleanNumber);
  }

  function luhn(number) {
    var numberArray = number.split('').reverse();
    for (var i = 0; i < numberArray.length; i++) {
      if (i % 2 != 0) {
        numberArray[i] = numberArray[i] * 2;
        if (numberArray[i] > 9) {
          numberArray[i] = parseInt(String(numberArray[i]).charAt(0)) + parseInt(String(numberArray[i]).charAt(1))
        }
      }
    }
    var sum = 0;
    for (var i = 1; i < numberArray.length; i++) {
      sum += parseInt(numberArray[i]);
    }
    sum = sum * 9 % 10;
    if (numberArray[0] == sum) {
      return true
    } else {
      return false
    }
  }

  //if the number passes the Luhn algorithm add the class 'active'
  if (isLuhn == true) {
    e.target.nextElementSibling.className = 'card-valid active'
  } else {
    e.target.nextElementSibling.className = 'card-valid'
  }

  var card_types = [
    {
      name: 'amex',
      pattern: /^3[47]/,
      valid_length: [15]
    }, {
      name: 'diners_club_carte_blanche',
      pattern: /^30[0-5]/,
      valid_length: [14]
    }, {
      name: 'diners_club_international',
      pattern: /^36/,
      valid_length: [14]
    }, {
      name: 'jcb',
      pattern: /^35(2[89]|[3-8][0-9])/,
      valid_length: [16]
    }, {
      name: 'laser',
      pattern: /^(6304|670[69]|6771)/,
      valid_length: [16, 17, 18, 19]
    }, {
      name: 'visa_electron',
      pattern: /^(4026|417500|4508|4844|491(3|7))/,
      valid_length: [16]
    }, {
      name: 'visa',
      pattern: /^4/,
      valid_length: [16]
    }, {
      name: 'mastercard',
      pattern: /^5[1-5]/,
      valid_length: [16]
    }, {
      name: 'maestro',
      pattern: /^(5018|5020|5038|6304|6759|676[1-3])/,
      valid_length: [12, 13, 14, 15, 16, 17, 18, 19]
    }, {
      name: 'discover',
      pattern: /^(6011|622(12[6-9]|1[3-9][0-9]|[2-8][0-9]{2}|9[0-1][0-9]|92[0-5]|64[4-9])|65)/,
      valid_length: [16]
    },
    // Additional card types
    {
      name: 'unionpay',
      pattern: /^(62|88)/,
      valid_length: [16, 17, 18, 19]
    },
    {
      name: 'mir',
      pattern: /^(2200|2204)/,
      valid_length: [16, 17, 18, 19]
    },
    {
      name: 'instapayment',
      pattern: /^63/,
      valid_length: [16]
    },
    {
      name: 'hipercard',
      pattern: /^(3841|60)/,
      valid_length: [16]
    },
    {
      name: 'elo',
      pattern: /^((50670[7-8])|(5090[1-9])|(63636[0-9])|(636368)|(6504)|(6504)|(6504)|(6505)|(6505)|(6505)|(6509)|(6509)|(6509)|(6516)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550)|(6550))/,
      valid_length: [16]
    },
    {
      name: 'rupay',
      pattern: /^(60|6521)/,
      valid_length: [16]
    },
    {
      name: 'bcglobal',
      pattern: /^7(2(0[8-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-8]))/,
      valid_length: [16]
    },
    {
      name: 'carnet',
      pattern: /^6(00[1-5]|5(0(0[0-9]|1[0-8])|1(5(0[0-9]|1[0-8])|6(0[0-9]|1[0-8]))))/,
      valid_length: [16]
    }
    // Add more card types as needed
  ];

  //test the number against each of the above card types and regular expressions
  for (var i = 0; i < card_types.length; i++) {
    if (number.match(card_types[i].pattern)) {
      //if a match is found add the card type as a class
      e.target.previousElementSibling.className = 'card-type ' + card_types[i].name;
    }
  }
}

$cc.expiry = function (e) {
  if (e.key != 'Backspace') {
    var number = String(this.value);

    //remove all non-number character from the value
    var cleanNumber = '';
    for (var i = 0; i < number.length; i++) {
      if (i == 1 && number.charAt(i) == '/') {
        cleanNumber = 0 + number.charAt(0);
      }
      if (/^[0-9]+$/.test(number.charAt(i))) {
        cleanNumber += number.charAt(i);
      }
    }

    var formattedMonth = ''
    for (var i = 0; i < cleanNumber.length; i++) {
      if (/^[0-9]+$/.test(cleanNumber.charAt(i))) {
        //if the number is greater than 1 append a zero to force a 2 digit month
        if (i == 0 && cleanNumber.charAt(i) > 1) {
          formattedMonth += 0;
          formattedMonth += cleanNumber.charAt(i);
          formattedMonth += '/';
        }
        //add a '/' after the second number
        else if (i == 1) {
          formattedMonth += cleanNumber.charAt(i);
          formattedMonth += '/';
        }
        //force a 4 digit year
        else if (i == 2 && cleanNumber.charAt(i) < 2) {
          formattedMonth += '20' + cleanNumber.charAt(i);
        } else {
          formattedMonth += cleanNumber.charAt(i);
        }

      }
    }
    this.value = formattedMonth;
  }
}
//////////////card type suggestions//////////////
function suggestCreditCardType(inputValue, event) {
  // Ignore Backspace key and empty input
  if (inputValue === "" || event.key === "Backspace") {
    document.getElementById("creditCardTypeSuggestions").innerHTML = "";
    return;
  }

  var creditCardTypes = [
    "American Express (AMEX)",
    "Diners Club - Carte Blanche",
    "Diners Club - International",
    "JCB",
    "Laser",
    "Visa Electron",
    "Visa",
    "Mastercard",
    "Maestro",
    "Discover",
    "UnionPay",
    "Mir",
    "Instapayment",
    "Hipercard",
    "Elo",
    "BCGlobal",
    "Carnet",
    "Dankort",
    "Carte Bancaire (CB)",
    "InterPayment",
    "Bancontact",
    "Switch",
    "Solo",
    "Carte Bleue",
    "China UnionPay",
    "RuPay",
    "Troy",
    "Cabal",
    "UATP (Universal Air Travel Plan)",
    "Discover Diners Club"
    // Add more credit card types as needed

  ];

  var suggestions = [];

  // Filter credit card types based on input value
  creditCardTypes.forEach(function (type) {
    if (type.toLowerCase().startsWith(inputValue.toLowerCase())) {
      suggestions.push(type);
    }
  });

  // Display suggestions
  var suggestionContainer = document.getElementById("creditCardTypeSuggestions");
  suggestionContainer.innerHTML = "";

  suggestions.forEach(function (type) {
    var suggestion = document.createElement("div");
    suggestion.textContent = type;
    suggestion.style.cursor = "pointer";
    suggestion.addEventListener("click", function () {
      // Set selected credit card type to input field value
      document.querySelector(".ctype input").value = type;
      // Clear suggestions
      suggestionContainer.innerHTML = "";
    });
    suggestionContainer.appendChild(suggestion);
  });
}
//suggestions
// function showSuggestions() {
//   var suggestionDiv = document.getElementById('creditCardTypeSuggestions');
//   suggestionDiv.classList.add('visible');
// }

// function hideSuggestions() {
//   var suggestionDiv = document.getElementById('creditCardTypeSuggestions');
//   suggestionDiv.classList.remove('visible');
// }
//
function handleInput(value) {
  var suggestionDiv = document.getElementById('creditCardTypeSuggestions');
  if (value.trim() !== '') {
    suggestionDiv.classList.add('visible');
    suggestCreditCardType(value, { key: '' }); // Call suggestCreditCardType with input value
  } else {
    suggestionDiv.classList.remove('visible');
  }
}
//cvv
function handleCVVInput(value) {
  var cvvInput = document.getElementById('cvvInput');
  var cleanValue = value.replace(/\D/g, ''); // Remove non-numeric characters

  if (cleanValue.length > 3) {
    cleanValue = cleanValue.slice(0, 3); // Limit to 3 digits
  }

  cvvInput.value = cleanValue; // Update the input field value

  if (cleanValue.length === 3) {
    // Automatically switch focus to the next input field
    var nextInput = cvvInput.nextElementSibling;
    if (nextInput) {
      nextInput.focus();
    }
  }
}



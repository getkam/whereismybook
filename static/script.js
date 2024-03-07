function validatePassword(){
  let pass = document.getElementById("password").value

  if (pass.length < 5 || !/[a-z]/.test(pass) || !/\d/.test(pass))
  {
      alert('Password must have at least 5 characters including letter and  digit');
      document.getElementById("password").value = "";
  }
}

function checkIfPasswordsAreMatching(){

  let password = document.getElementById("password").value;
  let confirmation = document.getElementById("confirmation").value;

  if (password != confirmation){
      alert('Passwords are not matching');
  }
}

function validateAmountOfShares(){
  let amount = parseInt(document.getELementById("amount").value)

  if (amount==NaN){
      alert("Amount must be a number")
  }
  else if ( amount < 0 ){
      alert("Amount must be greater than 0")
  }
  document.getELementById("amount").innerText ==""
}

$(document).ready(function() {
  $('.js-example-basic-multiple').select2({
      placeholder: "Select tags",
      allowClear: true
  });
});

document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('select-all').addEventListener('change', function (event) {
      var checked = event.target.checked;
      document.querySelectorAll('.book-checkbox').forEach(function (checkbox) {
          checkbox.checked = checked;
      });
  });
});
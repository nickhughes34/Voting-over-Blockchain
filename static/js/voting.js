var form = document.getElementById("form");

function validation(){
  var person = document.getElementById("party");

  if (person.value == "null" || person.value === ""){
    alert("Vote for a Candidate!");
  } else {
    //alert("Voted " + person.value);
    form.submit();
  }

}

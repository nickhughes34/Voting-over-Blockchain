var app = angular.module('VotinglPage', []);
var previous = -1;

app.controller("MainController", function($scope){
  $scope.picks = [
    {FName: "John", LName: "Doe", Age: "45", Party: "NDP", Img: "images/logo.png"},
    {FName: "Jane", LName: "Doe", Age: "55", Party: "Liberal", Img: "images/logo.png"},
    {FName: "John", LName: "Smith", Age: "65", Party: "Conservative", Img: "images/logo.png"}
];

  $scope.Vote =  function(index, $event) {
      //console.log(index, $event["currentTarget"]);
      //console.log(index);
      document.getElementById("firstName").value = $scope.picks[index]["FName"];
      document.getElementById("lastName").value = $scope.picks[index]["LName"];
      document.getElementById("party").value = $scope.picks[index]["Party"];
      document.getElementById("age").value = $scope.picks[index]["Age"];

      //$event["currentTarget"].parentNode.parentNode.classList.add("green");
      for (x=0; x < $scope.picks.length; x++){
          if (x == index){
             document.getElementById("Vote " + x).parentNode.parentNode.classList.remove("removegreen");
             document.getElementById("Vote " + x).parentNode.parentNode.classList.add("green");
          }
          if (x == previous && x != index) {
              document.getElementById("Vote " + x).parentNode.parentNode.classList.remove("green");
              document.getElementById("Vote " + x).parentNode.parentNode.classList.add("removegreen");
          }
      }
      previous = index;
  }
})

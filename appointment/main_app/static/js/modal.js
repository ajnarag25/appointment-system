
var modal1 = document.getElementById("myModal1");
var modal2 = document.getElementById("myModal2");

var btn_accept = document.getElementById("myBtnAccept");
var btn_decline = document.getElementById("myBtnDecline");

var span1 = document.getElementsByClassName("close1")[0];
var span2 = document.getElementsByClassName("close2")[0];

var btncancel1 = document.getElementsByClassName("cancel1")[0];
var btncancel2 = document.getElementsByClassName("cancel2")[0];

btn_accept.onclick = function() {
  modal1.style.display = "block";
}
btn_decline.onclick = function() {
    modal2.style.display = "block";
  }

span1.onclick = function() {
  modal1.style.display = "none";
}
span2.onclick = function() {
    modal2.style.display = "none";
  }

btncancel1.onclick = function(){
    modal1.style.display = "none";
}
btncancel2.onclick = function(){
    modal2.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal1) {
    modal1.style.display = "none";
  }
  else if (event.target == modal2) {
    modal2.style.display = "none";
  }
}
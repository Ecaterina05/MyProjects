// Function for responsive dropdown menu ( navigation bar )
function myFunction() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
}


// Function for sliding images 

var i = 0;
var images = [];

images[0] = 'SlideImages/S1.jpg';
images[1] = 'SlideImages/S2.jpg';
images[2] = 'SlideImages/S3.png';
images[3] = 'SlideImages/S4.jpg';
images[4] = 'SlideImages/S5.jpg';

function changeImg() {
	document.slide.src = images[i];

	if (i < images.length - 1) { i++; }
	else { i = 0; }

	setTimeout("changeImg()", 2000);

}
window.onload = changeImg;
//pt schimbarea numelui
function change(){
	var imagini = document.querySelectorAll("figcaption");
	var i = 0; 
	imagini[i].innerHTML = "Leo Beck";
	i++;
	imagini[i].innerHTML = "Bane Perez";
	i++;
	imagini[i].innerHTML = "Joker";
	i++;
	imagini[i].innerHTML = "Jack";
	}
	setTimeout("change()",2000);

//pt schimbarea fontului+culoare	
function stil(id){
  var elem=document.getElementById(id);
  elem.style.color="Red";
  elem.style.fontStyle = "italic";
}

function stilInitial(id){
  var elem=document.getElementById(id);
  elem.style.color="Black";
  elem.style.fontSize="22px";
}

document.getElementById("p1").onmouseover=function(){stil("p2");}
document.getElementById("p1").onmouseout=function(){stilInitial("p2");}

document.getElementById("p3").onmouseover=function(){stil("p4");}
document.getElementById("p3").onmouseout=function(){stilInitial("p4");}

document.getElementById("p5").onmouseover=function(){stil("p6");}
document.getElementById("p5").onmouseout=function(){stilInitial("p6");}

document.getElementById("p7").onmouseover=function(){stil("p8");}
document.getElementById("p7").onmouseout=function(){stilInitial("p8");}

//pt miscarea imaginii

window.onload=move;

function move(){	
	var x=document.getElementById("dw");
	x.addEventListener("click", schimbare);
	x.addEventListener("click",deplasare);
}

function schimbare(){
	var text=document.getElementById("pos");
	text.innerHTML=" Move it with the arrows ";
}

function deplasare()
{ 
 window.onkeydown=function(event)
                {
                var a = event.key;  
				var v=document.getElementById("dw");
               
                if(a == 'ArrowUp') 
					{
						v.style.top = (parseInt(window.getComputedStyle(v).top) - 50) + 'px';
					}
                     
				if(a == 'ArrowLeft') 
					{
						v.style.left = (parseInt(window.getComputedStyle(v).left) - 50) + 'px';
					}
					
                if(a == 'ArrowRight') 
					{
						v.style.left = (parseInt(window.getComputedStyle(v).left) + 50) + 'px';
					}
					
                if(a == 'ArrowDown') 
					{
						v.style.top = (parseInt(window.getComputedStyle(v).top) + 50) + 'px';
					}
                
				}	
  
}





var audio1 = new Audio();
audio1.src = 'http://iss240.net/tempfiles/menu-click/1.mp3';
var audio2 = new Audio();
audio2.src = 'beep-07.mp3';
var audio3 = new Audio();
audio3.src = 'beep-08.mp3';

function playAudio() {

    var id = event.srcElement.id;
    if (id == "bordo"){
        audio1.play();
        alert("riproduco audio bordo")
    }
    else if(id == "interno"){
        audio2.play();
        alert("riproduco audio interno")
    }
    else if(id == "porta"){
        audio3.play();
        alert("riproduco audio porta")
    }
    else if(id == "camera"){
        audio1.play();
        alert("riproduco audio camera")
    }
}
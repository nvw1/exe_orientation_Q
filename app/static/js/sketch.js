let capture;
let picture = [];
let button;

function setup() {
  createCanvas(480, 240);
  capture = createCapture(VIDEO);
  capture.size(320, 240);
  button = createButton('snap');
  button.mousePressed(takesnap);
}

function draw(){
  background(0);
  for(var i = 0; i < picture.length; i++){
    // image(picture[i], 0, 0);
  }
}

function takesnap(){
  picture.push(capture.get());
  console.log(picture);
}
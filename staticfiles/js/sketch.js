let capture;

function setup(){
	createCanvas(640, 480);
	capture = createCapture(VIDEO);
}

function draw(){
background(0);
  if (capture.loadedmetadata) {
    let c = capture.get(0, 0, 100, 100);
    image(c, 0, 0);
  }
}
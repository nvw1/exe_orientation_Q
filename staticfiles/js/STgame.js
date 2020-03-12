function showhint() {
  var lost = document.getElementById("myDIV");
  var hint = document.getElementById("myDIV");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}


function sendRequest(){
        {% for questions in data %}
    var current_question =  {{ questions.node_num }}
        {% endfor %}
    $.ajax({
        url: "/update_request",
        type: "post",
        data: {current_question:current_question,'csrfmiddlewaretoken': "{{ csrf_token }}" },
        success:
        function(result){
            if (result == "Same Question"){
            setTimeout(function(){
                sendRequest(); //this will send request again and again;
            }, 1000);}
            else{
                location.reload(true);
            }
        },
        error: function() {
                    alert("failed")
                    location.reload(true);
                    setTimeout(function(){
                    sendRequest(); //this will send request again and again;
                     }, 5000);
                }
    });
    }
    $(window).bind("load",function(){
        sendRequest();
    })
    $(document).ready(function() {
        var hint_got = false;
        var a = "{{ score }}";
        document.getElementById("score").innerHTML = "High score : " + a ;
        $("#gethint").click(function (e) {
            if (hint_got == false) {
                a--;
                hint_got = true;
            }
            document.getElementById("score").innerHTML = "High score : " + a ;
			e.preventDefault();
            $.ajax({
                url: '/hint',
                type: "post",
                data :{score:a,'csrfmiddlewaretoken': "{{ csrf_token }}"},
                success: function (response) {
                    alert(response);
                },
                error: function(xhr, status, error) {
                    alert("error");
								}
            });
        });
    });
    $(document).ready(function() {
        $("#button_1").click(function (){
            $.ajax({
                url:'/reset_question',
                success: function(response){

                }
            });
        });
    });
    var map_check = "True";
    $(window).bind("load",function(){
        map_check = "{{ map_check }}"
        if (map_check == "True"){
            document.getElementById('myModal').style.display='block';
            initMap();
        }
    });


var x = document.getElementById("demo");

var map, infoWindow, pos, marker, radi, circle;
//CHANGE This is the center coordinate for the circle for checking if player insde. Get this from the databse.
var circPos = {
lat: {{latitude}},
lng:{{ longtitude }}
}

//CHANGE This is the radius of circle. Get this from the database.
radi = 30;

	//Ran at loading of website, intiliazes the map.
      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
		//Change this to the values of the circle. From the database
          center: circPos,
          zoom: 18
        });
        infoWindow = new google.maps.InfoWindow;
        var marker = new google.maps.Marker({
          position: circPos,
          map: map,
          title: 'Hello World!'
        });
        setCompletionZone(circPos, 1);
        infoWindow.open(map);






      }

	  //Checks if player in the circle
function pointInCircle(point, radius, circPos)
{


var p = new google.maps.LatLng(point.lat, point.lng );
var c = new google.maps.LatLng(circPos.lat, circPos.lng);

	if((google.maps.geometry.spherical.computeDistanceBetween(p, c)) >= radius )
	{
		//CHANGE this to whatever you want
		alert("This is your current location. You are not there.");
	}
	else{
		//CHANGE this to whatver you want.
		alert("This is your current location. You are there.");
		document.getElementById('myModal').style.display='none';
		setFalse();
	}
}


//Gets players current location
function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition, showError);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

//Shows position of player on the map.
function showPosition(position) {

    pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            map.setCenter(pos);
			map.setZoom(17);

			marker.setMap(null);

			marker = new google.maps.Marker({
					  map: map,
					  position: pos,
					  title: 'your location'
					});

			pointInCircle(pos, radi, circPos);
}

//Draws circle of the completion zone.
function setCompletionZone(posi, radi){

  					marker = new google.maps.Marker({
					  map: map,
					  position: posi,
					  title: 'circle centre'
					});

					circle = new google.maps.Circle({
					  map: map,
					  radius: radi,
					     strokeColor: '#FF0000',
					strokeOpacity: 0.8,
					strokeWeight: 2,
					fillColor: '#FF0000',
					fillOpacity: 0.35
					});
					circle.bindTo('center', marker, 'position');

					marker.setMap(null);


}

//Error handling for location request.
function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      x.innerHTML = "User denied the request for Geolocation."
      break;
    case error.POSITION_UNAVAILABLE:
      x.innerHTML = "Location information is unavailable."
      break;
    case error.TIMEOUT:
      x.innerHTML = "The request to get user location timed out."
      break;
    case error.UNKNOWN_ERROR:
      x.innerHTML = "An unknown error occurred."
      break;
  }



}

function setFalse(){
           $.ajax({
                url:'/set_map_false',
                success: function(response){

                }
            });
}



</script>

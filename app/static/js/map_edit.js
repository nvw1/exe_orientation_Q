function initMap() {
	// make the map
  var map = new google.maps.Map(
    document.getElementById('map2'), {
      zoom: 17,
      center: new google.maps.LatLng(50.726, -3.531)
    });
	// put the marker on the map
  var myMarker = new google.maps.Marker({
    position: new google.maps.LatLng(50.737, -3.535),
    map: map,
    draggable: true
  });

//   fill in the elements with latitude and longitud of the marker
  google.maps.event.addListener(myMarker, 'dragend', function(evt) {
	document.getElementById('lat_edit').value = evt.latLng.lat().toFixed(6);
    document.getElementById('lng_edit').value = evt.latLng.lng().toFixed(6);
  });

  map.setCenter(myMarker.position);
  myMarker.setMap(map);

}
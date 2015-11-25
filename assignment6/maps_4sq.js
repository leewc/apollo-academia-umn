var droppedMarker;

function initMap() {
    directionsService = new google.maps.DirectionsService;
    directionsDisplay = new google.maps.DirectionsRenderer;
    map = new google.maps.Map(document.getElementById('map'), {
	center: {lat: 44.974802, lng:-93.235301 }, 
	zoom: 16
	});
    listenToMapClicksAndDropMarker();
/*    buildings = loadBuildings();
    buildingSelector = document.getElementById("buildingSelector");
    generateMarkersAndCards();
    populateSelector();
    


    //bind onchange event handler to route calculator function
    var onChangeHandler = function() {
	displayRoute = true; //start displaying route after first change.
	calculateAndDisplayRoute(directionsService, directionsDisplay);
	};
    buildingSelector.addEventListener('change', onChangeHandler);
    document.getElementById('travelSelector').addEventListener('change', onChangeHandler);
*/
}


function listenToMapClicksAndDropMarker(){
    map.addListener('click', function(event){
	if(droppedMarker != null)
	{//clears previous marker, only one
	    droppedMarker.setMap(null);
	    }
	droppedMarker = new google.maps.Marker({
	    position : event.latLng,
	    map: map,
	    title : 'Location: ' + event.latLng.lat() + ', ' + event.latLng.lng(),
	    });
	//call route display (will check if building is selected)
	// needed to ensure route changes on new marker
//	calculateAndDisplayRoute(directionsService, directionsDisplay)
	});
}

function validate(form){
    if(droppedMarker == null){
	window.alert("Please, drop a marker on the map for nearby places!");
	return false;
    }
    var lat = document.createElement("input");
    lat.type = 'hidden';
    lat.name = 'lat';
    lat.value = droppedMarker.getPosition().lat();
    
    var lng = document.createElement("input");
    lng.type = 'hidden';
    lng.name = 'lng';
    lng.value = droppedMarker.getPosition().lng();

    form.limitDisplay.name =""; //remove from POST data
    form.radiusDisplay.name="";

    form.appendChild(lat);
    form.appendChild(lng);
    form.submit();
    return true;
}

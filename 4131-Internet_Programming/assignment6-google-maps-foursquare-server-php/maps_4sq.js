var droppedMarker;
var latLng;
var fourSquareData;

function initMap() {
    directionsService = new google.maps.DirectionsService;
    directionsDisplay = new google.maps.DirectionsRenderer;
    map = new google.maps.Map(document.getElementById('map'), {
	center: {lat: 44.974802, lng:-93.235301 }, 
	zoom: 16
	});
    listenToMapClicksAndDropMarker();
    loadData();
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
	});
}

function validate(form){
    if(droppedMarker == null){
	window.alert("Please, drop a marker on the map for nearby places!");
	return false;
    }
    prepFormData(form);
    form.submit();
    return true;
}

function prepFormData(form)
{
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
}

function loadData(){
    if(latLng == null)
	return false; //either first visit or no data POSTed
    droppedMarker = new google.maps.Marker({
	    position : latLng,
	    map: map,
	    title : 'Location: ' + latLng.lat + ', ' + latLng.lng,
	    });
    //center the map
    map.setCenter(latLng);

    if(fourSquareData == null)
	return false;

    fourSquareData.response.venues.forEach(makeMarker);
    return true;
}

function makeMarker(venue){
    if(venue === undefined) //safety check
	return; //http://stackoverflow.com/questions/3390396/how-to-check-for-undefined-in-javascript

    var marker = new google.maps.Marker({
	position: { lat: venue.location.lat, lng: venue.location.lng },
	map: map,
	title: venue.name,
	icon: venue.categories[0].icon.prefix+'bg_32'+venue.categories[0].icon.suffix
    });
    
    //Can also prepare information for infocard and map to content key in infowindow
    //var contentString = <div>htmlstuff</div>
    //Address can be undefined if there is no set point
    var address = ( (venue.location.address !== undefined) ? venue.location.address : venue.location.formattedAddress.toString());
    var infowindow = new google.maps.InfoWindow({
	content: 
	'<div id="content">'+
	    '<div id="siteNotice">'+
	    '</div>'+
	    '<h1 id="firstHeading" class="firstHeading">' + venue.name + '</h1>'+
	    '<p><b> Address: </b><br/>' + address + '</p>' +
	    '<p><b> Latitude: </b>' + venue.location.lat + '</p>' +
	    '<p><b> Longtitude: </b>' + venue.location.lng + '</p>',
	maxWidth: 400
	});

    //Add infowindow key to each marker, to avoid only having a reference to last marker
    marker.infowindow = infowindow;

    marker.addListener('click', function() {
	return this.infowindow.open(map, this);
	});
}

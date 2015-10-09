var map;
var buildings;
var markers = [];

function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
		center: {lat: 44.974802, lng:-93.235301 }, 
		zoom: 16
	});
	buildings = loadBuildings();
	generateMarkersAndCards();
	listenToMapClicksAndDropMarker();
}

function Building(name, imgPath, latitude, longtitude, architect, description){
	this.name = name;
	this.architect = architect;
	this.description = description;

	this.latLong = {lat: latitude, lng: longtitude}; //same as new google.maps.LatLng

	this.image = new Image();
	this.image.src = "building_images/" + imgPath;
}

function loadBuildings() {
	return new Array(
		new Building("Armory", "armory.jpg", 44.977276, -93.232266, "Charles Aldrich", "Built for athletics and military drill, as well as performing arts and social activities. Memorial plaques at the front entrance honor students, faculty, and alumni who fought in the Spanish-American War."),
		new Building("Pillsbury Hall", "pillsbury.jpg",44.977018, -93.234444,"Leroy Buffington with Harvey Ellis", "Built as Science Hall. Named for Governor John S. Pillsbury."),
		new Building("Folwell Hall", "folwell.jpg", 44.978354, -93.234409, "Clarence H. Johnston, Sr.", "When Old Main burned in 1904, Folwell Hall was built to house displaced departments. Named for William Watts Folwell, first president of the University, 1869-84. "),
		new Building("Jones Hall", "jones.jpg", 44.977995, -93.235415, "Charles Aldrich", "Built as Physics Building. Named for Frederick S. Jones, professor of physics and dean of the College of Engineering."),
		new Building("Pillsbury Statue", "pillsbury.jpg", 44.978239, -93.236964, "Daniel C. French, sculptor", "Pillsbury statue located across the street from Burton Hall."),
		new Building("Wesbrook Hall", "statue.jpg", 44.976662, -93.236310, "Frederick Corser", "Built as Laboratory of Medical Science. In 1912, dentistry moved here. Named for Frank Wesbrook, professor of pathology and bacteriology and dean of the College of Medicine and Surgery."),
		new Building("Nicholson Hall", "nicholson.jpg", 44.977197, -93.235973, "LeRoy Buffington with Harvey Ellis", "Built as chemical laboratory. In 1914, chemistry moved to the mall area and Nicholson was remodeled for the men's union until Coffman Memorial Union was built as a coed student union. Named for Edward E. Nicholson, professor of chemistry and later dean of Student Affairs."),
		new Building("Eddy Hall", "eddy.jpg", 44.977679, -93.236707, "LeRoy Buffington", "Built as Mechanic Arts. It is the oldest existing building on campus. Named for Henry Turner Eddy, professor of engineering and mathematics and dean of the Graduate School."),
		new Building("Music Education", "music.jpg", 44.971201, -93.241777, "Warren H. Hayes", "Built as Student Christian Association building. Acquired by the University, it housed Child Welfare and Music Education."),
		new Building("Wulling Hall","wulling.jpg", 44.976306, -93.237437, "Allen Stem and Charles Reed", "Built as Medical Hall; named Millard Hall in 1906. Fire damaged the building. It later became the site for the pharmacy building. Named for Frederick J. Wulling, first dean and founder of the College of Pharmacy. ")
		
		
		);
}

function generateMarkersAndCards(){
	for (var i = 0; i < buildings.length; ++i){
		var building = buildings[i];

		var marker = new google.maps.Marker({
			position: building.latLong,
			map: map,
			title: building.name,
			icon: "icon.png"
		});

		//Can also prepare information for infocard and map to content key in infowindow
		//var contentString = <div>htmlstuff</div>
			
		var infowindow = new google.maps.InfoWindow({
			content: 
			'<div id="content">'+
      		'<div id="siteNotice">'+
      		'</div>'+
      		'<h1 id="firstHeading" class="firstHeading">' + building.name + '</h1><br/>'+
      		' <p><b> Architect: ' + building.architect + '</b></p><div id="bodyContent"><br/>' +
      		'<p>' + building.description + '</p>' +
      		'<img src="' + building.image.src + '"/>',
      		maxWidth: 489 //to make it look as close to provided screenshot as possible
		});

		//Add infowindow key to each marker, to avoid only having a reference to last marker
		marker.infowindow = infowindow;

		// Alternate way of adding infowindow listeners
		// google.maps.event.addListener(marker, 'click', function() {
		// 	this.infowindow.open(map, this); 
  		//     		});

		marker.addListener('click', function() {
			return this.infowindow.open(map, this);
		});

		markers.push(marker);
	}
}

function listenToMapClicksAndDropMarker(){
	map.addListener('click', function(event){
		var marker = new google.maps.Marker({
			position : event.latLng,
			map: map,
			title : event.latLng.lat() + ', ' + event.latLng.lng(),
			infowindow : new google.maps.InfoWindow({
				content: 'Hello'
				}) 
		});
		marker.addListener('click', function() {
			return this.infowindow.open(map, this);
		});
	});
}
var buildings;
var selectedImage;
var selectedBuilding;
var selectedId;
var thumbnails;
var started;

function setUp(){
	buildings = initBuildings();
	loadThumbnails();
	started = false;
}

function Building(name, imgPath, year, architect, description){
	this.name = name;
	this.year = year;
	this.architect = architect;
	this.description = description;

	this.image = new Image();
	this.image.src = "images/" + imgPath;
}

function initBuildings(){
	return new Array(
		new Building("Armory", "armory.jpg",1896,"Charles Aldrich", "Built for athletics and military drill, as well as performing arts and social activities. Memorial plaques at the front entrance honor students, faculty, and alumni who fought in the Spanish-American War."),
		new Building("Pillsbury Hall", "pillsbury.jpg", 1889,"Leroy Buffington with Harvey Ellis", "Built as Science Hall. Named for Governor John S. Pillsbury."),
		new Building("Folwell Hall", "folwell.jpg", 1907, "Clarence H. Johnston, Sr.", "When Old Main burned in 1904, Folwell Hall was built to house displaced departments. Named for William Watts Folwell, first president of the University, 1869-84. "),
		new Building("Jones Hall", "jones.jpg", 1901, "Charles Aldrich", "Built as Physics Building. Named for Frederick S. Jones, professor of physics and dean of the College of Engineering."),
		new Building("Pillsbury Statue", "pillsbury.jpg", 1900, "Daniel C. French, sculptor", "Pillsbury statue located across the street from Burton Hall."),
		new Building("Wesbrook Hall", "statue.jpg", 1898, "Frederick Corser", "Built as Laboratory of Medical Science. In 1912, dentistry moved here. Named for Frank Wesbrook, professor of pathology and bacteriology and dean of the College of Medicine and Surgery."),
		new Building("Nicholson Hall", "nicholson.jpg", 1890, "LeRoy Buffington with Harvey Ellis", "Built as chemical laboratory. In 1914, chemistry moved to the mall area and Nicholson was remodeled for the men's union until Coffman Memorial Union was built as a coed student union. Named for Edward E. Nicholson, professor of chemistry and later dean of Student Affairs."),
		new Building("Eddy Hall", "eddy.jpg", 1886, "LeRoy Buffington", "Built as Mechanic Arts. It is the oldest existing building on campus. Named for Henry Turner Eddy, professor of engineering and mathematics and dean of the Graduate School."),
		new Building("Music Education", "music.jpg", 1888, "Warren H. Hayes", "Built as Student Christian Association building. Acquired by the University, it housed Child Welfare and Music Education."),
		new Building("Wulling Hall","wulling.jpg", 1892, "Allen Stem and Charles Reed", "Built as Medical Hall; named Millard Hall in 1906. Fire damaged the building. It later became the site for the pharmacy building. Named for Frederick J. Wulling, first dean and founder of the College of Pharmacy. ")
		);
}

function loadThumbnails(){
	thumbnails = document.getElementById("thumbnails");
	for (var i = 0; i < buildings.length; ++i){
		thumb = document.createElement("img");
		thumb.src = buildings[i].image.src;
		thumb.id = i;
		thumb.onclick = function(){ setBorderAndBuilding(this); }
		thumbnails.appendChild(thumb);
	}
}

function startShow(){
	started = true;
	setBorderAndBuilding(document.getElementById("0"));
	theatreDisplay();
}

function next(){
	if(!started)
		return;

	selectedId++;
	if(selectedId == buildings.length)
		selectedId = 0;
	setBorderAndBuilding(document.getElementById(selectedId));
}

function prev(){
	if(!started)
		return;

	selectedId--;
	if(selectedId == -1)
		selectedId = buildings.length - 1;
	setBorderAndBuilding(document.getElementById(selectedId));
}

function setBorderAndBuilding(self) {
	if(!started)
		return;
	if(selectedImage != null)
		selectedImage.style.borderStyle = "none"; //unset border
	selectedImage = self;
	selectedImage.style.borderStyle = "solid";
	selectedImage.style.borderColor = "red";

	selectedId = parseInt(self.id);
	selectedBuilding = buildings[selectedId];

	theatreDisplay();
	updateInfoPanel();
}

function theatreDisplay(){
	var imgTheatre = document.getElementById("theatre");
	imgTheatre.src = selectedBuilding.image.src;
}

function updateInfoPanel(){
	var infoPanel = document.getElementById("infoPanel");
	var infoTypeSelection = document.getElementById("infoTypeSelection");
	infoType = infoTypeSelection.options[infoTypeSelection.selectedIndex].value;

	var buildingInfo = "<b> Building: " + selectedBuilding.name + "</b> <br />";

	switch (infoType){
		case "none":
			break;
		case "architect":
			buildingInfo += "<b> Architect: " + selectedBuilding.architect + "</b>"; 
			break;
		case "year":
			buildingInfo += "<b> Year: " + selectedBuilding.year +"</b>";
			break;
		case "description":
			buildingInfo += "<b> Description: " + selectedBuilding.description + "</b>";
			break;
	}
	infoPanel.innerHTML = buildingInfo;
}
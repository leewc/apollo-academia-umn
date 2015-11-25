<?php
  define("ERROR", 0);
  define("SUCCESS", 1);

  class Model {
   	private $data; //so the controller can change values, removes need for overloading accessors.. (small assignment)

	private function __construct(){
		$this->data = array("","","","","","","","","","limit"=>25, "radius"=>1500); //initial values for the form
	}

	public static function getInstance(){
            static $instance = null;
            if ($instance == null){
               $instance = new Model();
       	    }
            return $instance;
	}

	public function check($index){ //changes data array to 'checked'
	    $this->data[$index] = "checked";
	}

	public function setLimit($value){
	    $this->data['limit'] = $value;
	}

	public function setRadius($value){
	    $this->data['radius'] = $value;
 	}

	public function setLatLng($lat, $lng){
	    $this->data['lat'] = $lat;
	    $this->data['lng'] = $lng;
	}

	public function getData(){
	    return $this->data;
	}
  }

  class FourSq {
  	private $oauth;
	private $date;
   	private $categories; 

	private function __construct(){
		$this->oauth = "CCFSLVQBHPZZTSVNATADJEYJZIBPPYOQM0B50NWMZ0K42QJV";
		$this->date = "20151114";
		$this->categories = array("4d4b7104d754a06370d81259", 
	              	           "4d4b7105d754a06374d81259",
			    	   "4d4b7105d754a06376d81259",
			    	   "4d4b7105d754a06377d81259",
			    	   "4d4b7105d754a06378d81259",
			    	   "4d4b7105d754a06379d81259",
			    	   "4d4b7105d754a06372d81259",
			    	   "4d4b7105d754a06375d81259",
			    	   "4e67e38e036454776db1fb3a");
	}

	public static function getInstance(){
            static $instance = null;
            if ($instance == null){
               $instance = new FourSq();
       	    }
            return $instance;
	}

	public function query($data){
	       $lat = $data['lat'];
	       $lng = $data['lng'];
	       $limit = $data['limit'];
	       $radius = $data['radius'];
	       $selectedCategories = "";

	       if(!in_array("checked", $data)){
	            $selectedCategories = implode(",",$this->categories);
	       }
	       else {
	            for($i = 0; $i < count($this->categories); $i++){
		     	   if($data[$i] == "checked"){
			    	$selectedCategories .= $this->categories[$i] .",";
			   }
		    }
		    $selectedCategories = rtrim($selectedCategories,",");
	       }

	       
	       $query = "https://api.foursquare.com/v2/venues/search?ll=$lat,$lng&intent=browse&oauth_token=$this->oauth&limit=$limit&radius=$radius&categoryId=$selectedCategories&v=$this->date";
	       echo ""
	       echo $query;
	       return $query;
	}
  } 

?>
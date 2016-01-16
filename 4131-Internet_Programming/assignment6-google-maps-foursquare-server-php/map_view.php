<?php

class View { 
      private $view;
      private $model;	
      private function __construct(){
       	      $this->model = Model::getInstance(); 
      }

      public static function getInstance(){
       	     static $instance = null;
	     if ($instance == null){
	      	$instance = new View();
 	     }
	     return $instance;
      }

      public function display($option, $json){
       	     switch($option){
		default:
			$index = file_get_contents("index.html");
			$data = $this->model->getData();
			$index = str_replace("{{form}}", Template::form($data), $index);

			if(!isset($_SESSION["error"])){
				$_SESSION["error"] = "";
			}

			if($json == ""){
				$index = str_replace("{{jsdata}}", "", $index);
			}
			else{
				$jsdata = array("latLng" =>"{ lat: ".$data['lat'].", lng: ".$data['lng']." }");
				$jsdata['fourSquareData'] = $json;
		    		$index = str_replace("{{jsdata}}", $this->loadJSVar($jsdata), $index);
			}
			echo $index;
		}
      }

      public function loadJSVar($jsdata)
      {
         $jsString = "<script type='text/javascript'>\n";
	 foreach($jsdata as $var => $val){
	 	$jsString .= "$var = $val ; \n";
	 } 
	 $jsString .= "</script>";
	 return $jsString;
      }

}
?>
<?php
  ini_set('display_errors', '1');
  error_reporting(E_ALL | E_STRICT);   
  
  include "map_model.php";
  include "map_view.php";
  include "map_template.php";

  class Controller { 
   	private $view;
	private $model;
	public function __construct(){
	       $this->view = View::getInstance();	
	       $this->model = Model::getInstance();	
	}

	public function processdata($POST){
	       if(empty($_POST)){
		    $this->view->display("default", ""); //no json data yet
	       }
	       else {
	            if(isset($POST['category']))
		    {
			foreach($POST['category'] as $i => $value)
			{
			   $this->model->check($value); //value holds the actual index of selection
			}
		    }
		    $this->model->setLimit($POST['limit']);
		    $this->model->setRadius($POST['radius']);
		    $this->model->setLatLng($POST['lat'], $POST['lng']);

		    $json = $this->model->execute();
		    $this->view->display("default", $json);
    		    //print_r($this->model->getData());
 		}
 	}
}
	
$controller = new Controller();
$controller->processData($_POST);
?>
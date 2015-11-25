<?php
  ini_set('display_errors', '1');
  error_reporting(E_ALL | E_STRICT);   
  
  include "map_model.php";
  include "map_view.php";
  include "map_template.php";

  class Controller { 
   	private $view;
	private $model;
	private $foursq;
	public function __construct(){
	       $this->view = View::getInstance();	
	       $this->model = Model::getInstance();
	       $this->foursq = FourSq::getInstance();	
	}

	public function processdata($POST){
	       if(empty($_POST)){
		    $this->view->display("default");
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
		    print_r($this->model->getData());
		    $this->foursq->query($this->model->getData());
		    //foreach($POST as $key=> $value)
		    //    echo "<br>".$key."--> ".$value."</br>";
		    $this->view->display("default");
 		}
 	}
}
	
$controller = new Controller();
$controller->processData($_POST);
?>
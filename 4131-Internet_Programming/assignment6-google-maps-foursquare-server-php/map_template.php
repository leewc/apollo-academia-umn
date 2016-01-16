<?php
class Template { 
      public static function form($data){
      	     return <<<FORM
<div id="floating-panel-left">
<form name="mapForm" action="map_controller.php" method="POST" enctype="multipart/form-data" onsubmit="return validate(this)">
<input type='checkbox' name='category[]' value='0' $data[0] > Arts & Entertainment </input>
<input type='checkbox' name='category[]' value='1' $data[1] > Food </input>
<input type='checkbox' name='category[]' value='2' $data[2] > Nightlife Spot </input>
<input type='checkbox' name='category[]' value='3' $data[3] > Outdoor & Recreation </input>
<input type='checkbox' name='category[]' value='4' $data[4] > Shop & Service </input>
<input type='checkbox' name='category[]' value='5' $data[5] > Travel & Transport </input>
<input type='checkbox' name='category[]' value='6' $data[6] > College & Universities </input>
<input type='checkbox' name='category[]' value='7' $data[7] > Professional & Other Places </input>
<input type='checkbox' name='category[]' value='8' $data[8] > Residence </input>    
Limit (K):
<input type='range' name='limit' min=0 max=50 value={$data["limit"]} oninput="limitDisplay.value = limit.value"/>
<input type='text' name='limitDisplay' value={$data["limit"]} readonly/>
Radius (M): 
<!-- Decided to put oninput js code here for simplicity -->
<input type='range' name='radius' min=0 max=3000 step=100 value={$data["radius"]} oninput="radiusDisplay.value = radius.value"/>
<input type='text' name='radiusDisplay' value={$data["radius"]} readonly/> 
<input type='submit' value='Submit'/>
</form>  
</div>
FORM;
      }
}
?>
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Nearby Places </title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
<?php if (empty($_POST)): ?>

  <div id="map"> </div>
<?php else:
      foreach($_POST['category'] as $k => $v)
         print("<b> $k ... $v </b>");
      foreach($_POST as $key => $value)
         print("<b>$key, $value .......</b>");
?>
<?php endif; ?>

  <div id="floating-panel-left">
  <form name="mapForm" action="index.php" method="POST" enctype="multipart/form-data" onsubmit="return validate(this)">
    <input type='checkbox' name='category[]' value='4d4b7104d754a06370d81259'> Arts & Entertainment </input>
    <input type='checkbox' name='category[]' value='4d4b7105d754a06374d81259'> Food </input>
    <input type='checkbox' name='category[]' value='4d4b7105d754a06376d81259'> Nightlife Spot </input>
    <input type='checkbox' name='category[]' value='4d4b7105d754a06377d81259'> Outdoor & Recreation </input>
    <input type='checkbox' name='category[]' value='4d4b7105d754a06378d81259'> Shop & Service </input>
    <input type='checkbox' name='category[]' value='4d4b7105d754a06379d81259'> Travel & Transport </input>
    <input type='checkbox' name='category[]' value='4d4b7105d754a06372d81259'> College & Universities </input>
    <input type='checkbox' name='category[]' value='4d4b7105d754a06375d81259'> Professional & Other Places </input>
    <input type='checkbox' name='category[]' value='4e67e38e036454776db1fb3a'> Residence </input>
    
    Limit (K):
    <input type='range' name='limit' min=0 max=50 value=25 oninput="limitDisplay.value = limit.value"/>
    <input type='text' name='limitDisplay' value='25' readonly/>
    Radius (M): 
    <!-- Decided to put oninput js code here for simplicity -->
    <input type='range' name='radius' min=0 max=3000 step=100 value=1500 oninput="radiusDisplay.value = radius.value"/>
    <input type='text' name='radiusDisplay' value='1500' readonly/> 
    
    <input type='submit' value='Submit'/>
  </form>  
  </div>

  <script type="text/javascript" src="maps_4sq.js"></script>
  <!-- NOTE TO SELF: REVOKE API KEY AFTER ASSIGNMENT -->
  <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAJ7qcWfRp3G1TnhP9PgXXBF4FCkr3TRGw&callback=initMap" async defer></script>
</body>
</html>
﻿<?php
$type = $_GET['type'];
$yy = 100;
if($type == "single"){
  $algo = $_GET['algo1'];

  if($algo == "pso"){
    $noOfParticles = $_GET['particles'];
    $functionCode = $_GET['functionCode'];
    $noOfIttration = $_GET['iteration'];
  }
  elseif($algo == "abc"){

  }

}
else{
  $algo1 = $_GET['algo1'];
  $algo2 = $_GET['algo2'];
//retrive algo 1 detail
  if($algo1 == "pso"){
    $noOfParticles1 = $_GET['noOfParticles1'];
    $functionCode1 = $_GET['functionCode1'];
    $noOfIttration1 = $_GET['noOfIttration1'];
  }
  elseif($algo1 = "abc"){

  }

  //retrieve algo 2 detail
  if($algo2 == "pso"){
    $noOfParticles2 = $_GET['noOfParticles2'];
    $functionCode2 = $_GET['functionCode2'];
    $noOfIttration2 = $_GET['noOfIttration2'];
  }
  elseif($algo2 = "abc"){

  }


}

?>

<!DOCTYPE HTML>
<html>

<head>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script type="text/javascript">

	function plot(data) {

		var list = [
		];

		max = parseInt(data["length"]);
		var i;
		for(i = 0 ; i  < max ; i++){
			var t ={};
			t["x"] = parseFloat(data[i.toString()]["ittration"]);
			t["y"] = parseFloat(data[i.toString()]["bestSolForIttration"]);
			list.push(t);
		}
		 console.log(list);
		
			var chart = new CanvasJS.Chart("chartContainer", {
				title: {
					text: "PSO ittrations : x -> ittrations , y -> values"
				},
				data: [
				{
					type: "spline",
					showInLegend: true,
					name: "PSO",
					dataPoints: list
				}
				],

			});

			chart.render();

} 

	$.ajax({
                    url: "http://192.168.0.115:8000/pso_algorithm/run/?noOfParticles=<?php echo $noOfParticles ?>&functionCode=<?php echo $functionCode ?>&noOfIttration=<?php echo $noOfIttration ?>",
                    type: 'GET',
                    success: function(data){
                    	let jsonObject = JSON.parse(data);
                    		
                            plot(jsonObject);
                    },
                    error:function(){
                        
                    },
            });

	</script>
	<script src="../../canvasjs.min.js"></script>
	<title>CanvasJS Example</title>
</head>
<body>
	<div id="chartContainer" style="height: 400px; width: 100%;">
	</div>
</body>
</html>
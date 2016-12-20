<?php
$type = $_GET['type'];
$url = "http://192.168.0.109:8000/";
if($type == "single"){
  $algo = $_GET['algo1'];

  if($algo == "pso"){
    $noOfParticles = $_GET['particles'];
    $functionCode = $_GET['functionCode'];
    $noOfIttration = $_GET['iteration'];
    $lower_bound = $_GET['min_v'];
  	$upper_bound = $_GET['max_v'];
    $url = $url."pso_algorithm/run/?noOfParticles=".$noOfParticles."&functionCode=".$functionCode."&noOfIttration=".$noOfIttration."&min_v=".$lower_bound."&max_v=".$upper_bound;

  }
  elseif($algo == "abc"){
  	$np = $_GET['particles'];
  	$maxCycle = $_GET['iteration'];
  	$dimensions = $_GET['variables'];
  	$lower_bound = $_GET['min_v'];
  	$upper_bound = $_GET['max_v'];
  	$function = $_GET['functionCode'];
  	$url = $url."abc_algorithm/run?np=".$np."&function=".$function."&lower=".$lower_bound."&upper=".$upper_bound."&n_gen=".$maxCycle."&d=".$dimensions;


  }
  elseif($algo == "bat"){

  	$np = $_GET['particles'];
  	$n_gen = $_GET['iteration'];
  	$d = $_GET['variables'];
  	$lower_bound = $_GET['min_v'];
  	$upper_bound = $_GET['max_v'];
  	$function = $_GET['functionCode'];
  	$a = $_GET['a1'];
  	$r = $_GET['r1'];
  	$qmin = $_GET['qmin1'];
  	$qmax = $_GET['qmax1'];

  	$url = $url."bat_algorithm/run?d=".$d."&np=".$np."&n_gen=".$n_gen."&a=".$a."&r=".$r."&qmin=".$qmin."&qmax=".$qmax."&lower=".$lower_bound."&upper=".$upper_bound."&function=".$function;

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
			t["x"] = parseFloat(i);
			t["y"] = parseFloat(data[i.toString()]["bestSolutionForIteration"]);
			list.push(t);
		}
		 // console.log(list);
		
			var chart = new CanvasJS.Chart("chartContainer", {
				title: {
					text: "<?php echo $algo; ?> : x -> ittrations , y -> values"
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
                    url: "<?php echo $url ?>",
                    type: 'GET',
                    success: function(data){
                      console.log(data);
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
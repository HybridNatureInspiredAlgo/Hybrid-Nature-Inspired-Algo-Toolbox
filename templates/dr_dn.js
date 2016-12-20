 function dropdownlist(listindex)
 {
 	document.getElementById('compare').style.display = 'block';

 	document.formname.algo1.options.length = 0;
 	switch (listindex)
 	{

 		case " " :
 		document.formname.algo1.options[0]=new Option("Select algo1","");
 		break;

 		case "algo" :
 		document.formname.algo1.options[0]=new Option("Select Algo1","");
 		document.formname.algo1.options[1]=new Option("PSO","pso");
 		document.formname.algo1.options[2]=new Option("ABC","abc");
 		document.formname.algo1.options[3]=new Option("Firefly","firefly");
 		document.formname.algo1.options[4]=new Option("Grey Wolf","grey-wolf");
 		document.formname.algo1.options[5]=new Option("BAT","bat");

 		document.formname.algo2.options[0]=new Option("Select Algo2","");
 		document.formname.algo2.options[1]=new Option("PSO","pso");
 		document.formname.algo2.options[2]=new Option("ABC","abc");
 		document.formname.algo2.options[3]=new Option("Firefly","firefly");
 		document.formname.algo2.options[4]=new Option("Grey Wolf","grey-wolf");
 		document.formname.algo2.options[5]=new Option("BAT","bat");

 		break;
 	}
 	return true;
 }


 function algoselection1(listindex)
 {
 	// document.getElementById('compare').style.display = 'block';

 	// document.formname.algo1.options.length = 0;
 	switch (listindex)
 	{

 		case " " :
 		document.formname.algo1.options[0]=new Option("Select algo1","");
 		break;

 		case "bat" :
 		document.getElementById('v11').name='a1';
 		document.getElementById('v11').type='tel'
 		document.getElementById('v11').placeholder = "Loudness";
 		document.getElementById('v12').name='r1';
 		document.getElementById('v12').type='tel'
 		document.getElementById('v12').placeholder = "PulseRate";
 		document.getElementById('v13').name='qmin1';
 		document.getElementById('v13').type='tel'
 		document.getElementById('v13').placeholder = "Frequency Minimum";
 		document.getElementById('v14').name='qmax1';
 		document.getElementById('v14').type='tel'
 		document.getElementById('v14').placeholder = "Frequency Maximum";

 		
 		break;

 	}
 	return true;
 }


function algoselection2(listindex)
 {
 	switch (listindex)
 	{

 		case " " :
 		document.formname.algo1.options[0]=new Option("Select algo1","");
 		break;

 		case "bat" :
 		document.getElementById('v21').name='a2';
 		document.getElementById('v21').type='tel'
 		document.getElementById('v21').placeholder = "Loudness";
 		document.getElementById('v22').name='r2';
 		document.getElementById('v22').type='tel'
 		document.getElementById('v22').placeholder = "PulseRate";
 		document.getElementById('v23').name='qmin2';
 		document.getElementById('v23').type='tel'
 		document.getElementById('v23').placeholder = "Frequency Minimum";
 		document.getElementById('v24').name='qmax2';
 		document.getElementById('v24').type='tel'
 		document.getElementById('v24').placeholder = "Frequency Maximum";

 		
 		break;

 	}
 	return true;
 }



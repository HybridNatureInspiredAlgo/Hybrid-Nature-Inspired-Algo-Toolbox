 function dropdownlist(listindex)
 {


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

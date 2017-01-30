var months=new Array();
months["January"]=new Array();
months["January"]["name"]="January";
months["January"]["next"]="February";
months["January"]["previous"]="December";

months["February"]=new Array();
months["February"]["name"]="February";
months["February"]["next"]="March";
months["February"]["previous"]="January";

months["March"]=new Array();
months["March"]["name"]="March";
months["March"]["next"]="April";
months["March"]["previous"]="February";

months["April"]=new Array();
months["April"]["name"]="April";
months["April"]["next"]="May";
months["April"]["previous"]="March";

months["May"]=new Array();
months["May"]["name"]="May";
months["May"]["next"]="June";
months["May"]["previous"]="April";

months["June"]=new Array();
months["June"]["name"]="June";
months["June"]["next"]="July";
months["June"]["previous"]="May";

months["July"]=new Array();
months["July"]["name"]="July";
months["July"]["next"]="August";
months["July"]["previous"]="June";

months["August"]=new Array();
months["August"]["name"]="August";
months["August"]["next"]="September";
months["August"]["previous"]="July";

months["September"]=new Array();
months["September"]["name"]="September";
months["September"]["next"]="October";
months["September"]["previous"]="August";

months["October"]=new Array();
months["October"]["name"]="October";
months["October"]["next"]="November";
months["October"]["previous"]="September";

months["November"]=new Array();
months["November"]["name"]="October";
months["November"]["next"]="December";
months["November"]["previous"]="October";

months["December"]=new Array();
months["December"]["name"]="December";
months["December"]["next"]="January";
months["December"]["previous"]="November";
		
		
	
	
	//document.getElementById('month').value=months["Jenuary"]["next"];
	
	function next(){
		var cur=document.getElementById('month').innerHTML;
		var temp=cur.split(" ");
		var month=temp[0];
		var year=temp[1];
		if(month=="December"){
			year=(parseInt(year)+1).toString();
		}
		var last=months[month]["next"]+" "+year;
		month=months[month]["next"];
		document.getElementById('month').innerHTML=last;
		var temp=document.getElementById('form');
		var name = temp.options[temp.selectedIndex].text;
		if (name == "---------"){
			alert("Choose a partner");
		}
		else{
			
			send(month,year,name);
		}		
	}
	
	function previous(){
		var cur=document.getElementById('month').innerHTML;
		var temp=cur.split(" ");
		var month=temp[0];
		var year=temp[1];
		if(month=="January"){
			year=(parseInt(year)-1).toString();
		}
		var last=months[month]["previous"]+" "+year;
		month=months[month]["previous"];
		document.getElementById('month').innerHTML=last;
		var temp=document.getElementById('form');
		var name = temp.options[temp.selectedIndex].text;
		if (name == "---------"){
			alert("Choose a partner");
		}
		else{
			
			send(month,year,name);
		}
	}
	
	function send( month, year,name){
		$.ajax({
			url:"/water/customersserved",
			type:"POST",
			data:{'month':month,'year':year,'name':name},
			datatype:"json",
			success:function(resp){
				var obj=JSON.parse(resp.data);
				var i,j;
				//console.log(obj[0].fields.Promo_Code);
				
				createdom(obj);
				
			}
		});
		//console.log(cur);
	}


	function createdom(data){
		var div=document.getElementById("trapezi");
		div.innerHTML="";
		var table=document.createElement("table");
		table.setAttribute('class',"table table-hover table-striped");
		div.appendChild(table);
		var thead=document.createElement("thead");
		table.appendChild(thead);
		var tr=document.createElement("tr");
		thead.appendChild(tr);
		//HEADERS
		var th=document.createElement("th");
		th.innerHTML="Promo Code";
		tr.appendChild(th);
		
		
		th=document.createElement("th");
		th.innerHTML="First Name";
		tr.appendChild(th);
		
		
		th=document.createElement("th");
		th.innerHTML="Surname";
		tr.appendChild(th);
		
		
		th=document.createElement("th");
		th.innerHTML="Order Date";
		tr.appendChild(th);
		/////////
		
		
		//BODY/ELEMENTS
		
		var tbody=document.createElement("tbody");
		table.appendChild(tbody);
		
		////
		
		var i=0;
		while(data[i]){
			tr=document.createElement("tr");
			tbody.appendChild(tr);
			////
			var td=document.createElement("td");
			td.innerHTML=data[i].fields.Promo_Code;
			tr.appendChild(td);
			
			td=document.createElement("td");
			td.innerHTML=data[i].fields.First_Name;
			tr.appendChild(td);
			
			td=document.createElement("td");
			td.innerHTML=data[i].fields.Surname;
			tr.appendChild(td);
			
			td=document.createElement("td");
			td.innerHTML=data[i].fields.Order_Date;
			tr.appendChild(td);
			i++;
		}
		
		
		
		
	}
		

	

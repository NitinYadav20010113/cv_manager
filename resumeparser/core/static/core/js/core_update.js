function onFormSubmit(event) {
    event.preventDefault();

    var category=document.getElementById("category").value;
    var candidate=document.getElementById("candidate").value;
    var candidate_id=document.getElementById("can_id").value;
    var Data=document.getElementById("file22").files;
    document.getElementById("status").innerHTML="" 
    // document.getElementById("file22").value="";
    // console.log(Data)

    
    // console.log(resume)    
    if (Data.length!=0){
        var c = parseInt(100/Data.length)  
        
        for (var i=0; i<Data.length;i++){          
            let data = Data[i];  // file from input            
            let req = new XMLHttpRequest();
            let formData = new FormData(); 
            // formData.append("name",45) 
            key=String(category)+","+String(candidate)+","+String(candidate_id)          
            formData.append(key, data);  
            
                                                
            req.open("POST", 'http://127.0.0.1:8000/update/ud/',false);
            // req.open("POST", 'http://172.16.3.154:9001/update/ud/',false);
        	// req.open("POST", "http://103.210.112.132:9001/update/ud/", false);
            req.send(formData);
            console.log(c)
            document.getElementById("progress_div").style["display"]="block";        
            document.getElementById("progress_bar").style["width"]=""+String(c)+"%";
            document.getElementById("progress_bar").innerHTML=""+String(parseInt(c))+"%";
            if (i<(Data.length-2)) {
                c+=100/Data.length;
            } else {
                c=100
            }
            
            
        }
    }else {
    if (category=="Basic Details"|| category=="Address" || category=="Designation" || category=="Projects"){
        document.getElementById("status").innerHTML="" 
        document.getElementById("status").innerHTML="Function Not ACTIVE"  
    
    }else {
        if (candidate=="By Candidate" && candidate_id.length==0){
            document.getElementById("status").innerHTML="" 
            document.getElementById("status").innerHTML="Please Enter Candidate ID"   
        }else {
            var kk=isNaN(candidate_id) 
            
            if ((candidate=="By Candidate") && (candidate_id.length!=0) && (kk==true)){
                
                document.getElementById("status").innerHTML="" 
                document.getElementById("status").innerHTML="Candidate ID Must Be Digits" 
            }else {
                document.getElementById("status").innerHTML="" 
                
                document.getElementById("progress_div").style["display"]="block";        
                document.getElementById("progress_bar").style["width"]="0.5%";
                        
                var formData = new FormData();
                key=String(category)+","+String(candidate)+","+String(candidate_id) 
                formData.append(key, "");
                

                var xhr = new XMLHttpRequest();
                xhr.open("POST", "http://127.0.0.1:8000/update/ud/");
                // xhr.open("POST", "http://172.16.3.154:9001/update/ud/");
            	// xhr.open("POST", "http://103.210.112.132:9001/update/ud/");
                xhr.send(formData);     
                               
                
                
                
                // var data = JSON.stringify({"category": String(category), "type": String(candidate), "candidate_id":String(candidate_id), "files":Data});       
                // req.send(data); 
                // restxt = req.response
                c=10
                while (c <100) {
                    
                    let req2 = new XMLHttpRequest();                 
                    // req2.open("GET", 'http://172.16.3.154:9001/update/udp/', false);
                    req2.open("GET", 'http://127.0.0.1:8000/update/udp/', false);
                	// req2.open("GET", "http://103.210.112.132:9001/update/udp/", false);
                    req2.send(null)
                    resptxt2=req2.response               
                    c=parseInt(resptxt2)  
                    // console.log(c)
                    document.getElementById("progress_div").style["display"]="block";        
                    document.getElementById("progress_bar").style["width"]=""+String(c)+"%";
                    document.getElementById("progress_bar").innerHTML=""+String(parseInt(c))+"%";             
                    
                }
            }
        }   
    }
}
};



function Checkcategory(val){
    document.getElementById("progress_div").style["display"]="None";        
    document.getElementById("progress_bar").style["width"]="0.1%";
    document.getElementById("progress_bar").innerHTML="0.1%";
    var element = document.getElementById("file22"); 
    var element2= document.getElementById("candidate");
    var element3= document.getElementById("can_id");
    
    if(val=='Education') {  
        element3.disabled=true;
        element2.disabled=true;      
        element.disabled= false;     
        element3.value=""      
        console.log(val)          
    
    } else if (val=='Projects') {  
            element3.disabled=true;
            element2.disabled=true;      
            element.disabled= false;     
            element3.value=""      
            console.log(val)          
    
    }else  {
        element.value="";
        element.disabled= true;
        console.log(element2.value)
        document.getElementById("candidate").disabled=false;
        
    }
   }
function Checktype(val){
var element=document.getElementById('can_id');
if(val=='By Candidate') {
    element.disabled= false;           
} else  
    element.disabled= true;
    element.value=""
}


// testing

function myFunction() {
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}

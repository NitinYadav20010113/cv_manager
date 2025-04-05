function onFormSubmit(event) {
    event.preventDefault();
    var Data=document.getElementById("file").value;

    document.getElementById("loading").innerHTML="Loading . . .    Please Wait";

    document.getElementById("com_website").innerHTML="";  
    document.getElementById("com_website_value").innerHTML="";
    
    document.getElementById("com_f_name").innerHTML="";  
    document.getElementById("com_f_name_value").innerHTML=""; 
    
    document.getElementById("Address").innerHTML="";  
    document.getElementById("Address_value").innerHTML=""; 
    
    
    document.getElementById("Phone").innerHTML="";  
    document.getElementById("Phone_value").innerHTML=""; 
    
    
    document.getElementById("CEO").innerHTML="";  
    document.getElementById("CEO_value").innerHTML=""; 
   
    document.getElementById("Founder").innerHTML="";  
    document.getElementById("Founder_value").innerHTML=""; 
   
    document.getElementById("Founded").innerHTML="";  
    document.getElementById("Founded_value").innerHTML="" 
  
    document.getElementById("Owner").innerHTML="";  
    document.getElementById("Owner_value").innerHTML=""; 
    
    document.getElementById("Headquarters").innerHTML="";  
    document.getElementById("Headquarters_value").innerHTML=""; 
 
    document.getElementById("Revenue").innerHTML="";  
    document.getElementById("Revenue_value").innerHTML=""; 
    

    console.log(Data);
    let req = new XMLHttpRequest();                 
    req.open("POST", 'http://127.0.0.1:8000/companysearch/com/',false);
    // req.send(formData);     
    var data = JSON.stringify({"text": String(Data)});
    req.send(data); 
    console.log(req.response)
    restxt = JSON.parse(req.response)
    var data_key=Object.keys(restxt)
    document.getElementById("loading").innerHTML="";
    if (data_key.includes("com_website")){
        document.getElementById("com_website").innerHTML="Company website";  
        document.getElementById("com_website_value").innerHTML=String(restxt['com_website']);
    }
    if (data_key.includes("com_f_name")){
    document.getElementById("com_f_name").innerHTML="Company name";  
    document.getElementById("com_f_name_value").innerHTML=String(restxt['com_f_name']); 
    }
    if (data_key.includes("Address")){
    document.getElementById("Address").innerHTML="Company Address";  
    document.getElementById("Address_value").innerHTML=String(restxt['Address']); 
    }
    if (data_key.includes("Phone")){
    document.getElementById("Phone").innerHTML="Company Contact";  
    document.getElementById("Phone_value").innerHTML=String(restxt['Phone']); 
    }
    if (data_key.includes("CEO")){
    document.getElementById("CEO").innerHTML="Present CEO";  
    document.getElementById("CEO_value").innerHTML=String(restxt['CEO']); 
    }
    if (data_key.includes("Founder")){
    document.getElementById("Founder").innerHTML="Company Founder";  
    document.getElementById("Founder_value").innerHTML=String(restxt['Founder']); 
    }
    if (data_key.includes("Founded")){
    document.getElementById("Founded").innerHTML="Company Founded at";  
    document.getElementById("Founded_value").innerHTML=String(restxt['Founded']); 
    }
    if (data_key.includes("Owner")){
    document.getElementById("Owner").innerHTML="Company Owner";  
    document.getElementById("Owner_value").innerHTML=String(restxt['Owner']); 
    }
    if (data_key.includes("Headquarters")){
    document.getElementById("Headquarters").innerHTML="Company Headquarters";  
    document.getElementById("Headquarters_value").innerHTML=String(restxt['Headquarters']); 
    }
    if (data_key.includes("Revenue")){
    document.getElementById("Revenue").innerHTML="Company Revenue";  
    document.getElementById("Revenue_value").innerHTML=String(restxt['Revenue']); 
    }
}; 
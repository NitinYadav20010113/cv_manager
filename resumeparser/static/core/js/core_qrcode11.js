function onFormSubmit(event) {
    event.preventDefault();
    var Data=document.getElementById("file1").files;
    document.getElementById("recent_heading").innerHTML = "Recent Uploads"
    document.getElementById("progress_div").style["display"]="block";        
    document.getElementById("progress_bar").style["width"]="0.5%";
    document.getElementById("status").innerHTML="Processing... Please Wait"   

    var c = parseInt(100/Data.length)
    for (var i=0; i<Data.length;i++){  
        var initial_time = new Date();     
        let data = Data[i];  // file from input
        let req = new XMLHttpRequest();
        let formData = new FormData();
        formData.append("file", data);                                
        req.open("POST", 'http://172.16.3.154:9001/qrcode/qr/',false);
        var f_name = data.name        
        f_name = f_name.replace(/  +/g, ' ')
        f_name = f_name.split(" ").join("_")
        console.log(f_name)
        data.name.replace(/ /g,"_")
        req.send(formData);
        if (i<(Data.length-2)) {
            c+=100/Data.length;
        } else {
            c=100
        }
        // for dropdown (recent uploads)
        document.getElementById("progress_div").style["display"]="block";        
        document.getElementById("progress_bar").style["width"]=""+String(c)+"%";
        document.getElementById("progress_bar").innerHTML=""+String(parseInt(c))+"%";      
    	document.getElementById("recent_upload").innerHTML+= "<li><a id="+"list_item"+" href="+"http://172.16.3.154/qr_codes/"+f_name+" target="+"_blank"+">Download  "+f_name+"</a></li>" 

    }   
    document.getElementById("status").innerHTML="Completed"   
    
}; 

function onFormSubmit2(event) {
    event.preventDefault();
    var Data=document.getElementById("file11").files;
    document.getElementById("recent_heading").innerHTML = "Recent Uploads"
    document.getElementById("progress_div2").style["display"]="block";        
    document.getElementById("progress_bar2").style["width"]="0.5%";
    document.getElementById("status2").innerHTML="Processing... Please Wait"   

    var c = parseInt(100/Data.length)
    for (var i=0; i<Data.length;i++){  
        var initial_time = new Date();     
        let data = Data[i];  // file from input
        let req = new XMLHttpRequest();
        let formData = new FormData();
        formData.append("file", data);                                
        req.open("POST", 'http://172.16.3.154:9001/qrcode/qr2/',false);
        var f_name = data.name        
        f_name = f_name.replace(/  +/g, ' ')
        f_name = f_name.split(" ").join("_")
        console.log(f_name)
        data.name.replace(/ /g,"_")
        req.send(formData);
        if (i<(Data.length-2)) {
            c+=100/Data.length;
        } else {
            c=100
        }
        // for dropdown (recent uploads)
        document.getElementById("progress_div2").style["display"]="block";        
        document.getElementById("progress_bar2").style["width"]=""+String(c)+"%";
        document.getElementById("progress_bar2").innerHTML=""+String(parseInt(c))+"%";      
    	document.getElementById("recent_upload").innerHTML+= "<li><a id="+"list_item"+" href="+"http://172.16.3.154/qr_codes/"+f_name+" target="+"_blank"+">Download  "+f_name+"</a></li>" 

    }   
    document.getElementById("status2").innerHTML="Completed"   
    
}; 

// for searching part
function onFormSubmit1(event) {
    event.preventDefault();
    var Data2=document.getElementById("file3").value;
    console.log(Data2)    
    if (Data2.length>0) {
        document.getElementById("download_qr").href="http://172.16.3.154/qr_codes/"+Data2+".pdf";
        document.getElementById("download_qr").innerHTML="Download "+Data2+".pdf";
    } else {
        document.getElementById("download_qr").innerHTML="Enter Text"
        document.getElementById('download_qr').innerHTML = "<span style='color: red;'>Enter Text Please</span>"; 
    }
    
    
}
function showdir(event){
    console.log('finally')
    
    document.getElementById("recent_dir").innerHTML='';
    document.getElementById("recent_dir").style['display']="block";
    event.preventDefault();
    console.log("im here");
    let req2 = new XMLHttpRequest();    
    req2.open("GET", "http://172.16.3.154:9001/qrcode/qr3/", false);
    req2.send(null);
    resptxt2=req2.response  ;
    resptxt2=resptxt2.split(',')   ;          
    c=resptxt2  ;
    // console.log(c);
    for (var i=0; i<c.length-1;i++){  
        document.getElementById("recent_dir").innerHTML+= "<li id="+"item_list"+"><input id="+String(c[i])+" type='button' onclick="+"openDialog(event)"+" value="+c[i]+" /></li>" 
    
    }
}
let foldername = "abcd";
function openDialog(event) {
    var loc = event.target.id;
    foldername=String(loc)
    console.log("foldername",foldername)
    document.getElementById('fileid').click();
    document.getElementById('submitfolder').style['display']="block";
}
function replacefile(event){
    const myJSON = JSON.stringify({foldername:String(foldername)}); 
    let req = new XMLHttpRequest();
    req.open("POST", 'http://172.16.3.154:9001/qrcode/qr5/', false);
    req.send(myJSON);

    console.log("foldername",foldername)
    Data = document.getElementById("fileid").files ; 
    data=Data[0];
    console.log(Data.length) 
    let req2 = new XMLHttpRequest();
    let formData = new FormData();
    formData.append("file", data);
    console.log(data)                             
    req2.open("POST", 'http://172.16.3.154:9001/qrcode/qr4/',false);   
    req2.send(formData);    
    resptxt2=req2.response;
    console.log(resptxt2)
}

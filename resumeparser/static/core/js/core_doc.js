function onFormSubmit(event) {
    event.preventDefault();
    var Data=document.getElementById("file").files;

    document.getElementById("progress_div").style["display"]="block";        
    document.getElementById("progress_bar").style["width"]="1%";
    // document.getElementById("progress_bar").innerHTML="1%";

    var c = parseInt(100/Data.length)
    var exp_time = [];
    var total_time = 0;  //in miliseconds
    for (var i=0; i<Data.length;i++){  
        var initial_time = new Date();         

        document.getElementById("progress_text").innerHTML="Upload Count: ";
        document.getElementById("file_name").innerHTML="Processing: ";

        document.getElementById("progress_text_value").innerHTML=parseInt(i+1)+"/"+parseInt(Data.length);
        document.getElementById("file_name_value").innerHTML=String(Data[i]['name'])
        
        let data = Data[i];  // file from input
        let req = new XMLHttpRequest();
        let formData = new FormData();
        formData.append("file", data);                                
        req.open("POST", 'http://172.16.3.154:9001/doc/home/',false);
        req.send(formData);
        if (i<(Data.length-2)) {
            c+=100/Data.length;
        } else {
            c=100
        }
        var final_time = new Date();
        var diff_time = (final_time-initial_time)/1000;
        exp_time.push(diff_time)
        total_time+=diff_time       

        var t_hour = ~~(total_time/3600);
        var t_r_hour =(total_time%3600);
        var t_min = ~~(t_r_hour/60);
        var t_sec = String(t_r_hour%60).split('.');

        document.getElementById("progress_div").style["display"]="block";        
        document.getElementById("progress_bar").style["width"]=""+String(c)+"%";
        document.getElementById("progress_bar").innerHTML=""+String(parseInt(c))+"%";
        
        document.getElementById("total_time").innerHTML=String("Total Time: ");
        document.getElementById("total_time_value").innerHTML=t_hour+":"+t_min+":"+t_sec[0];
        
        exp_seconds = (total_time/(i+1))*(Data.length-(i+1));
        
        var e_hour = ~~(exp_seconds/3600);
        var e_r_hour = exp_seconds%3600;
        var e_min = ~~(e_r_hour/60);
        var e_sec = String(e_r_hour%60).split('.');
        if (Data.length> 1) {
            
            document.getElementById("exp_time").innerHTML="Expected Time: ";
            document.getElementById("exp_time_value").innerHTML=String(e_hour+":"+e_min+":"+e_sec[0]);
        }  
    }
    document.getElementById("exp_time").innerHTML=String("");
    document.getElementById("exp_time_value").innerHTML="";
    if (Data.length>0) {
        document.getElementById("file_name").innerHTML="STATUS: ";
        document.getElementById("file_name_value").innerHTML="  All Files Processed  !!!";
    } else {
        document.getElementById("file_name").innerHTML="NO FILE CHOOSEN  !!!"
    }    
}; 
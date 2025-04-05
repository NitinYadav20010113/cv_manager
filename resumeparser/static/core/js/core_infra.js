var domain_name = window.location.protocol+'//'+window.location.host;
console.log(domain_name)
$('#dropdown_btn').click(function(){
    $('ul').toggleClass('active');
  });
function fileselect(event){
    var Data=document.getElementById("file").files;
    document.getElementById('filelist').innerHTML='';
    document.getElementById('filelist').innerHTML+="<p class='text-end mb-1 p-1 px-3'><i style='cursor:pointer;' onclick="+"document.getElementById('filelist').className=''"+" class='fa fa-times'></i></p>"; 
    document.getElementById('dropdown_btn').innerHTML='Files : '+Data.length;
    for (var i=0; i<Data.length;i++){ 
        document.getElementById('filelist').innerHTML+='<li class="mb-1 p-1">'+Data[i].name+'</li>'; 
    }
}
function onFormSubmit(event) {
    event.preventDefault();
    var Data=document.getElementById("file").files;  
    document.getElementById("progress_bar").style["width"]="0.5%";
    document.getElementById("count_text_value").innerHTML='-- / --'
    document.getElementById('alert_message').innerHTML='';
    var c = parseInt(100/Data.length)
    i=0
    var total_time = 0;  //in miliseconds
    function sendfile(){    
        let formData = new FormData();
        formData.append("file", Data[i]);
        var initial_time = new Date();
        return $.ajax({            
            url: domain_name+'/infra/final/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            global: false, 
            success:function(data){
                var final_time = new Date();
                var diff_time = (final_time-initial_time)/1000;
                total_time+=diff_time  
                exp_seconds = (total_time/(i+1))*(Data.length-(i+1));
                var e_hour = ~~(exp_seconds/3600);
                var e_r_hour = exp_seconds%3600;
                var e_min = ~~(e_r_hour/60);
                var e_sec = String(e_r_hour%60).split('.');
                document.getElementById("exp_time_value").innerHTML=String(e_hour+" hr: "+e_min+" min: "+e_sec[0]+" sec");
                document.getElementById("count_text_value").innerHTML=parseInt(i+1)+"/"+parseInt(Data.length);
                document.getElementById("progress_bar").style["width"]=""+String(c)+"%";
                document.getElementById("progress_bar").innerHTML=""+String(parseInt(c))+"%";
                
                if (i<=(Data.length-2)) {
                    c+=100/Data.length;
                } else {
                    c=100                    
                    document.getElementById("progress_bar").style["width"]=""+String(c)+"%";
                    document.getElementById("progress_bar").innerHTML=""+String(parseInt(c))+"%";
                    document.getElementById('alert_message').className='text-center text-white';
                    document.getElementById('alert_message').innerHTML='Completed !!';
                }
                if (i<=Data.length-2){
                    i+=1
                    sendfile()
                } 
                              
            }
        })
    }
    if (Data.length>1){
        sendfile()
    }else{
        document.getElementById('alert_message').className='text-center text-danger';
        document.getElementById('alert_message').innerHTML='First Select a File';
    }
}; 

// $(window).click(function(e) {
//     if(document.getElementById('filelist').className=='active'){
//         document.getElementById('filelist').className='';
//     }
    // if(e.target != document.getElementById('filelist')) {
    //     console.log('You clicked outside');
    //     document.getElementById('filelist').className='';
    // } else {
    //     console.log('You clicked inside');
    // }

//   });
// $(window).onclick = function(e) {
//     console.log('clicked')
    // if(e.target == document.getElementById('filelist')) {
    //     console.log('You clicked inside');
    // } else {
    //     console.log('You clicked outside');
    // }
//   }

// window.addEventListener('click', function(e){   
//     this.document.getElementById('filelist').className='';
//     // if (document.getElementById('filelist').contains(e.target)){
      
//     //     console.log('clicked in box')
//     // } else{
//     //   this.document.getElementById('filelist').className='';
//     // }
//   });
  
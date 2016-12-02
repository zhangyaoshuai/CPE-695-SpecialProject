$(document).ready(function() {
    response = [];
    $("#btn1").click(function(){
        $.get("/showUsers", function(data, status){
            console.log(status);
            console.log(data);
            response = data;
        });
     });

});
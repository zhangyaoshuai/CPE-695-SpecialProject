(function ($) {
    console.log("Scripts works!");
    var load= function(){
        console.log("load!");
        //$("#h2").css("color","red").slideUp(2000).slideDown(2000);
    };
    load();

    $("#btn1").click(function(){

        $.get("/users", function(data, status){
            console.log(status);
            console.log(data);
        });
     });
})(jQuery)
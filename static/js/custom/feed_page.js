$(document).ready(function(){
    <!--Used to display feeds on current page-->
	$("#feedbut button").click(function(e){
		$("#feedpage").load($(this).attr("value"));
        
	});
    $("#recommendations button").click(function(e){
		$("#feedpage").load($(this).attr("value"));
	});
    $("#feedbut feed").click(function(e){
		$("#feedpage").load($(this).attr("value"));
	});
});
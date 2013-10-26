$(document).ready(function(){
    <!--Used to display feeds on current page-->
	$("#feedbut button").click(function(e){
		$("#feed-page").load($(this).attr("value"));
        $("#feed-container").addClass("well");
	});
    $("#recommendations button").click(function(e){
		$("#feed-page").load($(this).attr("value"));
	});
    $("#feedbut feed").click(function(e){
		$("#feed-page").load($(this).attr("value"));
	});
});


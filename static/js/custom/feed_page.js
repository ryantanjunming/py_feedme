var curReadTile = 0;
var curURL;

$(document).ready(function(){
	
	// <!--Used to display feeds on current page-->
	// $("#feedbut button").click(function(e){
	// 	$("#feed-page").load($(this).attr("value"));
 //        $("#feed-container").addClass("well");

	// });

	$( "#feed_content" ).accordion({
    	heightStyle: "content"
    });

	$("#feedbut button").click(function(e){
		curReadTile = 0;
		curURL = $(this).attr("value");
		$.ajax({
     		url: "/feeds/showfeed/",
            type: 'POST',
            dataType: 'json',
            data: {
            	tile : curReadTile,
           		url : curURL,
            	csrfmiddlewaretoken : document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function(data) {
            	curReadTile++;
            	$("#feed-page").empty();
            	//Title Making Portion
            	$("#feed-page").append('<div id="feed_header" class="feed_header"><a href='+data.link+' target="_blank"><h2>'+data.title_title+'</h2></a>'+
            							'<a href="'+data.link+'" target="_blank"><img src='+data.title_icon+'></a></div><br>'+data.last_updated);
            	$("#feed-page").append('<div id="feed_content">');
            	
            	var entries = data.request_entries;
            	$.each(entries, function(i, item){
            		
            		// $("#feed-page").append('<div><h3>Section 1</h3></div>');
            	})

            	$("#feed-page").append("</div>");
            	
            	$("#feed-container").addClass("well");
            }
		});
	});

	//USES FEEDS/SHOWFEED ALSO
 	//    $("#recommendations button").click(function(e){
	// 	$("#feed-page").load($(this).attr("value"));
	// 	$("#feed-container").addClass("well");
	// });

 	//    $("#feedbut feed").click(function(e){
	// 	$("#feed-page").load($(this).attr("value"));
	// 	$("#feed-container").addClass("well");
	// });
});


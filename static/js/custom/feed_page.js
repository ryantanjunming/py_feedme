var curReadTile = 0;
var curURL;

$(document).ready(function(){
	
	// <!--Used to display feeds on current page-->
	// $("#feedbut button").click(function(e){
	// 	$("#feed-page").load($(this).attr("value"));
 	//        $("#feed-container").addClass("well");
	// });

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

            	var image_tag = "";
            	if(data.title_icon.toUpperCase() !== "IMG".toUpperCase()){
            		var image_tag = '<img src='+data.title_icon+'>';
            	}
            	//Title Making Portion
            	$("#feed-page").append('<div id="feed_header" class="feed_header"><a href='+data.title_link+' target="_blank"><h2>'+data.title_title+'</h2></a>'+
            							'<a href="'+data.link+'" target="_blank">'+image_tag+'</a><br>'+data.last_updated+'</div>');
            	$("#feed-page").append('<div id="feed_content">');
            	
	            	var entries = data.request_entries;
	            	$.each(entries, function(i, item){
	            		
	            		$("#feed_content").append('<h5 class="tab">'+entries[i].title+'</h5>'+
	            			'<div class="content"><h3><a href="' + entries[i].link + '" target="_blank">' + entries[i].title + '</a></h3><p>'+
	            			entries[i].author + ', published on ' + entries[i].published + '</p><p>' + entries[i].summary + '</p>'+
		            		"<p><button href=\"#\" onclick=\"window.open('http://www.facebook.com/sharer/sharer.php?s=100&p[url]="+ entries[i].link +"&p[images][0]=&p[title]="+ entries[i].title +"&p[summary]="+ entries[i].title +"'"+
	                      	", 'facebook-share-dialog', 'width=626,height=436'); return false;\" style=\"color:white;background-color:#3B5998\">"+
	                       	"Share on Facebook</button>&nbsp;&nbsp;"+
			              	"<a href=\"https://twitter.com/share\" class=\"twitter-share-button\" data-lang=\"en\" data-url=\""+ entries[i].link +"\" data-text=\""+ entries[i].title +"\">Tweet</a>"+
			                "<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=\"https://platform.twitter.com/widgets.js\";fjs.parentNode.insertBefore(js,fjs);}}(document,\"script\",\"twitter-wjs\");</script>"+
			                "</p></div>");
			                
	            	});


            	$("#feed-page").append("</div>");
            	$("#feed-container").addClass("well");
            	
            	$('#feed_content div').hide();
            	$('#feed_content h5').click(function(e) {
				    $(e.target).next('div').siblings('div').slideUp('slow');
				    $(e.target).next('div').slideToggle('slow');
				});

            	//$("#feed_content" ).accordion({
			    // 	heightStyle: "content"
			    // });
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


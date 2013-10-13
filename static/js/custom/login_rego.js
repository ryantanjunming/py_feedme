$().ready( function(){
	
	//disable form submission on enter
	$('form').bind("keyup", function(e) {
		  var code = e.keyCode || e.which; 
		  if (code  == 13) {               
		    e.preventDefault();
		    return false;
		  }
		});
	$('form').submit(false);
	

	$('#loginSubmit').click(function(event) {	
		var username = $('#formSigninUsername').val();
		var password = $('#formSigninPassword').val();
		if(username && password){
	     	$.ajax({
	     		url: "/accounts/login/",
	            type: 'POST',
	            dataType: 'json',
	            data: {
	            	formType : 'login',
	            	username : username,
	            	password : password,
	            	csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value
	            },
	            success: function(data) {
	        		$('#formSigninAlert').show().html('<div class="alert alert-success">'+data.message+'</div>');
	        		setTimeout(function() {
	        			window.location.href = data.redirect;
	        		}, 500);
	            },error : function(xhr,errmsg,err) {
	            	$('#formSigninAlert').show().html(
	            		'<div class="alert alert-danger">'+xhr.status+": "+xhr.responseText+'</div>');
				}
	     	});
	 		return false;
	 	}else{
	 		$('#formSigninAlert').show().html('<div class="alert alert-danger">Please Login with your <strong>Username</strong> & <strong>Password</strong></div>');
	 	}
    });
	
	// validate signup form on keyup and submit
	$("#regoForm").validate({
		rules: {
			formRegoFirstName: "required",
			formRegoLastName: "required",
			formRegoUsername: {
				required: true,
				minlength: 2
			},
			formRegoPassword: {
				required: true,
				minlength: 6
			},
			formRegoConfirmPassword: {
				required: true,
				minlength: 6,
				equalTo: "#formRegoPassword"
			},
			formRegoEmail: {
				required: true,
				email: true
			},
		},
		messages: {
			formRegoFirstName: "Please enter your First Name",
			formRegoLastName: "Please enter your Last Name",
			formRegoUsername: {
				required: "Enter a username",
				minlength: "Username must consist of at least 2 characters"
			},
			formRegoPassword: {
				required: "Provide a password",
				minlength: "Password must be at least 6 characters long"
			},
			formRegoConfirmPassword: {
				required: "Please provide a password",
				minlength: "Your password must be at least 6 characters long",
				equalTo: "Please enter the same password as above"
			},
			formRegoEmail: {
				required: "Please enter your email address",
				email: "Please enter a valid email address"
			},
		},
		submitHandler: function(form) {
			var register = new Object();
			register.username = $('#formRegoUsername').val();
			register.password = $('#formRegoPassword').val();
			register.confirmPassword = $('#formRegoRepeatPassword').val();
			register.firstName = $('#formRegoFirstName').val();
			register.lastName = $('#formRegoLastName').val();
			register.email = $('#formRegoEmail').val();
			
			var registerDataString = "ajax=addUser&data=" + JSON.stringify(register);			
			$.ajax({
	     		url: "controller",
	            type: 'POST',
	            dataType: 'json',
	            data: registerDataString,
	            success: function(data) {
	            	if(data.success){
	            		$('#formRegoAlert').show().html('<div class="alert alert-success">'+data.message+'</div>');
	            		setTimeout(function() {
	            			window.location.href = data.redirect;
	            		}, 2000);
	            	}else{
	            		$('#formRegoAlert').show().html('<div class="alert alert-danger">'+data.message+'</div>');
	            	}
	            }
	     	});
		}
	});
	
	
	
});
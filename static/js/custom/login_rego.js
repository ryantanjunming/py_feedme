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
	            	if(data.success == true){
		        		$('#formSigninAlert').show().html('<div class="alert alert-success">'+data.message+'</div>');
		        		window.location.href = data.redirect;
		        	}else{
		        		$('#formSigninAlert').show().html('<div class="alert alert-danger">'+data.message+'</div>');
		        		$('#formSigninPassword').val('');
		        	}
	            },error : function(xhr,errmsg,err) {
	            	$('#formSigninAlert').show().html('<div class="alert alert-danger">'+xhr.status+": "+xhr.responseText+'</div>');
	            	$('#formSigninPassword').val('');
				}
	     	});
	 		return false;
	 	}else{
	 		$('#formSigninAlert').show().html('<div class="alert alert-danger">Please Login with your <strong>Username</strong> & <strong>Password</strong></div>');
	 	}
    });

    $('#forgetPass').click(function(event) {	
		window.open("http://localhost:8000/accounts/resetPasswordUser/","_blank");
    });

	$('#formRegoUsername').focusout( function() {
		var userNameCheck = $('#formRegoUsername').val();
		$.ajax({
			url: "/accounts/usernameValidation/",
            type: 'POST',
            dataType: 'json',
            data: {
            	'username' : userNameCheck,
            	csrfmiddlewaretoken : document.getElementsByName('csrfmiddlewaretoken')[0].value
            },
            success: function(data) {
            	if(data.result == true){
            		$('#formRegoUsernameAlert').show().html('<div class="alert alert-danger">'+data.message+'</div>');
            	}
            }
		});
	});

	$('#formRegoUsername').focus( function() {
		$('#formRegoUsernameAlert').hide().html('');
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

			var password = $('#formRegoPassword').val();
			var confirmPassword = $('#formRegoConfirmPassword').val();
			
			if(password === confirmPassword){
				$.ajax({
		     		url: "/accounts/register/",
		            type: 'POST',
		            dataType: 'json',
		            data: {
		            	formType : 'register',
		            	csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
		            	'username' : $('#formRegoUsername').val(),
		            	'password' : password,
		            	'first_name' : $('#formRegoFirstName').val(),
		            	'last_name' : $('#formRegoLastName').val(),
		            	'email' : $('#formRegoEmail').val()
		            },
		            success: function(data) {
		            	if(data.success){
		            		if(data.success == true){
			        			$('#formRegoAlert').show().html('<div class="alert alert-success">'+data.message+'</div>');
					        	setTimeout(function() {window.location.href = data.redirect;}, 100);
					        }else{
				        		$('#formRegoAlert').show().html('<div class="alert alert-danger">'+data.message+'</div>');
				        		$('#formRegoPassword').val('');
	            				$('#formRegoConfirmPassword').val('');
					        }
		            	}
		            },error : function(xhr,errmsg,err) {
	            		$('#formRegoAlert').show().html('<div class="alert alert-danger">'+xhr.status+": "+xhr.responseText+'</div>');
	            		$('#formRegoPassword').val('');
	            		$('#formRegoConfirmPassword').val('');
		            }
		     	});
		    }
		}
	});	
});

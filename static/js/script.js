$(document).ready(function(){
    $("a#login").on("click", function(){
        $.post("login.html", function(data){
			$("#modalLogin").html(data).fadeIn();
		});
    });
});
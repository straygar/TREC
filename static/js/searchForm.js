$(document).ready(function() {
    $.ajax({
			type: "GET",
			url: "{% url 'getOrgsAjax' %}"},
			dataType: "json",
			success: function(xml) {

			},
			error: function() {
			 // Cannot do anything, auto-complete won't be offered
			}
		});
    new jQueryCollapse($("#form"), {
      open: function() {
        this.slideDown(150);
      },
      close: function() {
        // Clear all inputs when closing this
        $.each($(this).find(":input"), function() {
            $(this).val("");
        });
        this.slideUp(150);
      }
    });
});


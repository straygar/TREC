var refetch = true;

$(document).ready(function() {
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
    $("#org_input").autocomplete({source:[]});
    $("#org_input").keyup(changeFunc);
});

function changeFunc() {
    if (refetch) {
        refetch = false;
        $.ajax({
            type: "GET",
            url: "/main/getOrgsJson?organization=" + $("#org_input").val(),
            dataType: "json",
            success: function(json) {
                $( "#org_input" ).autocomplete("option", "source", json);
               },
            error: function() {
             // Cannot do anything, auto-complete won't be offered
            }
        });
        window.setTimeout(function() {
            refetch = true;
        }, 800);
    }

}


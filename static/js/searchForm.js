$(document).ready(function() {
    new jQueryCollapse($("#form"), {
      open: function() {
        this.slideDown(150);
        this.prev().find(".glyphicon-plus").removeClass("glyphicon-plus").addClass("glyphicon-minus");
      },
      close: function() {
        // Clear all inputs when closing this
        $.each($(this).find(":input"), function() {
            $(this).val("");
        });
        this.slideUp(150);
        this.prev().find(".glyphicon-minus").removeClass("glyphicon-minus").addClass("glyphicon-plus");
      }
    });
    new jQueryCollapse($("#dateChooser"), {
     accordion: true,
     open: function() {
        this.slideDown(150);
        this.prev().find(".glyphicon-plus").removeClass("glyphicon-plus").addClass("glyphicon-minus");
      },
      close: function() {
        // Clear all inputs when closing this
        $.each($(this).find(":input"), function() {
            $(this).val("");
        });
        this.slideUp(150);
        this.prev().find(".glyphicon-minus").removeClass("glyphicon-minus").addClass("glyphicon-plus");
      }
    });
    applyAll(["#org_input","#usrname_input", "#usrdisplay_input", "#runname_input"]);
    $("#datepicker1").datepicker();
    $("#datepickerrange1").datepicker();
    $("#datepickerrange2").datepicker();
});

function applyAll(controlArray) {
    $.each(controlArray, function(index, item) {
        $(item).autocomplete({source:[]});
        $(item).keyup(changeFunc);
    });
}

function changeFunc() {
    control = $(this);
    if (control.attr("refetch")) {
        control.attr("refetch", false);
        $.ajax({
            type: "GET",
            url: "/main/" + control.attr("jsonpath") + control.val(),
            dataType: "json",
            success: function(json) {
                control.autocomplete("option", "source", json);
               },
            error: function() {
             // Cannot do anything, auto-complete won't be offered
            }
        });
        window.setTimeout(function() {
            control.attr("refetch", true);
        }, 800);
    }

}
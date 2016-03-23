$(document).ready(function() {
    createCollapsible($("#form"), false);
    createCollapsible($("#dateChooser"), true);
    createCollapsible($("#p10form"), true);
    createCollapsible($("#p20form"), true);
    createCollapsible($("#mapform"), true);
    applyAll(["#org_input","#usrname_input", "#usrdisplay_input", "#runname_input"]);
    setDatePicker(["#datepicker1", "#datepickerrange1", "#datepickerrange2"]);
    $("#searchbtn").click(function(event) {
        event.preventDefault();
        var queryString = "?";
        var tempValue = "";
        var currentElement;
        var tempPrefix = "";
        try {
            $.each($("#form").find("select"), function() {
                tempValue = encodeURI($(this).val());
                if ($.trim(tempValue).length > 0) {
                    queryString += tempValue + "&";
                }
            });
            $.each($("#form").find("input"), function() {
                currentElement = $(this);
                tempValue = encodeURI(currentElement.val());
                if ($.trim(tempValue).length > 0) {
                    // Check if it is a single value
                    tempPrefix = currentElement.attr("prepend");
                    if (currentElement.attr("extra") == "unique") {
                        queryString += tempPrefix + "min=" + tempValue + "&" + tempPrefix + "max=" + tempValue;
                    } else {
                        queryString += tempPrefix + "=" + tempValue;
                    }
                    queryString += "&";
                }
            });
            if ($.trim(queryString).length > 1) {
                queryString += $("#pageSize").val();
                window.location.href=$(this).attr("href") + queryString;
            } else {
                $("#noCrit").slideDown(150);
            }
        } catch (e) {
            $("#noCrit").slideDown(150);
        }
    });
});

function setDatePicker(elements) {
    $.each(elements, function(index, item) {
        $(item).datepicker();
        $(item).datepicker("option", "dateFormat", "dd-mm-yy");
    });
}

function createCollapsible(element, accordion) {
    new jQueryCollapse(element, {
     accordion: accordion,
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
}

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
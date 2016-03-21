$(document).ready(function() {
    $("#graphbtn").click(function(event) {
        event.preventDefault();
        var value = $("#taskSelect").val();
        if ((value === null) || (value.length == 0)) {
            $("#noCrit").slideDown(150);
        } else {
            var finalUrl = window.location.href.split("?")[0];
            finalUrl += "?" + value + "#chart";
            window.location.href = finalUrl;
        }
    });
});

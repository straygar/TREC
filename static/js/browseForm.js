$(document).ready(function() {
    var visible = false;
    $("#sortForm").hide();
    $("#toggle").click(function(event) {
        event.preventDefault();
        if (visible) {
            $(this).find(".glyphicon-minus").removeClass("glyphicon-minus").addClass("glyphicon-plus");
            $("#id_sortOn").val(""); // Clear option
            $("#sortForm").slideUp(150);
        } else {
            $(this).find(".glyphicon-plus").removeClass("glyphicon-plus").addClass("glyphicon-minus");
            $("#sortForm").slideDown(150);
        }
        visible = !visible;
    });
});
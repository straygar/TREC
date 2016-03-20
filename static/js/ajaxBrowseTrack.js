$(document).ready(function() {
    $("#id_track").change(function() {
        $("#tableInfo").hide();
        $("#tableInfo > tbody").empty();
        $.ajax({
            type: "GET",
            url: "/main/getTrackInfoJson/?track=" + $(this).val(),
            dataType: "json",
            success: function(json) {
            // Cannot use a dictionary since the order of the values could change and that could mislead the user
                $.each(json, function(key, value) {
                        var node = $("<tr>");
                        var title = value[0];
                        var item = value[1];
                        node = node.append($("<td>").text(value[0]));
                        if (title != "URL") {
                            node = node.append($("<td>").text(value[1]));
                        } else{
                            node = node.append($("<td>").append($("<a>").attr("href",value[1]).text(value[1])))
                        }
                        $("#tableInfo").find("tbody").append(node);
                    });
                $("#tableInfo").fadeIn(150);
            },
            error: function() {
             // Cannot do anything, auto-complete won't be offered
            }
        });

    });
});
$(document).ready(function() {
    $.each($("[track_id]"), function(index, item) {
        $(item).click(function(event) {
            event.preventDefault();
            var item = $(this).attr("track_id");
            if (item !== undefined) {
                $.ajax({
                    type: "GET",
                    url: "/main/getTasksJson/?track=" + item,
                    dataType: "json",
                    success: function(json) {
                        $("#tableInfo tbody").empty();
                        $.each(json, function(key, value) {
                                var node = $("<tr>");
                                var title = value[0];
                                var desc = value[1];
                                var url = value[2];
                                node = node.append($("<td>").text(value[0]));
                                node = node.append($("<td>").text(value[1]));
                                node = node.append($("<td>").append($("<a>").attr("href",value[2]).text(value[2])))
                                $("#tableInfo").find("tbody").append(node);
                            });
                        $("#popup").bPopup({
                            speed: 650,
                            transition: 'slideDown',
                            transitionClose: 'slideUp',
                        });
                    },
                    error: function() {
                     // Cannot do anything, auto-complete won't be offered
                    }
                });
            }
        })
    });
});
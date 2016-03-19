$(document).ready(function() {
      new jQueryCollapse($("#form"), {
          open: function() {
            this.slideDown(150);
			this.prev().find(".glyphicon-plus").removeClass("glyphicon-plus").addClass("glyphicon-minus");
          },
          close: function() {
            this.slideUp(150);
			this.prev().find(".glyphicon-minus").removeClass("glyphicon-minus").addClass("glyphicon-plus");
          }
        });
});
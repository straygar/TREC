$(document).ready(function() {
      new jQueryCollapse($("#form"), {
          open: function() {
            this.slideDown(150);
          },
          close: function() {
            this.slideUp(150);
          }
        });
});


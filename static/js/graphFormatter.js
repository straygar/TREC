function formatDate(value) {
    return $.format.date(value,"dd-MMM-yyyy HH:mm");
}
function formatter() { return formatDate(this.value); }

function tooltipFormatter() {
 return '<b>'+ this.y +'</b><br/>'+
                    'at '+ formatDate(this.x);
}
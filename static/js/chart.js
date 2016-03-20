
$(document).ready(function() {
	google.charts.load('current', {packages: ['corechart']});

        $.get('/returnResults',function(data){
			runs=JSON.parse(data);

			var dataTable= new google.visualization.DataTable();
			dataTable.addColumn('string','Name');
    	    dataTable.addColumn('number','MAP');
    	    dataTable.addColumn('number','P10');
    	    dataTable.addColumn('number','P20');
			$.each(data, function(val){
                fields = data[val]["fields"];
                dataTable.addRow([fields["name"],fields["map"],fields["p10"],fields["p20"]]);
            });
			var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    		chart.draw(data, options);

        });
	});


    //// Load the Visualization API and the corechart package.
    //  google.charts.load('current', {'packages':['corechart']});
    //
    //  // Set a callback to run when the Google Visualization API is loaded.
    //  google.charts.setOnLoadCallback(drawChart);
    //  // Callback that creates and populates a data table,
    //  // instantiates the pie chart, passes in the data and
    //  // draws it.
    //  function drawChart() {
    //      var runs = "{{runs|safe}}";
    //    // Create the data table.
    //    var data = new google.visualization.DataTable();
    //    data.addColumn('string', 'Run');
    //    data.addColumn('number', 'p10');
    //      data.addColumn('number','p20');
    //    data.addRows([
    //      ['Run 1', 4,3],
    //      ['Run 2', 1,5],
    //      ['Run 3', 1,4],
    //      ['Run 4', 1,1],
    //      ['Run 5', 2,3]
    //    ]);
    //
    //
    //    // Set chart options
    //    var options = {'title':'Last 5 runs',
    //                   'width':400,
    //                   'height':300};
    //
    //    // Instantiate and draw our chart, passing in some options.
    //    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    //    chart.draw(data, options);
    //  }

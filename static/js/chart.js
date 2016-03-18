google.charts.load('current', {packages: ['corechart', 'bar']});
google.charts.setOnLoadCallback(drawBasic);

function drawBasic() {

      var data = new google.visualization.DataTable();
      data.addColumn('number', 'run');
      data.addColumn('number', 'p10');
      data.addColumn('number','p20');


      data.addRows([
        [{v: [8, 0, 0], f: 'run1'}, p10_list[0],p20_list[0],],
        [{v: [9, 0, 0], f: 'run2'}, p10_list[1],p20_list[1],],
        [{v: [10, 0, 0], f:'run3'}, p10_list[2],p20_list[2],],
        [{v: [11, 0, 0], f: 'run4'}, p10_list[3],p20_list[3],],
        [{v: [12, 0, 0], f: 'run5'}, p10_list[4],p20_list[4],]
      ]);

      var options = {
        title: 'Last 5 runs',
        hAxis: {
          title: 'Runs',
          viewWindow: {
            min: [7, 30, 0],
            max: [17, 30, 0]
          }
        },
        vAxis: {
          title: 'p10 and p20'
        }
      };

      var chart = new google.visualization.ColumnChart(
        document.getElementById('chart_div'));

      chart.draw(data, options);
    }
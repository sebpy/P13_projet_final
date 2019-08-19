// Hidden message after 4 sec
window.setTimeout(function() {
    $(".save-conf").fadeTo(500, 0).slideUp(500, function(){
        $(this).remove();
    });
}, 4000);

am4core.useTheme(am4themes_animated);

// Create chart instance
var chart = am4core.create("chart_pw_total", am4charts.XYChart);

chart.paddingLeft = -8;
chart.paddingBottom = -10;
chart.dataSource.url = $SCRIPT_ROOT + '/_graph';
//chart.dataSource.incremental = true;
chart.dataSource.reloadFrequency = 60000;
chart.dataSource.incrementalParams = {
  incremental: "y",
  something: "else"
}
//chart.dataSource.updateCurrentData = true;

chart.dateFormatter.inputDateFormat = "MM-dd-yyyy";

// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.DateAxis());
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.renderer.minGridDistance = 60;
categoryAxis.renderer.labels.template.fontSize = 10;
categoryAxis.renderer.grid.template.location = 0;

var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.renderer.labels.template.fontSize = 10;

// Create series
var series = chart.series.push(new am4charts.LineSeries());
series.dataFields.valueY = "total_pw";
series.dataFields.dateX = "date";
series.tooltipText = "[b]{valueY}W[/]\n{dateX.formatDate('d MMM')}";
series.strokeWidth = 2;

chart.cursor = new am4charts.XYCursor();
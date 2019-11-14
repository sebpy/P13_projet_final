am4core.useTheme(am4themes_dark);
am4core.useTheme(am4themes_animated);

// Create chart instance
var chart = am4core.create("chart_pw_total", am4charts.XYChart);

chart.paddingLeft = 0;
chart.paddingBottom = -10;
chart.dataSource.url = $SCRIPT_ROOT + '/_graphpw';
//chart.dataSource.incremental = true;
chart.dataSource.reloadFrequency = 60000;
chart.dataSource.incrementalParams = {
  incremental: "y",
  something: "else"
}
chart.dataSource.updateCurrentData = true;

chart.dateFormatter.inputDateFormat = "MM-dd-yyyy";

// Create axes
var categoryAxis = chart.xAxes.push(new am4charts.DateAxis());
categoryAxis.renderer.grid.template.location = 0;
categoryAxis.renderer.minGridDistance = 1440;
categoryAxis.renderer.labels.template.fontSize = 10;
categoryAxis.renderer.grid.template.location = 0;
//categoryAxis.renderer.labels.template.fill = am4core.color("#fff");

var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
valueAxis.renderer.labels.template.fontSize = 10;
//valueAxis.renderer.labels.template.fill = am4core.color("#fff");
valueAxis.title.text = "[font-size:10px]Consommation (W)[/]";
valueAxis.title.color = "#fff"

// Create series
var series = chart.series.push(new am4charts.LineSeries());
series.dataFields.valueY = "total_pw";
series.dataFields.dateX = "date";
series.tooltipText = "[b]{valueY}W[/]\n{dateX.formatDate('d MMM')}";
series.strokeWidth = 2;

chart.cursor = new am4charts.XYCursor();
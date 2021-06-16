anychart.onDocumentReady(function () {

  // create data
  var data = {
    "nodes": [
      // hardwares
      {
        id: 'entrance_guard', height: '30', fill: ' #3498DB',
        description: 'Basecore: 12.50'
      },
      {
        id: 'surveillance', height: '30', fill: '#DC7633',
        description: 'Basecore: 21.10'
      },
      {
        id: 'alarm', height: '30', fill: '#AF7AC5',
        description: 'Basecore: 18.30'
      },
      {
        id: 'door_window_alarm_sensor0', height: '30', fill: '#cc1964',
        description: 'Basecore: 10.00.'
      },
      {
        id: 'door_window_alarm_sensor1', height: '30', fill: '#cc1964',
        description: 'Basecore: 10.00.'
      },
    ],

    "edges": [
      { from: 'surveillance', to: 'entrance_guard' },
      { from: 'surveillance', to: 'alarm' },
      { from: 'door_window_alarm_sensor0', to: 'door_window_alarm_sensor1' },
      { from: 'door_window_alarm_sensor0', to: 'alarm' },
      { from: 'door_window_alarm_sensor1', to: 'alarm' },
      { from: 'alarm', to: 'entrance_guard' },
      { from: 'alarm', to: 'surveillance' },
    ]
  }

  var chart = anychart.graph(data);

  chart.title("Security Systerm Connection");

  // configure nodes
  chart.nodes().labels().enabled(true);
  chart.nodes().labels().format("{%name}");
  chart.nodes().labels().fontSize(12);

  chart.nodes().normal().fill("white");
  chart.nodes().normal().stroke("white");
  chart.nodes().shape('circle');

  chart.nodes().hovered().fill("white");
  chart.nodes().hovered().stroke("white");
  chart.nodes().hovered().shape('circle');

  chart.edges().normal().stroke("#85C1E9", 1.4);
  chart.edges().hovered().stroke("#85C1E9", 1.4);

  chart.nodes().tooltip().useHtml(true);
  chart.nodes().tooltip().format(
    "<span style='font-weight:bold'>{%id}</span><br>{%description}"
  );
  chart.edges().tooltip().format("{%from} -> {%to}");
  chart.layout().type('force');

  // initiate drawing the chart
  chart.container('container').draw();
});
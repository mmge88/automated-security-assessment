anychart.onDocumentReady(function () {

  // create data
  var data = {
    "nodes": [
      // hardwares
      {
        id: 'entrance_guard', height: '30', fill: ' #3498DB',
        x: 300, y: 100,
        description: 'Basecore: 12.50'
      },
      {
        id: 'surveillance', height: '30', fill: '#DC7633',
        x: 600, y: 0,
        description: 'Basecore: 25.80'
      },
      {
        id: 'alarm', height: '30', fill: '#AF7AC5',
        x: 300, y: -100,
        description: 'Basecore: 21.10'
      },
      {
        id: 'door_window_alarm_sensor0', height: '30', fill: '#cc1964',
        x: 400, y: -300,
        description: 'Basecore: 10.00.'
      },
      {
        id: 'door_window_alarm_sensor1', height: '30', fill: '#cc1964',
        x: 200, y: -300,
        description: 'Basecore: 10.00.'
      },
      {
        id: 'asset_tag0', height: '30', fill: '#2ECC71',
        x: 100, y: -100,
        description: 'Basecore: 5.80'
      },
      {
        id: 'asset_tag1', height: '30', fill: '#2ECC71',
        x: 100, y: 0,
        description: 'Basecore: 5.80'
      },
      {
        id: 'wearable_device0', height: '30', fill: '#F5B041',
        x: 0, y: -200,
        description: 'Basecore: 7.80'
      },
      {
        id: 'wearable_device1', height: '30', fill: '#F5B041',
        x: 0, y: 200,
        description: 'Basecore: 7.80'
      },
      {
        id: 'computer', height: '30', fill: 'red',
        x: 800, y: 0,
        description: 'Attacker'
      },
    ],

    "edges": [
      { from: 'surveillance', to: 'entrance_guard' , stroke: { color: "red" }},
      { from: 'door_window_alarm_sensor1', to: 'alarm' , stroke: { color: "red" }},
      { from: 'door_window_alarm_sensor0', to: 'door_window_alarm_sensor1' , stroke: { color: "red" } },
      { from: 'alarm', to: 'entrance_guard'},
      { from: 'alarm', to: 'surveillance', stroke: { color: "red" }},
      { from: 'computer', to: 'door_window_alarm_sensor0', stroke: { color: "red" } },
      { from: 'asset_tag0', to: 'alarm' },
      { from: 'asset_tag1', to: 'alarm' },
      { from: 'asset_tag0', to: 'asset_tag1' },
      { from: 'wearable_device0', to: 'wearable_device1' },
      { from: 'wearable_device0', to: 'alarm' },
      { from: 'wearable_device1', to: 'alarm' },
    ]
  }

  var chart = anychart.graph(data);

  chart.title("The Most risk Path in Combined Security Systerm(Maximum CVSS Base Score: 80.20)");

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
  chart.layout().type('fixed');

  // initiate drawing the chart
  chart.container('container').draw();
});
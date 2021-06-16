anychart.onDocumentReady(function () {

  // create data
  var data = {
    "nodes": [
      // hardwares
      {
        id: 'light0', height: '30', fill: '#F7DC6F',
        description: 'Basecore: 9.30.'
      },
      {
        id: 'light1', height: '30', fill: '#F7DC6F',
        description: 'Basecore: 9.30'
      },
      {
        id: 'occupancy_sensor', height: '30', fill: '#DC7633',
        description: 'Basecore: 7.50'
      },
      {
        id: 'brightness_sensor', height: '30', fill: '#AF7AC5',
        description: 'Basecore: 5.00'
      },
      {
        id: 'light_controller', height: '30', fill: '#3498DB',
        description: 'Basecore: 10.00'
      },
      {
        id: 'motion_sensor', height: '30', fill: '#5146bb',
        description: 'Basecore: 5.00'
      },
    ],

    "edges": [
      { from: 'light0', to: 'light1' },
      { from: 'light0', to: 'occupancy_sensor' },
      { from: 'light0', to: 'brightness_sensor' },
      { from: 'light0', to: 'light_controller' },


      { from: 'light1', to: 'light0' },
      { from: 'light1', to: 'occupancy_sensor' },
      { from: 'light1', to: 'brightness_sensor' },
      { from: 'light1', to: 'light_controller' },

      { from: 'motion_sensor', to: 'occupancy_sensor' },
      { from: 'motion_sensor', to: 'brightness_sensor' },

      { from: 'occupancy_sensor', to: 'light0' },
      { from: 'occupancy_sensor', to: 'light1' },
      { from: 'occupancy_sensor', to: 'brightness_sensor' },
      { from: 'occupancy_sensor', to: 'light_controller' },

      { from: 'brightness_sensor', to: 'light0' },
      { from: 'brightness_sensor', to: 'light1' },
      { from: 'brightness_sensor', to: 'occupancy_sensor' },
      { from: 'brightness_sensor', to: 'light_controller' },

      { from: 'light_controller', to: 'light0' },
      { from: 'light_controller', to: 'light1' },
      { from: 'light_controller', to: 'occupancy_sensor' },
      { from: 'light_controller', to: 'brightness_sensor' },
    ]
  }

  var chart = anychart.graph(data);

  chart.title("Light Systerm Connection");

  // configure nodes
  // chart.nodes().labels().enabled(true);
  // chart.nodes().labels().format("{%id}");
  // chart.nodes().labels().fontSize(12);

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
  chart.edges().tooltip().format(`
    {%from} -> {%to}
    {%to} -> {%from}
    `);

  chart.layout().type('force');

  // initiate drawing the chart
  chart.container('container').draw();
});
anychart.onDocumentReady(function () {

  var data = {
    "nodes": [
      // hardwares
      {
        id: 'light0', height: '30', fill: '#F7DC6F',
        x: 200, y: 0,
        description: 'Basecore: 8.50'
      },
      {
        id: 'light1', height: '30', fill: '#F7DC6F',
        x: 150, y: 200,
        description: 'Basecore: 8.50'
      },
      {
        id: 'occupancy_sensor', height: '30', fill: '#DC7633',
        x: -200, y: 0,
        description: 'Basecore: 7.50'
      },
      {
        id: 'brightness_sensor', height: '30', fill: '#AF7AC5',
        x: -150, y: 200,
        description: 'Basecore: 3.30'
      },
      {
        id: 'light_controller', height: '30', fill: '#3498DB',
        x: 0, y: -150,
        description: 'Basecore: 8.00'
      },
      {
        id: 'motion_sensor', height: '30', fill: '#5146bb',
        x: 0, y: -50,
        description: 'Basecore: 5.00'
      },

      // attackers
      {
        id: 'computer', height: '30', fill: '#DC143C',
        x: 400, y: 0,
        description: 'Attacker'
      },
    ],

    "edges": [
      { from: 'light0', to: 'light1' },
      { from: 'light0', to: 'brightness_sensor' },
      { from: 'light0', to: 'light_controller', stroke: { color: "red" } },


      { from: 'light1', to: 'light0' },
      { from: 'light1', to: 'occupancy_sensor', stroke: { color: "red" } },
      { from: 'light1', to: 'light_controller' },

      { from: 'motion_sensor', to: 'occupancy_sensor' },
      { from: 'motion_sensor', to: 'brightness_sensor', stroke: { color: "red" } },

      { from: 'occupancy_sensor', to: 'light0', stroke: { color: "red" } },
      { from: 'occupancy_sensor', to: 'light1' },
      { from: 'occupancy_sensor', to: 'brightness_sensor' },
      { from: 'occupancy_sensor', to: 'light_controller' },

      { from: 'brightness_sensor', to: 'light0' },
      { from: 'brightness_sensor', to: 'light1', stroke: { color: "red" } },
      { from: 'brightness_sensor', to: 'occupancy_sensor' },
      { from: 'brightness_sensor', to: 'light_controller' },

      { from: 'light_controller', to: 'light0' },
      { from: 'light_controller', to: 'light1' },
      { from: 'light_controller', to: 'occupancy_sensor' },
      { from: 'light_controller', to: 'brightness_sensor' },

      { from: 'computer', to: 'motion_sensor', stroke: { color: "red" } },
      //   {from: 'computer2', to:'light1'},
      //   {from: 'computer3', to:'occupancy_sensor'},
      //   {from: 'computer4', to:'brightness_sensor'},
      //   {from: 'computer5', to:'light_controller'},
    ]
  }

  var chart = anychart.graph(data);

  chart.title("Most Risk Path in Light Systerm(Maximum CVSS Base Score: 40.80)");

  // configure nodes
  // chart.nodes().labels().enabled(true);
  // chart.nodes().labels().format("{%name}");
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

  chart.layout().type('fixed');

  // initiate drawing the chart
  chart.container('container').draw();
});
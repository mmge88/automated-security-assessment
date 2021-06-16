anychart.onDocumentReady(function () {

  var data = {
    "nodes": [
      // hardwares
      {
        id: 'light0', height: '30', fill: '#F7DC6F',
        x: 550, y: 320,
        description: 'Basecore: 10.50'
      },
      {
        id: 'light1', height: '30', fill: '#F7DC6F',
        x: 450, y: 300,
        description: 'Basecore: 10.50'
      },
      {
        id: 'occupancy_sensor', height: '30', fill: '#DC7633',
        x: 250, y: 100,
        description: 'Basecore: 5.00'
      },
      {
        id: 'brightness_sensor', height: '30', fill: '#AF7AC5',
        x: 500, y: 200,
        description: 'Basecore: 12.10'
      },
      {
        id: 'light_controller', height: '30', fill: '#3498DB',
        x: 300, y: 300,
        description: 'Basecore: 8.00'
      },
      {
        id: 'motion_sensor', height: '30', fill: '#5146bb',
        x: 550, y: -100,
        description: 'Basecore: 5.00'
      },
      {
        id: 'projector', height: '30', fill: '#D35400',
        x: -300, y: -200,
        description: 'Basecore: 7.10'
      },
      {
        id: 'TV', height: '30', fill: '#B7950B',
        x: -170, y: 300,
        description: 'Basecore: 5.00'
      },
      {
        id: 'speaker', height: '30', fill: '#34495E',
        x: -50, y: 200,
        description: 'Basecore: 7.80'
      },
      {
        id: 'media_player', height: '30', fill: '#2b7e47',
        x: -150, y: 100,
        description: 'Basecore: 9.30'
      },
      {
        id: 'ventilator', height: '30', fill: '#EDBB99',
        x: 250, y: -100,
        description: 'Basecore: 5.00'
      },
      {
        id: 'heater', height: '30', fill: '#2E86C1',
        x: 300, y: -200,
        description: 'Basecore: 9.40'
      },
      {
        id: 'thermometer', height: '30', fill: '#86bd2d',
        x: 300, y: 100,
        description: 'Basecore: 9.70'
      },
      {
        id: 'humidity_sensor', height: '30', fill: '#B7950B',
        x: 300, y: 200,
        description: 'Basecore: 10.20'
      },
      {
        id: 'CO2_sensor', height: '30', fill: '#8E44AD',
        x: 150, y: 300,
        description: 'Basecore: 10.20'
      },
      {
        id: 'air_conditioner', height: '30', fill: '#873600',
        x: 50, y: 100,
        description: 'Basecore: 7.20'
      },
      {
        id: 'window_sensor0', height: '30', fill: '#0b5a35',
        x: 120, y: -200,
        description: 'Basecore: 11.70'
      },
      {
        id: 'window_sensor1', height: '30', fill: '#0b5a35',
        x: 120, y: -100,
        description: 'Basecore: 11.70'
      },
      {
        id: 'CO_sensor', height: '30', fill: '#2ECC71',
        x: 470, y: 100,
        description: 'Basecore: 15.00'
      },
      {
        id: 'fire_alarm', height: '30', fill: '#F5B041',
        x: 380, y: 200,
        description: 'Basecore: 10.00'
      },
      {
        id: 'smoke_sensor', height: '30', fill: '#1b34c5',
        x: 10, y: 300,
        description: 'Basecore: 12.50'
      },


      // attackers
      {
        id: 'computer', height: '30', fill: '#DC143C',
        x: 600, y: 0,
        description: 'Attacker'
      },
    ],

    "edges": [
      { from: 'light0', to: 'light1', stroke: { color: "red" } },
      { from: 'light0', to: 'light_controller' },

      { from: 'light1', to: 'light0' },
      { from: 'light1', to: 'occupancy_sensor' },
      { from: 'light1', to: 'light_controller', stroke: { color: "red" } },

      { from: 'motion_sensor', to: 'occupancy_sensor' },
      { from: 'motion_sensor', to: 'brightness_sensor', stroke: { color: "red" } },

      { from: 'occupancy_sensor', to: 'light0' },
      { from: 'occupancy_sensor', to: 'light1' },
      { from: 'occupancy_sensor', to: 'brightness_sensor' },

      { from: 'brightness_sensor', to: 'light0', stroke: { color: "red" } },
      { from: 'brightness_sensor', to: 'light1' },
      { from: 'brightness_sensor', to: 'occupancy_sensor' },
      { from: 'brightness_sensor', to: 'light_controller' },

      { from: 'light_controller', to: 'light0' },
      { from: 'light_controller', to: 'light1' },
      { from: 'light_controller', to: 'occupancy_sensor', stroke: { color: "red" } },
      { from: 'light_controller', to: 'brightness_sensor' },

      { from: 'media_player', to: 'projector' },
      { from: 'projector', to: 'speaker' },
      { from: 'media_player', to: 'TV' },
      { from: 'media_player', to: 'brightness_sensor' },
      { from: 'TV', to: 'speaker' },

      { from: 'humidity_sensor', to: 'ventilator' },
      { from: 'humidity_sensor', to: 'heater' },
      { from: 'humidity_sensor', to: 'air_conditioner' },

      { from: 'CO2_sensor', to: 'ventilator' },

      { from: 'thermometer', to: 'heater' },
      { from: 'thermometer', to: 'air_conditioner' },

      { from: 'occupancy_sensor', to: 'heater' },
      { from: 'occupancy_sensor', to: 'air_conditioner', stroke: { color: "red" } },

      { from: 'window_sensor0', to: 'window_sensor1' },
      { from: 'window_sensor0', to: 'heater' },
      { from: 'window_sensor0', to: 'air_conditioner' },

      { from: 'window_sensor1', to: 'heater' },
      { from: 'window_sensor1', to: 'air_conditioner' },

      { from: 'CO_sensor', to: 'fire_alarm' },
      { from: 'thermometer', to: 'fire_alarm' },
      { from: 'smoke_sensor', to: 'fire_alarm' },

      { from: 'computer', to: 'motion_sensor', stroke: { color: "red" } },
    ]
  }

  var chart = anychart.graph(data);

  chart.title("Most Risk Path in Combined ALFH Systerm(Maximum CVSS Base Score: 58.30)");

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
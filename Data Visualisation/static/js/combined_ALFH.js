anychart.onDocumentReady(function () {

  // create data
  var data = {
    "nodes": [
      // hardwares
      {
        id: 'light0', height: '30', fill: '#F7DC6F',
        description: 'Basecore: 12.20.'
      },
      {
        id: 'light1', height: '30', fill: '#F7DC6F',
        description: 'Basecore: 12.20'
      },
      {
        id: 'occupancy_sensor', height: '30', fill: '#DC7633',
        description: 'Basecore: 7.50'
      },
      {
        id: 'brightness_sensor', height: '30', fill: '#AF7AC5',
        description: 'Basecore: 14.40'
      },
      {
        id: 'light_controller', height: '30', fill: '#3498DB',
        description: 'Basecore: 10.00'
      },
      {
        id: 'motion_sensor', height: '30', fill: '#5146bb',
        description: 'Basecore: 5.00'
      },
      {
        id: 'projector', height: '30', fill: '#D35400',
        description: 'Basecore: 7.80'
      },
      {
        id: 'TV', height: '30', fill: '#B7950B',
        description: 'Basecore: 7.80'
      },
      {
        id: 'speaker', height: '30', fill: '#34495E',
        description: 'Basecore: 7.80'
      },
      {
        id: 'media_player', height: '30', fill: '#2b7e47',
        description: 'Basecore: 9.30'
      },
      {
        id: 'ventilator', height: '30', fill: '#EDBB99',
        description: 'Basecore: 5.00'
      },
      {
        id: 'heater', height: '30', fill: '#2E86C1',
        description: 'Basecore: 16.40'
      },
      {
        id: 'thermometer', height: '30', fill: '#86bd2d',
        description: 'Basecore: 16.40'
      },
      {
        id: 'humidity_sensor', height: '30', fill: '#B7950B',
        description: 'Basecore: 11.80'
      },
      {
        id: 'CO2_sensor', height: '30', fill: '#8E44AD',
        description: 'Basecore: 16.80'
      },
      {
        id: 'air_conditioner', height: '30', fill: '#873600',
        description: 'Basecore: 7.20'
      },
      {
        id: 'window_sensor0', height: '30', fill: '#0b5a35',
        description: 'Basecore: 10.20'
      },
      {
        id: 'window_sensor1', height: '30', fill: '#0b5a35',
        description: 'Basecore: 10.20'
      },
      {
        id: 'CO_sensor', height: '30', fill: '#2ECC71',
        description: 'Basecore: 16.80'
      },
      {
        id: 'fire_alarm', height: '30', fill: '#F5B041',
        description: 'Basecore: 10.00'
      },
      {
        id: 'smoke_sonsor', height: '30', fill: '#1b34c5',
        description: 'Basecore: 14.00'
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
      { from: 'occupancy_sensor', to: 'air_conditioner' },

      { from: 'window_sensor0', to: 'window_sensor1' },
      { from: 'window_sensor0', to: 'heater' },
      { from: 'window_sensor0', to: 'air_conditioner' },

      { from: 'window_sensor1', to: 'heater' },
      { from: 'window_sensor1', to: 'air_conditioner' },

      { from: 'CO_sensor', to: 'fire_alarm' },
      { from: 'thermometer', to: 'fire_alarm' },
      { from: 'smoke_sonsor', to: 'fire_alarm' },
    ]
  }

  var chart = anychart.graph(data);

  chart.title("Combined ALFH Systerm Connection");

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
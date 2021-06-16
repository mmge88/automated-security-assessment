anychart.onDocumentReady(function () {

  // create data
  var data = {
    "nodes": [
      // hardwares
      {
        id: 'asset_tag0', height: '30', fill: '#2ECC71',
        description: 'Basecore: 7.90'
      },
      {
        id: 'asset_tag1', height: '30', fill: '#2ECC71',
        description: 'Basecore: 7.90'
      },
      {
        id: 'wearable_device0', height: '30', fill: '#F5B041',
        description: 'Basecore: 10.00'
      },
      {
        id: 'wearable_device1', height: '30', fill: '#F5B041',
        description: 'Basecore: 10.00'
      },
      {
        id: 'alarm', height: '30', fill: '#3498DB',
        description: 'Basecore: 18.30'
      },
    ],

    "edges": [
      { from: 'asset_tag0', to: 'alarm' },
      { from: 'asset_tag1', to: 'alarm' },
      { from: 'asset_tag0', to: 'asset_tag1' },
      { from: 'wearable_device0', to: 'wearable_device1' },
      { from: 'wearable_device0', to: 'alarm' },
      { from: 'wearable_device1', to: 'alarm' },

    ]
  }

  var chart = anychart.graph(data);

  chart.title("Resources Tracking Systerm Connection");

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
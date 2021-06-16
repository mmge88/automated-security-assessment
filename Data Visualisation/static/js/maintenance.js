anychart.onDocumentReady(function() {

    // create data
    var data= {
      "nodes":[
      			// hardwares
        {
            id:'electrical_current_monitoring_sensor', height: '30', fill: '#2ECC71', 
            description: 'Basecore: 12.80'
        },
        {
            id:'water_monitoring_sensor', height: '30',  fill: '#F5B041',
            description: 'Basecore: 3.30'
        },
        {
            id:'repair_alarm', height: '30', fill:'#3498DB',
            description: 'Basecore: 5.00'
        },
      ],
  
      "edges":[
        {from: 'electrical_current_monitoring_sensor', to:'repair_alarm'},
        {from: 'water_monitoring_sensor', to:'repair_alarm'},
        
      ]}
  
    var chart = anychart.graph(data);
  
    chart.title("Maintenance Systerm Connection");
  
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
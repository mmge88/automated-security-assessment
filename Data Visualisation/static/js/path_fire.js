anychart.onDocumentReady(function() {

    // create data
    var data= {
      "nodes":[
      			// hardwares
        {
            id:'CO_sensor', height: '30', fill: '#2ECC71', 
            description: 'Basecore: 15.00'
        },
        {
            id:'fire_alarm', height: '30',  fill: '#F5B041', 
            description: 'Basecore: 10.00'
        },
        {
            id:'thermometer', height: '30', fill:'#3498DB',
            description: 'Basecore: 9.70'
        },
        {
          id:'smoke_sensor', height: '30', fill:'#1b34c5',
          description: 'Basecore: 12.50'
      },
    
        // attackers
        {
            id:'computer', height: '30', fill: '#DC143C', 
            description: 'Attacker'
        },
      ],
  
      "edges":[
        {from: 'CO_sensor', to:'fire_alarm', stroke:  {color: "red"}},
        {from: 'thermometer', to:'fire_alarm'},
        {from: 'smoke_sensor', to:'fire_alarm'},
        {from: 'computer', to: 'CO_sensor', stroke:  {color: "red"}},
      ]}
  
    var chart = anychart.graph(data);
  
    chart.title("The Most Risk Path in Fire Detection Systerm(Maximum CVSS Base Score: 25.00)");
  
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
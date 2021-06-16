anychart.onDocumentReady(function() {

    // create data
    var data= {
      "nodes":[
      			// hardwares
        {
            id:'ventilator', height: '30', fill: '#EDBB99', 
            description: 'Basecore: 5.00'
        },
        {
            id:'heater', height: '30',  fill: '#2E86C1', 
            description: 'Basecore: 9.40'
        },
        {
            id:'thermometer', height: '30', fill:'#F39C12',
            description: 'Basecore: 9.70'
        },
        {
            id:'humidity_sensor', height: '30', fill:'#B7950B',
            description: 'Basecore: 10.20'
        },
        {
            id:'CO2_sensor', height: '30', fill:'#8E44AD', 
            description: 'Basecore: 10.20'
        },
        {
            id:'occupancy_sensor', height: '30', fill:'#27AE60', 
            description: 'Basecore: 7.50'
        },
        {
            id:'air_conditioner', height: '30', fill:'#873600', 
            description: 'Basecore: 7.20'
        },
        {
            id:'window_sensor0', height: '30', fill:'#0b5a35', 
            description: 'Basecore: 11.70'
        },
        {
            id:'window_sensor1', height: '30', fill:'#0b5a35', 
            description: 'Basecore: 11.70'
        },
        {
            id:'computer', height: '30', fill:'red', 
            description: 'attacker'
        },
      ],
  
      "edges":[
        {from: 'humidity_sensor', to:'ventilator'},
        {from: 'humidity_sensor', to:'heater'},
        {from: 'humidity_sensor', to:'air_conditioner'},

        {from: 'CO2_sensor', to:'ventilator'},

        {from: 'thermometer', to: 'heater'},
        {from: 'thermometer', to: 'air_conditioner'},

        {from: 'occupancy_sensor', to: 'heater'},
        {from: 'occupancy_sensor', to: 'air_conditioner'},

        {from: 'window_sensor0', to: 'window_sensor1', stroke:  {color: "red"}},
        {from: 'window_sensor0', to: 'heater'},
        {from: 'window_sensor0', to: 'air_conditioner'},

        {from: 'window_sensor1', to: 'heater', stroke:  {color: "red"}},
        {from: 'window_sensor1', to: 'air_conditioner'},

        {from: 'computer', to: 'window_sensor0', stroke:  {color: "red"}},
      ]}
  
    var chart = anychart.graph(data);
  
    chart.title("The Most Risk Path in HVAC Systerm(Maximum CVSS Base Score: 33.10)");
  
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
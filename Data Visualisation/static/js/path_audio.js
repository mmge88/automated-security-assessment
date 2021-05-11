anychart.onDocumentReady(function() {

    // create data
    var data= {
      "nodes":[
      			// hardwares
        {
            id:'projector', height: '30', fill: '#D35400', 
            description: 'Basecore: 7.80'
        },
        {
            id:'TV', height: '30',  fill: '#B7950B', 
            description: 'Basecore: 7.80'
        },
        {
            id:'brightness_sensor', height: '30', fill:'#9B59B6',
            description: 'Basecore: 12.20'
        },
        {
            id:'speaker', height: '30', fill:'#34495E', 
            description: 'Basecore: 7.80'
        },
        
        // attackers
        {
            id:'computer', height: '30', fill: '#DC143C', 
            description: 'Attacker'
        },
      ],
  
      "edges":[
        {from: 'brightness_sensor', to:'projector', stroke:  {color: "red"}},
        {from: 'projector', to:'speaker', stroke:  {color: "red"}},
        {from: 'brightness_sensor', to:'TV'},
        {from: 'TV', to:'speaker'},
        {from: 'computer', to: 'brightness_sensor', stroke:  {color: "red"}},
      ]}
  
    var chart = anychart.graph(data);
  
    chart.title("The Most Risk Path Audiovisual Systerm(Maximum CVSS Base Score: 25.40)");
  
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
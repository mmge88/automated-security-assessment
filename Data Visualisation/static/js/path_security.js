anychart.onDocumentReady(function() {

  // create data
  var data= {
    "nodes":[
          // hardwares
      {
          id:'entrance_guard', height: '30', fill: ' #3498DB', 
          x:100,y:100,
          description: 'Basecore: 12.50'
      },
      {
          id:'surveillance', height: '30',  fill: '#DC7633',
          x:400,y:0,
          description: 'Basecore: 21.10'
      },
      {
          id:'alarm', height: '30', fill:'#AF7AC5',
          x:100,y:-100,
          description: 'Basecore: 18.30'
      },
      {
        id:'computer', height: '30', fill:'red',
        x:600,y:0,
        description: 'Attacker'
    },
    ],

    "edges":[
      {from: 'surveillance', to:'entrance_guard'},
      {from: 'surveillance', to: 'alarm', stroke:  {color: "red"}},

      {from: 'alarm', to: 'entrance_guard', stroke:  {color: "red"}},
      {from: 'alarm', to: 'surveillance'},

      {from: 'computer', to: 'surveillance', stroke:  {color: "red"}},
    ]}

  var chart = anychart.graph(data);

  chart.title("The Most risk Path in Security Systerm(Maximum CVSS Base Score: 59.40)");

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
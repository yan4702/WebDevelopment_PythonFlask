


function dataD3Chart(){
  $.ajax({
      url: '/dataForChart',
      type: 'GET',
      success: function(data) {

        //empty array to store data from flask. 
        let dateArray = [];
        let caloriesArray = [];
        let jsonArray = [];
           
        for (i in data.date){
          //variousKeyWords.push(data.date[i]) 
          //console.log(new Date(data.date[i]))
          dateArray.push(new Date(data.date[i]))
        } 
        
        //parseInt(data.value[i]).toFixed(1)
        for (i in data.value){
          //console.log(data.value[i])
          caloriesArray.push(parseInt(data.value[i]).toFixed(1))
        }

        //to testing print out the data in dataArray
        for (i in dateArray){
          console.log(dateArray[i])
        }

      //parseInt(caloriesArray[i]).toFixed(1)
      var i;
      for (i = 0; i < dateArray.length; i++) {
        jsonArray.push({date: dateArray[i], value: parseInt(caloriesArray[i]).toFixed(1)})
        }
      console.log(jsonArray)
      createChart(jsonArray)
           
      }          
  });
}
dataD3Chart()
 
  
  function createChart(data) {
    var widthOfChartSVG = 550, heightOfChartSVG = 330;   
    var margin = { top: 18, right: 18, bottom: 28, left: 48 };   
    var height = heightOfChartSVG - margin.top - margin.bottom;
    var width = widthOfChartSVG - margin.left - margin.right; 

    var svg = d3.select('svg')     
        .attr("height", heightOfChartSVG)
        .attr("width", widthOfChartSVG);  

    var g = svg.append("g")   
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")" );
    var y = d3.scaleLinear().rangeRound([height, 0]);
    var x = d3.scaleTime().rangeRound([0, width]);

    var line = d3.line()   
        .y(function(d) { return y(d.value)})   
        .x(function(d) { return x(d.date)})   
    y.domain(d3.extent(data, function(d) { return d.value }));
    x.domain(d3.extent(data, function(d) { return d.date }));   
  
    g.append("g")   
        .attr("transform", "translate(0," + height + ")")   
        .call(d3.axisBottom(x))   
        .select(".domain")   
        .remove();
  
    g.append("g")   
        .call(d3.axisLeft(y))   
        .append("text")   
        .attr("fill", "#000")   
        .attr("transform", "rotate(-90)")   
        .attr("y", 6)   
        .attr("dy", "0.71em")   
        .attr("text-anchor", "end")   
        .text("Total Calories consumed");
  
    g.append("path")
        .datum(data).attr("fill", "none")
        .attr("stroke", "steelblue")
        .attr("stroke-linejoin", "round")
        .attr("stroke-linecap", "round")
        .attr("stroke-width", 1.5)
        .attr("d", line);
  
}
  

    
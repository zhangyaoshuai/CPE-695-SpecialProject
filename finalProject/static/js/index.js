/**
 * Created by EricZhang on 12/2/16.
 */
$(document).ready(function () {
    var response;
    $.ajax({
        url: '/getBuildings',
        data: {'kword': "all"},
        type: 'get',
        success: function(data) {
            response = data;
            var dataset = [];
            for(var key in response) {
                dataset.push({building: key, number: response[key]});
            }
            generateChart(dataset)
        }
    });
    $.ajax({
        url: '/getData',
        type: 'get',
        success: function (data) {
            console.log(data);
            generateDotChart(data)
        }
    });
    $('#leastCommon').on('click', function () {
        $('#sort').prop('checked', false);
        d3.select("svg").remove();
        $.ajax({
            url: '/getBuildings',
            data: {'kword': $('#leastCommon').attr('name')},
            type: 'get',
            success: function(data) {
                response = data;
                var dataset = [];
                for(var key in response) {
                    dataset.push({building: key, number: response[key]});
                }
                generateChart(dataset)
            }
        });
    });
    $('#mostCommon').on('click', function () {
        $('#sort').prop('checked', false);
        d3.select("svg").remove();
        $.ajax({
            url: '/getBuildings',
            data: {'kword': $('#mostCommon').attr('name')},
            type: 'get',
            success: function(data) {
                response = data;
                var dataset = [];
                for(var key in response) {
                    dataset.push({building: key, number: response[key]});
                }
                generateChart(dataset)
            }
        });
    });

    var generateChart = function (dataset) {
        var margin = {top: 10, right: 0, bottom: 20, left: 50},
            width = 700 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;
        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .3, 0.3);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
        if(dataset.length > 10) {
            xAxis.scale(x)
            .orient("bottom")
            .tickFormat(function (d) { return ''; });
        }
        else {
            xAxis.scale(x)
            .orient("bottom")
        }
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");
        var tip = d3.tip()
            .attr('class', 'd3-tip')
            .offset([-10, 0])
            .html(function(d) {
                return "<strong><span style='color:white'>" + d.building + "</span></strong>";
            });
        var svg = d3.select("#svg1").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
            .on('mouseover', tip);
        svg.call(tip);

        x.domain(dataset.map(function(d) { return d.building; }));
        y.domain([0, d3.max(dataset, function(d) { return d.number; })]);

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("transform", "rotate(-90)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Number");

        svg.selectAll(".bar")
            .data(dataset)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", function(d) { return x(d.building); })
            .attr("width", x.rangeBand())
            .attr("y", function(d) { return y(d.number); })
            .attr("height", function(d) { return height - y(d.number); })
            .on('mouseover', tip.show)
            .on('mouseout', tip.hide);

        var sortTimeout = setTimeout(function() {

        }, 2000);

        $('#sort').on("change", change);

        function change() {
            clearTimeout(sortTimeout);
            // Copy-on-write since tweens are evaluated after a delay.
            var x0 = x.domain(dataset.sort(this.checked
                ? function(a, b) { return b.number - a.number; }
                : function(a, b) { return d3.ascending(a.building, b.building); })
                .map(function(d) { return d.building; }))
                .copy();

            svg.selectAll(".bar")
                .sort(function(a, b) { return x0(a.building) - x0(b.building); });
            var transition = svg.transition().duration(750),
                delay = function(d, i) { return i * 50; };

            transition.selectAll(".bar")
                .delay(delay)
                .attr("x", function(d) { return x0(d.building); });

            transition.select(".x.axis")
                .call(xAxis)
                .selectAll("g")
                .delay(delay);
        }
    };
    var generateDotChart = function (data) {
        var margin = {top: 10, right: 0, bottom: 20, left: 50},
            width = 700 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;

        /*
         * value accessor - returns the value to encode for a given data object.
         * scale - maps value to a visual display encoding, such as a pixel position.
         * map function - maps from data value to display value
         * axis - sets up axis
         */

        // setup x
        var xValue = function(d) { return d.friends_count;}, // data -> value
            xScale = d3.scale.linear().range([0, width]), // value -> display
            xMap = function(d) { return xScale(xValue(d));}, // data -> display
            xAxis = d3.svg.axis().scale(xScale).orient("bottom");

        // setup y
        var yValue = function(d) { return d.followers_count;}, // data -> value
            yScale = d3.scale.linear().range([height, 0]), // value -> display
            yMap = function(d) { return yScale(yValue(d));}, // data -> display
            yAxis = d3.svg.axis().scale(yScale).orient("left");

        // setup fill color
        /*
        var cValue = function(d) { return d.Manufacturer;},
            color = d3.scale.category10();
        */

        // add the graph canvas to the body of the webpage
        var svg = d3.select("#svg2").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
          .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // add the tooltip area to the webpage
        var tooltip = d3.select("svg2").append("div")
            .attr("class", "tooltip")
            .style("opacity", 0);

        // load data

          // change string (from CSV) into number format
        /*
          data.forEach(function(d) {
            d.Calories = +d.Calories;
            d["Protein (g)"] = +d["Protein (g)"];
        //    console.log(d);
          });
          */

          // don't want dots overlapping axis, so add in buffer to data domain
          xScale.domain([d3.min(data, xValue)-1, d3.max(data, xValue)+1]);
          yScale.domain([d3.min(data, yValue)-1, d3.max(data, yValue)+1]);

          // x-axis
          svg.append("g")
              .attr("class", "x axis")
              .attr("transform", "translate(0," + height + ")")
              .call(xAxis)
            .append("text")
              .attr("class", "label")
              .attr("x", width)
              .attr("y", -6)
              .style("text-anchor", "end")
              .text("friends_count");

          // y-axis
          svg.append("g")
              .attr("class", "y axis")
              .call(yAxis)
            .append("text")
              .attr("class", "label")
              .attr("transform", "rotate(-90)")
              .attr("y", 6)
              .attr("dy", ".71em")
              .style("text-anchor", "end")
              .text("followers_count");

          // draw dots
          svg.selectAll(".dot")
              .data(data)
            .enter().append("circle")
              .attr("class", "dot")
              .attr("r", 3.5)
              .attr("cx", xMap)
              .attr("cy", yMap)
              .style("fill", function(d) { return })
              .on("mouseover", function(d) {
                  tooltip.transition()
                       .duration(200)
                       .style("opacity", .9);
                  tooltip.html(d["friends_count"] + "<br/> (" + 1
                    + ", " + 2 + ")")
                       .style("left", (d3.event.pageX + 5) + "px")
                       .style("top", (d3.event.pageY - 28) + "px");
              })
              .on("mouseout", function(d) {
                  tooltip.transition()
                       .duration(500)
                       .style("opacity", 0);
              });
          /*
          // draw legend
          var legend = svg.selectAll(".legend")
              .data(color.domain())
            .enter().append("g")
              .attr("class", "legend")
              .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

          // draw legend colored rectangles
          legend.append("rect")
              .attr("x", width - 18)
              .attr("width", 18)
              .attr("height", 18)
              .style("fill", color);

          // draw legend text
          legend.append("text")
              .attr("x", width - 24)
              .attr("y", 9)
              .attr("dy", ".35em")
              .style("text-anchor", "end")
              .text(function(d) { return d;})
            */
    }
});
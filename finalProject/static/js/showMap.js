/**
 * Created by EricZhang on 12/3/16.
 */
$(document).ready(function () {
    var response;
    $.ajax({
        data: {'screen_name': $('#screen_name').text()},
        url: '/getMap',
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

    $('#leastCommon').on('click', function () {
        d3.select("svg").remove();
        $.ajax({
        url: '/leastCommon',
        type: 'POST',
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
        d3.select("svg").remove();
        $.ajax({
        url: '/getBuildings',
        type: 'GET',
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
        var margin = {top: 10, right: 10, bottom: 20, left: 10},
            width = 450 - margin.left - margin.right,
            height = 300 - margin.top - margin.bottom;
        var x = d3.scale.ordinal()
            .rangeRoundBands([0, width], .3, 0.3);

        var y = d3.scale.linear()
            .range([height, 0]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");
        var svg = d3.select("#svg1").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        /*
        dataset.forEach(function(d) {
            d.number = +d.number;
        });
        */

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
            .attr("height", function(d) { return height - y(d.number); });
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
});
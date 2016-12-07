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
            console.log(response);
            var dataset = [];
            for(var key in response) {
                dataset.push({building: key, number: response[key]});
            }
            generateChart(dataset)
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
});
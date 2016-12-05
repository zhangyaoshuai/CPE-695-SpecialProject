/**
 * Created by EricZhang on 12/3/16.
 */
$(document).ready(function () {
    var response;
    var dataset = [];
    $.ajax({
        data: {'screen_name': $('#screen_name').text()},
        url: '/getUser/',
        type: 'get',
        success: function(data) {
            response = data;//json data from Flask
            for(var key in response.buildings) {
                dataset.push({building: key, number: response.buildings[key]});
            }
            dataset.sort(function (a,b) {
                return b.number - a.number
            });
            generateChart(dataset.slice(0,10));

            //define a layer for map
            var mytiles = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            });
            // Initialise an empty map
            var map = L.map('map');
            map.addLayer(mytiles);
            var markers = new L.LayerGroup().addTo(map);
            showMap(response, markers, map)
        }
    });

    $('#leastCommon').on('click', function () {
        d3.select("svg").remove();
        dataset.sort(function (a,b) {
            return a.number - b.number
        });
        generateChart(dataset.slice(0,10));


    });
    $('#mostCommon').on('click', function () {
        d3.select("svg").remove();
        dataset.sort(function (a,b) {
            return b.number - a.number
        });
        generateChart(dataset.slice(0,10));
    });

    var generateChart = function (dataset) {
        var margin = {top: 10, right: 10, bottom: 20, left: 30},
            width = 550 - margin.left - margin.right,
            height = 350 - margin.top - margin.bottom;
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
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        svg.call(tip);
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

    //generate map
    var showMap = function(geoData, markers, map) {
        markers.clearLayers();
        var lat = [];
        var lng = [];
        for (var i = 0; i < geoData.features.length; i++) {
            lat.push(geoData.features[i].coordinates[0]);
            lng.push(geoData.features[i].coordinates[1]);
        }
        var latMiddle = (Math.max.apply(null, lat) + Math.min.apply(null, lat)) / 2;
        var lngMiddle = (Math.max.apply(null, lng) + Math.min.apply(null, lng)) / 2;
        map.setView([lngMiddle,latMiddle], 12);
        // specify popup options
        var customOptions = {
        'maxWidth': '250',
        'className' : 'custom-popup'
        };
        for (var i = 0; i < geoData.features.length; i++) {
            if (geoData.features[i].buildings != "") {
                L.marker([geoData.features[i].coordinates[1], geoData.features[i].coordinates[0]])
                    .bindPopup("<div class='panel panel-default'><div class='panel-heading'><h4 class='text-warning'>" +
                        geoData.features[i].buildings[0].name + "</h4>" + "<h4 class='text-primary'>" + geoData.features[i].buildings[0].type + "</h4></div><div class='panel-body'><div class='caption'><h4>" +
                        geoData.features[i].text + "</h4></div><h4><span class=text-danger>" +
                        geoData.features[i].created_at + "</span></h4></div>", customOptions)
                    .addTo(map)
                    .on('mouseover', function (e) {
                        this.openPopup();
                    })
                    .on('mouseout', function (e) {
                        this.closePopup();
                    })
                    .on('click', function (e) {
                        this.off('mouseout');
                        this.openPopup();
                    })
            }
        }
    }

});
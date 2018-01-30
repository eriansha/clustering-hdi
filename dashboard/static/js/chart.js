function plot3d(dict, color) {
	var x_value = [],
		y_value = [],
		z_value = [],
		cluster = [];
		kab_value = []

	dict.forEach(function(d) {
		x_value.push(d.coordinate[0]);
		y_value.push(d.coordinate[1]);
		z_value.push(d.ipm);
		if (d.cluster == -1)
		{
			cluster.push('#000');
		}
		cluster.push(color(d.cluster));
		kab_value.push(d.kabupaten);
	});

	var plot = {
		hoverinfo: "z+text",
		hoverlabel: {
			bgcolor: cluster,
			bordercolor: cluster,
			font: {
				family: 'Courier New, monospace',
				size: 15,
				color: '#ffffff'
			},
		},
		x: x_value,
		y: y_value,
		z: z_value,
		hovertext: kab_value,
		mode: 'markers',
		marker: {
			color: cluster,
			size: 5,
			line: {
				width: 0.5
			},
			opacity: 0.8,
		},
		type: 'scatter3d'
	};

	var data = [plot];
	var layout = {
			margin: {
				l: 100,
				r: 0,
				b: 0,
				t: 0
			},
			scene: {
				xaxis: { title: 'longitude'},
				yaxis: { title: 'latitude'},
				zaxis: { title: 'IPM' }
			}
		};
	Plotly.newPlot('my3dplot', data, layout);
}

function geo_scatter(selection, json_data, color) {
	var center = d3.geoCentroid(topojson.feature(json_data, json_data.objects.jawa));
	var subunits = topojson.feature(json_data, json_data.objects.jawa);

	var projection =  d3.geoMercator()
	    				.center(center)
	    				.scale(7000)
     					.translate([areaWidth /2, areaHeight /2]);

	var path = d3.geoPath()
	    		 .projection(projection);

	selection.append('path')
	    	 .datum(subunits)
	    	 .attr('d', path);

	selection.selectAll(".provinsi")
	    	 .data(topojson.feature(json_data, json_data.objects.jawa).features)
	    	 .enter()
	    	 .append('path')
	    	 .attr('class', function(d) { 
	    		var namaProv = d.id.replace(/\s/g, "");
	    		return "provinsi " + namaProv 
	    	 })
	    	 .attr('d', path);

	// add circle to svg
	selection.call(plot_circle, color, dict, projection)

	// create legend for map
	selection.call(create_legend, color, dict);
}


function plot_circle(selection, color, dataset, projection) {
	var circles = selection.selectAll('circle')
	    				   .data(dataset)
	    				   .enter()
	    				   .append('circle');

	var circleAttr = circles.attr('cx', function(d) {
	    									var coordinate = d.coordinate;
	    									return projection(coordinate)[0]; 
	    								})
	    								.attr('cy', function(d) {
	    									var coordinate = d.coordinate; 
	    									return projection(coordinate)[1];
	    								})
	    								.attr('r', '6px')
	    								.attr('fill', function(d) {
	    								//console.log(d[2]);
	    								if (d.cluster == -1) return '#000'
	    									else {
	    									  	return color(d.cluster);
	    									  	}
	    								});

	// hovering tooltips
	circleAttr.on("mouseover", function(d) {
	    			tooltip.transition(200)
	    				   .duration(200)
	    				   .style('opacity', 0.9);
	    			tooltip.text(d.kabupaten)
	    				   .style('left', (d3.event.pageX - 10) + "px")
	    				   .style('top', (d3.event.pageY - 65) + "px");
	    		})
	    		.on("mouseout", function(d) {
	    			tooltip.transition()
	    					.duration(500)
	    					.style('opacity', 0)
	    		});

	// add bar chart while click the plot
	circleAttr.on("click", function(d) {
	    d3.select('#myBarChart')
	      .call(draw_bar, color, d, dataset);	
	});
}

function draw_bar(selection, color, datum, dataset) {
	// remove previous bar chart
	selection.selectAll('svg').remove();

	// Add header
	d3.select('#bar-header')
	  .html('<i class="fa fa-bar-chart"></i> Bar Chart: ' + datum.kabupaten);
	  		
	// x-scale and y-scale
	var xScale = d3.scaleBand()
			  	   .rangeRound([0, barWidth], .4),
		yScale = d3.scaleLinear().range([barHeight, 0]);

	var xAxis = d3.axisBottom(xScale),
		yAxis = d3.axisLeft(yScale);

	// Create bar container
	var barChart = selection.append('svg')
			  				.attr('width', barWidth + margin.left + margin.right)
			  				.attr('height', barHeight + margin.top + margin.bottom)
			  				.append('g')
			  				.attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

	var bar = dataset.filter(element => element.kabupaten == datum.kabupaten);
	xScale.domain(bar.map(function(d) { return d.tahun; }));
	yScale.domain([d3.min(bar, function(d) { return d.ipm-2.5; }),
	d3.max(bar, function(d) { return d.ipm; })]);

	// Draw x axis
	barChart.append("g")
			.attr("class", "x axis")
			.attr("transform", "translate(0," + barHeight + ")")
			.call(xAxis);

	// draw y axis
	barChart.append("g")
			.attr("class", "y axis")
			.call(yAxis);


	// draw bar chart
	barChart.selectAll(".bar")
			.data(bar)
			.enter()
			.append("rect")
			.attr("class", "bar")
			.attr("x", function(d) { return xScale(d.tahun); })
			.attr("y", function(d) { return yScale(d.ipm); })
			.attr("height", function(d) { return barHeight - yScale(d.ipm); })
			.attr("width", xScale.bandwidth())
			.attr('fill', function(d) { 
				if (d.cluster == -1) return '#000'
	    		else { return color(d.cluster); }
	    	})
			.on("mouseover", function(d) { 
				tooltip.transition(200)
					   .duration(200)
				       .style('opacity', 0.9);
				tooltip.html('tahun ' + d.tahun + '<br>' + d.ipm)
				       .style('left', (d3.event.pageX - 10) + "px")
				       .style('top', (d3.event.pageY - 65) + "px");
			})
			.on("mouseout", function(d) {
				tooltip.transition()
				       .duration(500)
				       .style('opacity', 0)
			});	

		// Add y label
		barChart.append('text')
			.attr('transform', 'rotate(-90)')
			.attr('y', 0 - (margin.left + 10))
			.attr('x', 0 - (barHeight/2))
			.attr('dy', '2em')
			.style('text-anchor', 'middle')
			.text('Nilai IPM');

		barChart.append('text')
			.attr('transform', "translate(")
			.attr('y', 0 - (margin.left + 10))
			.attr('x', 0 - (barHeight/2))
			.attr('dy', '2em')
			.style('text-anchor', 'middle')
			.text('Nilai IPM');
}

function create_legend(selection, color, dataset) {
	var cluster_legend = [];
	dataset.forEach(function(d) {
		if (cluster_legend.includes(d.cluster) == false) {
			cluster_legend.push(d.cluster);
		}
	});	

	var legend = selection.selectAll('g')
						  .data(cluster_legend.sort())
						  .enter().append('g')
						  .attr('class', 'legend')
						  .attr("transform","translate(20,30)");

	legend.append("path")
		  .attr("class", "line");

	legend.append('circle')
		  .attr('cx', 20)
		  .attr('cy', function(d, i){ return i *  20;})
		  .attr("r","0.4em")
		  .attr('width', 10)
		  .attr('height', 10)
		  .style('fill', function(d) { 
		  	if (d == -1) return '#000'
	    	else {
	    			return color(d);
	    		 }
	    	});

	legend.append('text')
		  .attr('x', 40 - 8)
		  .attr('y', function(d, i){ return (i *  20) + 9;})
		  .text(function(d){ 
		  	if (d == -1) return "Noise"
		  	return "Cluster " + d; 
		  });

	return legend
}

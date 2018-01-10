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
				l: 0,
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
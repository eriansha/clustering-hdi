function tabulate(selection, dataset, columns) {
	// render the tables: create new dict for table
	var dictTable = [];
	dataset.forEach(function(d) {
	   	dictTable.push({
	    				"kabupaten": d[0],
	    				"longitude": d[1], 
	    				"latitude": d[2],
	    				"tahun": d[3],
	    				"ipm": d[4],
	    				"cluster": d[5],
	    			});
	});

	// create a row for each object in data
	// var rows = selection.selectAll('tr')
	// 				.data(dictTable)
	// 				.enter()
	// 				.append('tr')
	// 				.html(function(d) {
	// 					"<td>" + d.kabupaten + "</td>"
	// 					"<td>" + d.longitude + "</td>"
	// 					"<td>" + d.latitude + "</td>"
	// 					"<td>" + d.tahun + "</td>"
	// 					"<td>" + d.ipm + "</td>"
	// 					"<td>" + d.cluster + "</td>"
	// 				});

	// var tbody = d3.select('#data-fill');
		// thead = table.append('thead'),
		// tbody = table.append('tbody'),
		// tfoot = table.append('tfoot');

	// // append the header row
	// thead.append('tr')
	// 	 .selectAll('th')
	// 	 .data(columns)
	// 	 .enter()
	// 	 	.append('th')
	// 	 	.text(function (column) { return column; });

	// // append the foot row
	// tfoot.append('tr')
	// 	 .selectAll('th')
	// 	 .data(columns)
	// 	 .enter()
	// 	 	.append('th')
	// 	 	.text(function (column) { return column; });

	// create a row for each object in data
	var rows = selection.selectAll('tr')
					.data(dictTable)
					.enter()
					.append('tr');

	// create a cell in each row for each column
	var cells = rows.selectAll('td')
					.data(function(row) {
							return columns.map(function (column) {
										return {column: column, value: row[column]};
									});
					})
					.enter()
					.append('td')	
					.text(function(d) { return d.value});
}
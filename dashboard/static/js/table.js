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
	var rows = selection.selectAll('tr')
					.data(dictTable)
					.enter()
					.append('tr')
					.html(function(d) {
						"<td>" + d.kabupaten + "</td>"
						"<td>" + d.longitude + "</td>"
						"<td>" + d.latitude + "</td>"
						"<td>" + d.tahun + "</td>"
						"<td>" + d.ipm + "</td>"
						"<td>" + d.cluster + "</td>"
					});
}
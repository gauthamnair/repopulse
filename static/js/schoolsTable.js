var data;
var tableSelection;
var pstuff;


var createTable = function(columnNames) {
    var table = d3.select("#schools");
    var thead = table.append("thead");
    var tbody = table.append("tbody");
    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columnNames)
        .enter()
        .append("th")
            .text(function(column) { return column; });
};



d3.json('/static/schoolsEasy.json', function(error, json) {
	data = json;
	tableSelection = d3.select('#schools');
	pstuff = tableSelection.selectAll('tr').data(data['school']);
	// pstuff.enter().append('tr').text(function (d) {
	// 	return d[0];
	// });
	pstuff.enter().append('tr').append('td').text(function (d) {
		return d['name'];
	});
});
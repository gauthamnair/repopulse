var data;
var pstuff;
var table;
var tbody;
var thead;
var rows;
var cells;

var createTable = function(columnNames) {
    table = d3.select("#schools");
    thead = table.append("thead");
    tbody = table.append("tbody");
    // append the header row
    thead.append("tr")
        .selectAll("th")
        .data(columnNames)
        .enter()
        .append("th")
            .text(function(column) { return column; });
};


var makeRows = function(rowsData){
    rows = tbody.selectAll("tr")
        .data(rowsData)
        .enter()
        .append("tr");
};

var makeLabeledDatum = function(row, columnName) {
	return {column: columnName, value: row[columnName]};
};

var Labelizer = function(row, columnNames) {
	return columnNames.map(function(columnName){
		return makeLabeledDatum(row, columnName);
	});
};

var makeCells = function() {
	rows.selectAll("td")
        .data(function(row) {
            return Labelizer(row, data.schoolColNames);
        })
        .enter()
        .append("td")
            .text(function(d) { return d.value; });
};

d3.json('/static/schoolsEasy.json', function(error, json) {
	data = json;

	createTable(data.schoolColNames);
	makeRows(data['school']);
	makeCells();
});
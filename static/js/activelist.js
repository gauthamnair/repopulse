
// #master
// #saved

var data = ['Matthew', 'Mark', 'Luke', 'John'];


var SavedRow = function(item, parentSelection) {
	var nameUI;
	var deleteUI;
	var row;

	row = parentSelection.append('tr');
	nameUI = row.append('td').text(item);
	deleteUI = row.append('td').text('delete');

	deleteUI.on('click', function() {row.remove();});
};

var ActiveRow = function(item, parentSelection, onSave) {
	var nameUI;
	var deleteUI;
	var saveUI;
	var row;

	row = parentSelection.append('tr');
	nameUI = row.append('td').text(item);
	deleteUI = row.append('td').text('delete');
	saveUI = row.append('td').text('save');

	deleteUI.on('click', function() {row.remove();});
	saveUI.on('click', function() {
		onSave(item);
		row.remove();
	});
};


var masterTable = d3.select("#master");
var savedTable = d3.select("#saved");

var onSave = function(item){
	SavedRow(item, savedTable);
};

data.forEach(function(item){
	ActiveRow(item, masterTable, onSave);
});


var data;

var urlToRepoData = function(repoString) {
	return "/api/repo/" + repoString;
};

var resultsPane = d3.select('#resultsPane');

function RepoPulseResult(repoString) {
	var publicSelf = {};
	var localSelection;
	var doOnLoadJson;
	var loadRepoData;
	var data;
	var render;
	
	doOnLoadJson = function(error, json) {
		if (error) return console.warn(error);
		data = json;
		render();
	};

	publicSelf.load = function() {
		console.log('requesting ' + repoString);
		d3.json(urlToRepoData(repoString), doOnLoadJson);
	};

	render = function(){
		localSelection = resultsPane.append('div');
		var heading = localSelection.append('h1');
		var prob = localSelection.append('h1');
		heading.text(repoString);
		prob.text(data.probAlive.toPrecision(2));
	};

	return publicSelf;
}

var submitRepoString = function() {
	var repoString = d3.select("#repoString").property('value');
	RepoPulseResult(repoString).load();
};

var d = d3.select('#resultsPane');
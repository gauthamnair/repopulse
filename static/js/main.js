var results = [];

var urlToRepoData = function(repoString) {
	return "/api/repo/" + repoString;
};

var resultsPane = d3.select('#resultsPane');

function ResultView() {
	var localSelection;
	var headingDisplay;
	var probabilityDisplay;
	var deleteButton;
	var cgraph;

	var public = {};

	var initialize = function() {
		localSelection = resultsPane.append('div');
		headingDisplay = localSelection.append('h1');
		probabilityDisplay = localSelection.append('h1');
		deleteButton = localSelection.append('button');
		deleteButton.text('clear');
		deleteButton.on('click', public.remove);
	};

	public.render = function(result) {
		if (localSelection === undefined) {
			initialize();
		}
		headingDisplay.text(result.repoString);
		if (result.data === undefined) {
			probabilityDisplay.text('...');
		} else {
			probabilityDisplay.text(result.data.probAlive.toPrecision(2));
			cgraph = CommitsGraph(localSelection, result.data['weeks']);
		}
	};

	public.remove = function() {
		if (localSelection !== undefined) {
			localSelection.remove();
		}
		localSelection = undefined;
	};

	return public;
}

function RepoPulseResult(repoString, view) {
	var public = {};
	var doOnLoadJson;
	var loadRepoData;

	public.repoString = repoString;
	
	doOnLoadJson = function(error, json) {
		if (error) return console.warn(error);
		public.data = json;
		view.render(public);
	};

	public.load = function() {
		view.render(public);
		console.log('requesting ' + repoString);
		d3.json(urlToRepoData(repoString), doOnLoadJson);
	};

	return public;
}

var submitRepoString = function() {
	var repoString = d3.select("#repoString").property('value');
	var repoResult = RepoPulseResult(repoString, ResultView());
	repoResult.load();
	results.push(repoResult);
};

d3.select("#newRepoForm").on('submit', function() {
	d3.event.preventDefault();
	submitRepoString();
	});
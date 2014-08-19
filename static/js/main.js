var results = [];

var urlToRepoData = function(repoString) {
	return "/api/repo/" + repoString;
};

var resultsPane = d3.select('#resultsPane');

function ResultView() {
	var localSelection;
	var leftSide;
	var rightSide;
	var headingDisplay;
	var probabilityDisplay;
	var deleteButton;
	var cgraph;

	var public = {};

	var prependRow = function() {
		return resultsPane.insert('tr','tr');
	};

	var initialize = function() {
		localSelection = prependRow();
		leftSide = localSelection.append('td');
		rightSide = localSelection.append('td');
		headingDisplay = rightSide.append('h1');
		probabilityDisplay = rightSide.append('h1');
		deleteButton = rightSide.append('button');
		deleteButton.text('clear');
		deleteButton.on('click', public.remove);
	};

	public.render = function(result) {
		var probabilityString;

		if (localSelection === undefined) {
			initialize();
		}
		headingDisplay.text(result.repoString);
		if (result.data === undefined) {
			probabilityDisplay.text('...');
		} else {
			probabilityString = (result.data.probAlive * 100).toFixed(1);
			probabilityString += '%';
			probabilityDisplay.text(probabilityString);
			myglobal = leftSide;
			cgraph = CommitsGraph(leftSide, result.data['weeks']);
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

var normalizeRepoString = function(repoString) {
	var cleaned = repoString.replace(/^https:\/\//, '');
	cleaned = cleaned.replace(/^github\.com\//, '');
	return cleaned;
};

var submitRepoString = function() {
	var repoString = d3.select("#repoString").property('value');
	repoString = normalizeRepoString(repoString);
	var repoResult = RepoPulseResult(repoString, ResultView());
	repoResult.load();
	results.push(repoResult);
	d3.select("#repoString").property('value', '');
	d3.select("#repoString").property('placeholder', 'enter another repo. Ex: pydata/pandas');
};

d3.select("#newRepoForm").on('submit', function() {
	d3.event.preventDefault();
	submitRepoString();
	});
var data;

var urlToRepoData = function(repoString) {
	return "/api/repo/" + repoString;
};

var doOnLoadJson = function(error, json) {
	if (error) return console.warn(error);
	data = json;
	d3.select("#repoResult").text(data.probAlive.toPrecision(2));
	console.log('success');
};

var loadRepoData = function(repoString) {
	console.log('requesting ' + repoString);
	d3.select("#repoHeading").text(repoString);
	d3.select("#repoResult").text("calculating...");
	d3.json(urlToRepoData(repoString), doOnLoadJson);

};

var submitRepoString = function() {
	var repoString = d3.select("#repoString").property('value');
	d3.select("#repoString").property('value', '');
    loadRepoData(repoString);
};
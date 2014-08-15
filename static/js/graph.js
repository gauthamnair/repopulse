var chart;

d3.json('/api/repo/torvalds/linux', function(error, json) {
	chart = CommitsGraph(d3.select('body'), json['weeks']);
});
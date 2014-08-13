d3.json('/api/repo/torvalds/linux', function(error, json) {
	CommitsGraph(d3.select('body'), json['weeks']);
});
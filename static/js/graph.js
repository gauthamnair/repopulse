
var dataset;

var w = 500;
var h = 100;
var svg;
var xScale;
var yScale;
var lines;
var aes;

var makeSVG = function() {
  svg = d3.select("body")
            .append("svg")
            .attr("width", w)
            .attr("height", h);
};


var setAesthetics = function() {
	aes = {
		'x1' : function(d) {
			return xScale(getDate(d));
		},
		'x2' : function(d) {
			return xScale(getDate(d));
		},
		'y1' : function(d) {
			return h;
		},
		'y2' : function(d) {
		return h - yScale(getCommits(d));
		// return 0;
	},
	'stroke' : 'black'
};
};

var doOnLoad = function(error, json) {
	dataset = json['weeks'];
	parseDates(dataset);
	makeSVG();
	setScales();
	setAesthetics();
	lines = svg.selectAll('line').data(dataset).enter().append('line')
		.attr(aes);
};

var getDate = function(row) {
	return row.week_start;
};

var getCommits = function(row) {
	return row.commits_num;
};

var setScales = function() {
	xScale = d3.time.scale();
	xScale.domain([d3.min(dataset, getDate), d3.max(dataset, getDate)]);
	xScale.range([0, w], 0.05);
	yScale = d3.scale.linear()
				.domain([0, d3.max(dataset, getCommits)])
				.range([0, h]);
};

formatter = d3.time.format("%Y-%m-%d");

var parseDates = function(weeks) {
	for (i=0; i < weeks.length ; i++) {
		weeks[i].week_start = formatter.parse(weeks[i].week_start);
	}
};

d3.json('/api/repo/hadley/plyr', doOnLoad);
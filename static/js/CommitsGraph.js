var CommitsGraph = function(parentSelection, dataset) {

	var w = 500;
	var h = 200;
	var svg;
	var xScale;
	var yScale;
	var lines;
	var enteringAes;
	var aes;
	var yPadding = 20;
	var leftPadding = 50;
	var rightPadding = 30;
	var xAxisMaker;
	var yAxisMaker;

	var makeSVG = function() {
		svg = d3.select("body")
		.append("svg")
		.attr("width", w)
		.attr("height", h);
	};


	var setEnteringAesthetics = function() {
		enteringAes = {
			'x1' : function(d) {
				return xScale(getDate(d));
			},
			'x2' : function(d) {
				return xScale(getDate(d));
			},
			'y1' : function(d) {
				return yScale(0);
			},
			'y2' : function(d) {
				return yScale(0);
		// return 0;
	}
};
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
			return yScale(0);
		},
		'y2' : function(d) {
			return yScale(getCommits(d));
		// return 0;
	},
	'stroke' : 'black'
};
};

var getDate = function(row) {
	return row.week_start;
};

var getCommits = function(row) {
	return row.commits_num;
};

var setScales = function() {
	xScale = d3.time.scale();
	xScale.domain([d3.min(dataset, getDate), new Date()]);
	xScale.range([leftPadding, w - rightPadding], 0.05);
	yScale = d3.scale.linear()
	.domain([0, d3.max(dataset, getCommits)])
	.range([h - yPadding, yPadding]);
};

formatter = d3.time.format("%Y-%m-%d");

var parseDates = function(weeks) {
	for (i=0; i < weeks.length ; i++) {
		weeks[i].week_start = formatter.parse(weeks[i].week_start);
	}
};

var specifyAxes = function() {
	xAxisMaker = d3.svg.axis()
	.scale(xScale)
	.orient('bottom');
	yAxisMaker = d3.svg.axis()
	.scale(yScale)
	.orient('left');
	yAxisMaker.ticks(5);
};

var drawAxes = function() {
	var translateXAxisToBottomCmd = 'translate(0,' + (h - yPadding).toString() + ')';
	var translateYAxisToLeftCmd = 'translate(' + leftPadding.toString() + ',0)';
	svg.append('g')
	.attr('class', 'axis')
	.attr('transform', translateXAxisToBottomCmd)
	.call(xAxisMaker);
	svg.append('g')
	.attr('class', 'axis')
	.attr('transform', translateYAxisToLeftCmd)
	.call(yAxisMaker);
};

var draw = function() {
	parseDates(dataset);
	makeSVG();
	setScales();
	setEnteringAesthetics();
	setAesthetics();
	specifyAxes();
	drawAxes();
	var commitsLines = svg.append('g').attr('class', 'commitsLines');
	lines = commitsLines.selectAll('line').data(dataset).enter().append('line').attr(enteringAes);
	lines.transition()
	.delay(function(d,i) {
		return i * 10;
	})
	.duration(0)
	.attr(aes);
};


draw();

};

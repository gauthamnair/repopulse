var CommitsGraph = function(parentSelection, dataset) {

	var obj = {};

	obj.parentSelection = parentSelection;
	obj.dataset = dataset;
	obj.w = 400;
	obj.h = 150;
	obj.yPadding = 20;
	obj.leftPadding = 50;
	obj.rightPadding = 20;

	obj.svgSelection = undefined;
	obj.xScale = undefined;
	obj.yScale = undefined;
	obj.lines = undefined;
	obj.enteringAes = undefined;
	obj.aes = undefined;
	obj.xAxisMaker = undefined;
	obj.yAxisMaker = undefined;

	obj.makeSVG = function() {
		obj.svgSelection = obj.parentSelection
		.append("svg")
		.attr("width", obj.w)
		.attr("height", obj.h);
	};


	obj.setEnteringAesthetics = function() {
		obj.enteringAes = {
			'x1' : function(d) {
				return obj.xScale(getDate(d));
			},
			'x2' : function(d) {
				return obj.xScale(getDate(d));
			},
			'y1' : function(d) {
				return obj.yScale(0);
			},
			'y2' : function(d) {
				return obj.yScale(0);
		// return 0;
	}
};
};

obj.setAesthetics = function() {
	obj.aes = {
		'x1' : function(d) {
			return obj.xScale(getDate(d));
		},
		'x2' : function(d) {
			return obj.xScale(getDate(d));
		},
		'y1' : function(d) {
			return obj.yScale(0);
		},
		'y2' : function(d) {
			return obj.yScale(getCommits(d));
		// return 0;
	},
	'stroke' : 'blue'
};
};

var getDate = function(row) {
	return row.week_start;
};

var getCommits = function(row) {
	return row.commits_num;
};

obj.setScales = function() {
	obj.xScale = d3.time.scale();
	obj.xScale.domain([d3.min(obj.dataset, getDate), new Date()]);
	obj.xScale.range([obj.leftPadding, obj.w - obj.rightPadding], 0.05);
	obj.yScale = d3.scale.linear()
	.domain([0, d3.max(dataset, getCommits)])
	.range([obj.h - obj.yPadding, obj.yPadding]);
};

formatter = d3.time.format("%Y-%m-%d");

var parseDates = function(weeks) {
	for (i=0; i < weeks.length ; i++) {
		weeks[i].week_start = formatter.parse(weeks[i].week_start);
	}
};

obj.specifyAxes = function() {
	obj.xAxisMaker = d3.svg.axis()
	.scale(obj.xScale)
	.orient('bottom');
	obj.yAxisMaker = d3.svg.axis()
	.scale(obj.yScale)
	.orient('left');
	obj.yAxisMaker.ticks(5);
};

obj.drawAxes = function() {
	var translateXAxisToBottomCmd = 'translate(0,' + (obj.h - obj.yPadding).toString() + ')';
	var translateYAxisToLeftCmd = 'translate(' + obj.leftPadding.toString() + ',0)';
	obj.svgSelection.append('g')
	.attr('class', 'axis')
	.attr('transform', translateXAxisToBottomCmd)
	.call(obj.xAxisMaker);
	obj.svgSelection.append('g')
	.attr('class', 'axis')
	.attr('transform', translateYAxisToLeftCmd)
	.call(obj.yAxisMaker);
};

obj.draw = function() {
	parseDates(obj.dataset);
	obj.makeSVG();
	obj.setScales();
	obj.setEnteringAesthetics();
	obj.setAesthetics();
	obj.specifyAxes();
	obj.drawAxes();
	var commitsLines = obj.svgSelection.append('g').attr('class', 'commitsLines');
	obj.lines = commitsLines.selectAll('line').data(dataset).enter().append('line').attr(obj.enteringAes);
	obj.lines.transition()
	.delay(function(d,i) {
		return i * 10;
	})
	.duration(0)
	.attr(obj.aes);
};


obj.draw();
return obj;

};

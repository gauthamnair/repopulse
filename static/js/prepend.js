
var mydiv = d3.select('#mydiv');

// var firstp = mydiv.append('p').text('first');
var firstp = mydiv.insert('p', 'p');
firstp.text('first');

var secondp = mydiv.insert('p', 'p');
secondp.text('second');
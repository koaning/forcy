var width = $width,
	height = $height;

var svg = d3.select("#$div_id").append("svg").style("width", width).style("height", height);

var color = d3.scaleOrdinal(d3.schemePastel1);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(30))
    .force("charge", d3.forceManyBody().strength(-150))
    .force("center", d3.forceCenter(width / 2, height / 2));

var graph = $data;

var link = svg.append("g")
  .attr("class", "link")
  .selectAll("line")
  .data(graph.links)
  .enter().append("line")
  .attr("stroke-width", function(d) { return 3; })
  .attr('marker-end','url(#arrowhead)');

svg.append('defs').append('marker')
    .attr("id",'arrowhead')
    .attr('viewBox','-0 -5 10 10') //the bound of the SVG viewport for the current SVG fragment. defines a coordinate system 10 wide and 10 high starting on (0,-5)
	.attr('refX', 20 - 2.5) // x coordinate for the reference point of the marker. If circle is bigger, this need to be bigger.
	.attr('refY',0)
	.attr('orient','auto')
	.attr('markerWidth',6)
	.attr('markerHeight',6)
	.attr('xoverflow','visible')
    .append('svg:path')
    .attr('d', 'M 0,-2.5 L 5 ,0 L 0,2.5')
    .attr('fill', '#999')
    .style('stroke','none');

var node = svg.append("g")
  .attr("class", "nodes")
  .selectAll("g")
  .data(graph.nodes)
  .enter()
  .append("g");

var circles = node.append("circle")
  .attr("r", 15)
  .attr("fill", function(d) { return color(d.group); })
  .attr("stroke", function(d) { return d3.color(color(d.group)).darker(); })
  .attr("stroke-width", 2)
  .call(d3.drag()
	  .on("start", dragstarted)
	  .on("drag", dragged)
	  .on("end", dragended));

var labels = node.append("text")
  .text(function(d) {
	return d.name;
  })
  .attr("text-anchor", "middle")
  .attr("dy", ".35em");

simulation.nodes(graph.nodes).on("tick", ticked);
simulation.force("link").links(graph.links);

function ticked() {
	link
		.attr("x1", function(d) { return d.source.x; })
		.attr("y1", function(d) { return d.source.y; })
		.attr("x2", function(d) { return d.target.x; })
		.attr("y2", function(d) { return d.target.y; });

	node
		.attr("transform", function(d) {
		  return "translate(" + d.x + "," + d.y + ")";
		})
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
  d3.select(this).classed("fixed", d.fixed = true);
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

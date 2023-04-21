import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const ForceDirectedGraph = () => {
  const svgRef = useRef();

  useEffect(() => {
    // Fetch the JSON data from the file
    d3.json('./graph_data.json').then((graph) => {
      const width = 800;
      const height = 600;

      // Create an SVG element to display the graph
      const svg = d3.select(svgRef.current)
        .attr('width', width)
        .attr('height', height);

      // Create the simulation with forces
      const simulation = d3.forceSimulation(graph.nodes)
        .force('link', d3.forceLink(graph.links).id((d) => d.id).distance(100))
        .force('charge', d3.forceManyBody().strength(-200))
        .force('center', d3.forceCenter(width / 2, height / 2));

      // Draw the links (edges)
      const link = svg.append('g')
        .attr('class', 'link')
        .selectAll('line')
        .data(graph.links)
        .join('line');

      // Draw the nodes
      const node = svg.append('g')
        .attr('class', 'node')
        .selectAll('circle')
        .data(graph.nodes)
        .join('circle')
        .attr('r', 8)
        .call(drag(simulation));

      // Add labels to the nodes
      const label = svg.append('g')
        .attr('class', 'label')
        .selectAll('text')
        .data(graph.nodes)
        .join('text')
        .text((d) => d.id)
        .attr('dx', 12)
        .attr('dy', 4);

      // Update the positions of the nodes and links during the simulation
      simulation.on('tick', () => {
        link.attr('x1', (d) => d.source.x)
          .attr('y1', (d) => d.source.y)
          .attr('x2', (d) => d.target.x)
          .attr('y2', (d) => d.target.y);

        node.attr('cx', (d) => d.x)
          .attr('cy', (d) => d.y);

        label.attr('x', (d) => d.x)
          .attr('y', (d) => d.y);
      });

      // Drag behavior for nodes
      function drag(simulation) {
        const dragstarted = (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        };
        const dragged = (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        };
        const dragended = (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        };
        return d3.drag()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended);
      }
    });
  }, []);

  return <svg ref={svgRef}></svg>;
};

export default ForceDirectedGraph;

function createMindMap(containerId, data, lang) {
    d3.select(`#${containerId}`).select("svg").remove();

    const width = 350;
    const height = 350;
    const radius = Math.min(width, height) / 2 - 40;

    const svg = d3.select(`#${containerId}`)
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMidYMid meet")
        .style("width", "100%")
        .style("height", "100%")
        .append("g")
        .attr("transform", `translate(${width / 2},${height / 2})`);

    // Main node
    svg.append("circle")
        .attr("r", 25)
        .style("fill", "#6C63FF");

    svg.append("text")
        .text("Main Idea")
        .attr("text-anchor", "middle")
        .attr("dy", 5)
        .style("fill", "#fff")
        .style("font-size", "12px")
        .style("font-weight", "bold");

    // Spread points around
    const angleStep = (2 * Math.PI) / data.length;

    data.forEach((point, i) => {
        const angle = i * angleStep;
        const x = Math.cos(angle) * radius;
        const y = Math.sin(angle) * radius;

        // Connector
        svg.append("line")
            .attr("x1", 0).attr("y1", 0)
            .attr("x2", x).attr("y2", y)
            .style("stroke", "#aaa")
            .style("stroke-width", 1);

        // Child node
        svg.append("circle")
            .attr("cx", x)
            .attr("cy", y)
            .attr("r", 15)
            .style("fill", "#FF6584");

        // Text
        svg.append("text")
            .text(point)
            .attr("x", x + (x > 0 ? 10 : -10))
            .attr("y", y)
            .attr("dy", ".35em")
            .attr("text-anchor", x > 0 ? "start" : "end")
            .style("font-size", "10px")
            .style("fill", "#333")
            .call(wrapText, 90);
    });

    function wrapText(text, width) {
        text.each(function () {
            const text = d3.select(this),
                words = text.text().split(/\s+/).reverse(),
                lineHeight = 1.1,
                y = text.attr("y"),
                dy = parseFloat(text.attr("dy"));

            let line = [],
                lineNumber = 0,
                tspan = text.text(null)
                    .append("tspan")
                    .attr("x", text.attr("x"))
                    .attr("y", y)
                    .attr("dy", dy + "em");

            let word;
            while (word = words.pop()) {
                line.push(word);
                tspan.text(line.join(" "));
                if (tspan.node().getComputedTextLength() > width) {
                    line.pop();
                    tspan.text(line.join(" "));
                    line = [word];
                    tspan = text.append("tspan")
                        .attr("x", text.attr("x"))
                        .attr("y", y)
                        .attr("dy", ++lineNumber * lineHeight + dy + "em")
                        .text(word);
                }
            }
        });
    }
}

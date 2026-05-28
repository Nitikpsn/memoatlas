var AtlasGraph = {
    buildNetwork: function(containerId, data, userOptions) {
        var container = document.getElementById(containerId);
        if (!container) {
            return null;
        }

        var options = {
            nodes: {
                shape: 'dot',
                size: 16,
                color: { background: '#10b981', border: '#10b981' },
                font: { color: '#a0a0b8', size: 11, face: 'Space Mono' },
                borderWidth: 0,
                scaling: { label: { enabled: false } }
            },
            edges: {
                color: { color: 'rgba(16,185,129,0.2)', highlight: 'rgba(16,185,129,0.4)' },
                smooth: { type: 'cubicBezier', roundness: 0.4 },
                width: 1.2
            },
            physics: {
                enabled: true,
                solver: 'barnesHut',
                barnesHut: {
                    gravitationalConstant: -3000,
                    springLength: 200,
                    springConstant: 0.03
                },
                stabilization: { iterations: 150 }
            },
            interaction: { hover: true }
        };

        if (userOptions) {
            for (var key in userOptions) {
                if (userOptions.hasOwnProperty(key)) {
                    options[key] = userOptions[key];
                }
            }
        }

        var nodesArray = [];
        for (var i = 0; i < data.nodes.length; i++) {
            var n = data.nodes[i];
            nodesArray.push({
                id: n.id,
                label: n.title,
                updated_at: n.updated_at,
                size: Math.max(10, 20 - i * 0.5)
            });
        }
        var nodes = new vis.DataSet(nodesArray);

        var edgesArray = [];
        for (var j = 0; j < data.links.length; j++) {
            var l = data.links[j];
            edgesArray.push({
                from: l.from || l.source,
                to: l.to || l.target,
                smooth: {
                    type: 'cubicBezier',
                    roundness: 0.2 + Math.random() * 0.3
                }
            });
        }
        var edges = new vis.DataSet(edgesArray);

        var network = new vis.Network(container, { nodes: nodes, edges: edges }, options);

        return {
            network: network,
            nodes: nodes,
            edges: edges,
            rawData: data
        };
    }
};

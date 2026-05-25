const AtlasGraph = (function() {

  function init(containerId, options) {
    const container = document.getElementById(containerId);
    if (!container) return null;

    const defaults = {
      nodes: {
        shape: 'dot',
        size: 16,
        color: { background: '#EF4444', border: '#EF4444' },
        font: { color: '#cccccc', size: 11, face: 'Pixelify Sans' },
        borderWidth: 0,
        scaling: { label: { enabled: false } }
      },
      edges: {
        color: { color: 'rgba(239,68,68,0.25)', highlight: 'rgba(239,68,68,0.5)' },
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

    const merged = deepMerge(defaults, options || {});
    return { container, options: merged };
  }

  function deepMerge(a, b) {
    const result = {};
    for (const k in a) {
      if (b && k in b) {
        result[k] = (typeof a[k] === 'object' && !Array.isArray(a[k]))
          ? deepMerge(a[k], b[k]) : b[k];
      } else {
        result[k] = a[k];
      }
    }
    for (const k in b) {
      if (!(k in a)) result[k] = b[k];
    }
    return result;
  }

  function buildNetwork(containerId, data, userOptions) {
    const config = init(containerId, userOptions);
    if (!config) return null;

    const nodes = new vis.DataSet(
      (data.nodes || []).map(function(n, i) {
        return {
          id: n.id,
          label: n.title,
          updated_at: n.updated_at,
          size: Math.max(10, 20 - i * 0.5)
        };
      })
    );

    const edges = new vis.DataSet(
      (data.links || []).map(function(l) {
        return {
          from: l.from || l.source,
          to: l.to || l.target,
          smooth: {
            type: 'cubicBezier',
            roundness: 0.2 + Math.random() * 0.3
          }
        };
      })
    );

    const network = new vis.Network(config.container, { nodes, edges }, config.options);

    return { network, nodes, edges, rawData: data };
  }

  return {
    init,
    buildNetwork
  };

})();

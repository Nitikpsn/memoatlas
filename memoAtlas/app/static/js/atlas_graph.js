/**
 * AtlasGraph — dedicated module for root node graph logic.
 * Keeps graph rendering cleanly separated from UI interactions.
 */
const AtlasGraph = (function() {

  function init(containerId, options) {
    const container = document.getElementById(containerId);
    if (!container) return null;

    const defaults = {
      nodes: {
        shape: 'dot',
        size: 14,
        color: { background: '#555555', border: '#555555' },
        font: { color: '#888888', size: 11 },
        borderWidth: 0,
        scaling: { label: { enabled: false } }
      },
      edges: {
        color: { color: '#333333' },
        smooth: { type: 'continuous' }
      },
      physics: {
        enabled: true,
        solver: 'barnesHut',
        barnesHut: {
          gravitationalConstant: -2000,
          springLength: 250,
          springConstant: 0.04
        },
        stabilization: { iterations: 100 }
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
      (data.nodes || []).map(n => ({
        id: n.id,
        label: n.title,
        updated_at: n.updated_at
      }))
    );
    const edges = new vis.DataSet(data.links || []);
    const network = new vis.Network(config.container, { nodes, edges }, config.options);

    return { network, nodes, edges, rawData: data };
  }

  return {
    init,
    buildNetwork
  };

})();

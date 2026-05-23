let network, nodes, graphData;
let pulseActive = false;
let pulseInterval = null;
let nodePulseData = [];

const pulseBtn = document.getElementById('pulse-btn');

fetch('/api/graph-data')
  .then(r => r.json())
  .then(data => {
    graphData = data;
    nodes = new vis.DataSet(data.nodes.map(n => ({
      id: n.id,
      label: n.title,
      updated_at: n.updated_at
    })));
    const edges = new vis.DataSet(data.links);

    const container = document.getElementById('mynetwork');
    const networkData = { nodes, edges };
    const options = {
      nodes: {
        shape: 'dot',
        size: 16,
        color: { background: '#8B5CF6', border: '#8B5CF6' },
        font: { color: 'rgba(255,255,255,0.5)', size: 12 },
        borderWidth: 0,
        scaling: { label: { enabled: false } }
      },
      edges: {
        color: { color: 'rgba(139,92,246,0.15)', highlight: 'rgba(139,92,246,0.3)' },
        smooth: { type: 'continuous' }
      },
      physics: {
        enabled: true,
        solver: 'barnesHut',
        barnesHut: { gravitationalConstant: -2000, springLength: 250, springConstant: 0.04 },
        stabilization: { iterations: 100 }
      },
      interaction: { hover: true }
    };

    network = new vis.Network(container, networkData, options);

    network.on('click', function(params) {
      if (params.nodes.length > 0) {
        window.location.href = '/note/' + params.nodes[0];
      }
    });

    preparePulseData(data.nodes);
  })
  .catch(() => {});

function preparePulseData(nodesData) {
  const now = Date.now();
  nodePulseData = nodesData.map(n => {
    const updatedAt = n.updated_at ? new Date(n.updated_at).getTime() : now;
    const diffHours = (now - updatedAt) / (1000 * 60 * 60);
    let speed;
    if (diffHours < 1) speed = 5 + Math.random() * 1;
    else if (diffHours < 24) speed = 3 + Math.random() * 0.5;
    else if (diffHours < 168) speed = 1.5 + Math.random() * 0.3;
    else speed = 0.5 + Math.random() * 0.3;
    return { id: n.id, speed, baseSize: 16 + Math.random() * 2 };
  });
}

if (pulseBtn) {
  pulseBtn.addEventListener('click', function() {
    pulseActive = !pulseActive;
    this.classList.toggle('active');
    if (pulseActive) {
      pulseBtn.innerHTML = '<span class="pulse-indicator" style="animation:pulse-dot 1.2s ease-in-out infinite;"></span> Pulsing';
      startPulse();
    } else {
      pulseBtn.innerHTML = '<span class="pulse-indicator"></span> Pulse';
      stopPulse();
    }
  });
}

function startPulse() {
  if (!network || !nodes) return;
  let time = 0;
  pulseInterval = setInterval(() => {
    time += 0.04;
    const updates = nodePulseData.map(n => {
      const oscillation = Math.sin(time * n.speed) * 5;
      return { id: n.id, size: Math.max(3, n.baseSize + oscillation) };
    });
    nodes.update(updates);
  }, 40);
}

function stopPulse() {
  if (pulseInterval) {
    clearInterval(pulseInterval);
    pulseInterval = null;
  }
  if (nodes) {
    const reset = nodePulseData.map(n => ({ id: n.id, size: 16 }));
    nodes.update(reset);
  }
}

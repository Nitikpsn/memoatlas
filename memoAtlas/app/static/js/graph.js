let network, nodes, graphData;
let pulseActive = false;
let pulseInterval = null;
let nodePulseData = [];

const pulseBtn = document.getElementById('pulse-btn');

fetch('/api/graph-data')
  .then(r => r.json())
  .then(data => {
    graphData = data;

    const result = AtlasGraph.buildNetwork('mynetwork', data, {
      nodes: {
        size: 16,
        color: { background: '#555555', border: '#555555' },
        font: { color: '#888888', size: 12 }
      },
      edges: {
        color: { color: '#333333' }
      },
      physics: {
        barnesHut: { gravitationalConstant: -2000, springLength: 250, springConstant: 0.04 }
      }
    });

    if (!result) return;
    network = result.network;
    nodes = result.nodes;

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
    if (diffHours < 1) speed = 5 + Math.random();
    else if (diffHours < 24) speed = 3 + Math.random() * 0.5;
    else if (diffHours < 168) speed = 1.5 + Math.random() * 0.3;
    else speed = 0.5 + Math.random() * 0.3;
    return { id: n.id, speed, baseSize: 16 };
  });
}

if (pulseBtn) {
  pulseBtn.addEventListener('click', function() {
    pulseActive = !pulseActive;
    this.classList.toggle('active');
    const indicator = this.querySelector('.pulse-indicator');
    if (pulseActive) {
      indicator.style.animation = 'pulse-dot 1s ease-in-out infinite';
      startPulse();
    } else {
      indicator.style.animation = '';
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

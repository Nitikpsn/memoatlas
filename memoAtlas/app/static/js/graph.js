var network;
var nodes;
var graphData;
var pulseActive = false;
var pulseInterval = null;
var nodePulseData = [];

var pulseBtn = document.getElementById('pulse-btn');

fetch('/api/graph-data')
    .then(function(r) { return r.json(); })
    .then(function(data) {
        graphData = data;

        var result = AtlasGraph.buildNetwork('mynetwork', data, {
            nodes: {
                size: 16,
                color: { background: '#2a2a42', border: '#2a2a42' },
                font: { color: '#6b6b82', size: 12 }
            },
            edges: {
                color: { color: '#1e1e32' }
            },
            physics: {
                barnesHut: { gravitationalConstant: -2000, springLength: 250, springConstant: 0.04 }
            }
        });

        if (!result) {
            return;
        }

        network = result.network;
        nodes = result.nodes;

        network.on('click', function(params) {
            if (params.nodes.length > 0) {
                window.location.href = '/note/' + params.nodes[0];
            }
        });

        preparePulseData(data.nodes);
    })
    .catch(function() {
    });

function preparePulseData(nodesData) {
    var now = Date.now();
    nodePulseData = [];

    for (var i = 0; i < nodesData.length; i++) {
        var n = nodesData[i];
        var updatedAt = n.updated_at ? new Date(n.updated_at).getTime() : now;
        var diffHours = (now - updatedAt) / (1000 * 60 * 60);
        var speed;

        if (diffHours < 1) {
            speed = 5 + Math.random();
        } else if (diffHours < 24) {
            speed = 3 + Math.random() * 0.5;
        } else if (diffHours < 168) {
            speed = 1.5 + Math.random() * 0.3;
        } else {
            speed = 0.5 + Math.random() * 0.3;
        }

        nodePulseData.push({
            id: n.id,
            speed: speed,
            baseSize: 16
        });
    }
}

if (pulseBtn) {
    pulseBtn.addEventListener('click', function() {
        pulseActive = !pulseActive;
        this.classList.toggle('active');
        if (pulseActive) {
            startPulse();
        } else {
            stopPulse();
        }
    });
}

function startPulse() {
    if (!network || !nodes) {
        return;
    }

    var time = 0;
    pulseInterval = setInterval(function() {
        time += 0.04;
        var updates = [];

        for (var i = 0; i < nodePulseData.length; i++) {
            var n = nodePulseData[i];
            var oscillation = Math.sin(time * n.speed) * 5;
            updates.push({
                id: n.id,
                size: Math.max(3, n.baseSize + oscillation)
            });
        }

        nodes.update(updates);
    }, 40);
}

function stopPulse() {
    if (pulseInterval) {
        clearInterval(pulseInterval);
        pulseInterval = null;
    }

    if (nodes) {
        var reset = [];
        for (var i = 0; i < nodePulseData.length; i++) {
            reset.push({ id: nodePulseData[i].id, size: 16 });
        }
        nodes.update(reset);
    }
}

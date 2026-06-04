document.addEventListener('DOMContentLoaded', function() {
  var container = document.getElementById('network')
  if (!container) return

  var pulseBtn = document.getElementById('pulse-btn')
  var network = null
  var nodes = null
  var pulseInterval = null
  var pulseActive = false

  fetch('/api/graph-data')
    .then(function(r) { return r.json() })
    .then(function(data) {
      if (!data.nodes.length) return

      var nodeArray = data.nodes.map(function(n) {
        var size = 16
        if (n.stage === 'ancient') size = 24
        else if (n.stage === 'mature') size = 20
        else if (n.stage === 'seed' || n.stage === 'dead') size = 12
        return { id: n.id, label: n.title, size: size, updated_at: n.updated_at }
      })

      var edgeArray = data.links.map(function(l) {
        return { from: l.source, to: l.target }
      })

      nodes = new vis.DataSet(nodeArray)
      var edges = new vis.DataSet(edgeArray)

      var options = {
        nodes: {
          shape: 'dot',
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
          solver: 'barnesHut',
          barnesHut: {
            gravitationalConstant: -3000,
            springLength: 200,
            springConstant: 0.03
          },
          stabilization: { iterations: 150 }
        },
        interaction: { hover: true }
      }
      

      network = new vis.Network(container, { nodes: nodes, edges: edges }, options)

      network.on('click', function(params) {
        if (params.nodes.length > 0) {
          window.location.href = '/tree/' + params.nodes[0]
        }
      })

      if (pulseBtn) {
        pulseBtn.addEventListener('click', function() {
          pulseActive = !pulseActive
          this.classList.toggle('active')
          if (pulseActive) startPulse(data.nodes)
          else stopPulse()
        })
      }
    })

  function startPulse(nodesData) {
    if (!network || !nodes) return
    var now = Date.now()
    var speeds = nodesData.map(function(n) {
      var t = n.updated_at ? new Date(n.updated_at).getTime() : now
      var diff = (now - t) / (1000 * 60 * 60)
      var speed = 0.5
      if (diff < 1) speed = 5 + Math.random()
      else if (diff < 24) speed = 3 + Math.random() * 0.5
      else speed = 1.5 + Math.random() * 0.3
      return { id: n.id, speed: speed }
    })
    var time = 0
    pulseInterval = setInterval(function() {
      time += 0.04
      var updates = speeds.map(function(s) {
        var size = 16 + Math.sin(time * s.speed) * 5
        return { id: s.id, size: Math.max(3, size) }
      })
      nodes.update(updates)
    }, 40)
  }

  function stopPulse() {
    if (pulseInterval) {
      clearInterval(pulseInterval)
      pulseInterval = null
    }
    if (nodes) {
      var reset = nodes.get().map(function(n) {
        var size = 16
        return { id: n.id, size: size }
      })
      nodes.update(reset)
    }
  }
})

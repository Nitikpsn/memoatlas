document.addEventListener('DOMContentLoaded', function() {
  var timer = document.getElementById('timer')
  var btn = document.getElementById('start-revise')
  var visual = document.getElementById('tree-visual')
  var healthLabel = document.querySelector('.focus-health')
  var timeLeft = 300
  var interval = null

  if (!btn) return

  btn.addEventListener('click', function() {
    btn.classList.add('hidden')
    btn.style.display = 'none'
    interval = setInterval(function() {
      timeLeft--
      var m = Math.floor(timeLeft / 60)
      var s = timeLeft % 60
      timer.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0')
      timer.style.opacity = (timeLeft % 2 === 0) ? '0.7' : '1'
      if (timeLeft <= 0) {
        clearInterval(interval)
        timer.textContent = 'DONE'
        finish()
      }
    }, 1000)
  })

  function finish() {
    var overlay = document.createElement('div')
    overlay.className = 'flash-overlay'
    document.body.appendChild(overlay)

    fetch('/revise/' + treeId, { method: 'POST' })
      .then(function(r) { return r.json() })
      .then(function(data) {
        if (data.success) {
          setTimeout(function() { overlay.remove() }, 500)
          updateTree(data.new_health)
        }
      })
  }

  function updateTree(health) {
    var cls = 'tree-display '
    if (health <= 20) cls += 'seed-tree'
    else if (health <= 40) cls += 'sprout-tree'
    else if (health <= 70) cls += 'young-tree'
    else if (health <= 90) cls += 'mature-tree'
    else cls += 'ancient-tree'

    visual.className = cls
    healthLabel.textContent = 'HEALTH ' + health + '/100'
  }
})

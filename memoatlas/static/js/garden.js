document.addEventListener('DOMContentLoaded', function() {
  var timer = document.getElementById('timer')
  var btn = document.getElementById('start-revise')
  var hpFill = document.getElementById('hp-fill')
  var hpLabel = document.getElementById('hp-label')
  var heartIcon = document.querySelector('.heart')
  var timeLeft = 300
  var interval = null
  var csrfToken = document.querySelector('meta[name="csrf-token"]')

  if (!btn) return

  btn.addEventListener('click', function() {
    btn.classList.add('hidden')
    btn.style.display = 'none'
    interval = setInterval(function() {
      timeLeft--
      var m = Math.floor(timeLeft / 60)
      var s = timeLeft % 60
      timer.textContent = String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0')
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

    var headers = { 'Content-Type': 'application/json' }
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken.getAttribute('content')
    }

    fetch('/revise/' + treeId, { method: 'POST', headers: headers })
      .then(function(r) { return r.json() })
      .then(function(data) {
        if (data.success) {
          setTimeout(function() { overlay.remove() }, 500)
          updateHp(data.new_health)
        }
      })
      .catch(function() {
        overlay.remove()
        timer.textContent = 'ERROR'
      })
  }

  function updateHp(health) {
    hpFill.style.width = health + '%'
    hpLabel.textContent = health + '/100 HP'
  }
})
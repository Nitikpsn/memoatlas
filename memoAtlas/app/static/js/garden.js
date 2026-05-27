document.addEventListener('DOMContentLoaded', () => {
  const timerDisplay = document.getElementById('timer-display')
  const startBtn = document.getElementById('start-btn')
  const plant = document.getElementById('plant')
  let timeLeft = 300
  let timerId = null

  updatePlantVisuals(parseInt(plant.dataset.health))

  startBtn.addEventListener('click', () => {
    startBtn.classList.add('hidden')
    timerId = setInterval(() => {
      timeLeft--
      const minutes = Math.floor(timeLeft / 60)
      const seconds = timeLeft % 60
      timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
      timerDisplay.style.opacity = (timeLeft % 2 === 0) ? '0.7' : '1'
      if (timeLeft <= 0) {
        clearInterval(timerId)
        timerDisplay.textContent = 'DONE'
        finishRevision()
      }
    }, 1000)
  })

  function finishRevision() {
    const overlay = document.createElement('div')
    overlay.className = 'flash-overlay'
    document.body.appendChild(overlay)
    fetch(`/revise/${currentNoteId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    })
      .then(r => r.json())
      .then(data => {
        if (data.success) {
          setTimeout(() => overlay.remove(), 300)
          updatePlantVisuals(data.new_health)
        }
      })
  }

  function updatePlantVisuals(health) {
    if (health < 30) {
      plant.className = 'retro-tree stage-seed'
    } else if (health < 70) {
      plant.className = 'retro-tree stage-sprout'
    } else {
      plant.className = 'retro-tree stage-full'
    }
    plant.classList.add('grow-anim')
    setTimeout(() => plant.classList.remove('grow-anim'), 1000)
  }
})

(function() {
  const map = document.getElementById('gameMap');
  const radar = document.getElementById('radarSweep');
  const scanStatus = document.getElementById('scanStatus');
  const hudCoords = document.getElementById('hudCoords');
  if (!map) return;

  /* ---- beacon pulse ---- */
  const beacons = document.querySelectorAll('.map-beacon');
  beacons.forEach(function(b) {
    const ring = b.querySelector('.beacon-ring');
    if (ring) {
      setInterval(function() {
        ring.style.transform = 'scale(2)';
        ring.style.opacity = '0';
        setTimeout(function() {
          ring.style.transform = 'scale(1)';
          ring.style.opacity = '0.6';
        }, 600);
      }, 2000 + parseFloat(b.style.getPropertyValue('--delay') || 0) * 1000);
    }
  });

  /* ---- radar sweep ---- */
  let radarAngle = 0;
  let radarOn = true;
  setInterval(function() {
    if (!radarOn) return;
    radarAngle = (radarAngle + 1) % 360;
    radar.style.transform = 'rotate(' + radarAngle + 'deg)';
  }, 30);

  /* ---- fake buttons ---- */
  function fakeClick(btn, label, duration) {
    btn.classList.add('active');
    if (scanStatus) scanStatus.textContent = label;
    setTimeout(function() {
      btn.classList.remove('active');
      if (scanStatus && label !== 'SCANNING') scanStatus.textContent = 'SCANNING';
    }, duration || 1200);
  }

  document.getElementById('btnScan').addEventListener('click', function() {
    fakeClick(this, 'SCANNING', 800);
  });

  document.getElementById('btnPulse').addEventListener('click', function() {
    fakeClick(this, 'PULSING', 1000);
    beacons.forEach(function(b) {
      b.style.transform = 'scale(1.15)';
      setTimeout(function() { b.style.transform = ''; }, 400);
    });
  });

  document.getElementById('btnRadar').addEventListener('click', function() {
    fakeClick(this, 'RADAR SWEEP', 1500);
    if (radar) {
      radarOn = !radarOn;
      radar.style.display = radarOn ? 'block' : 'none';
    }
  });

  document.getElementById('btnCompass').addEventListener('click', function() {
    fakeClick(this, 'CALIBRATING', 900);
    var rose = document.querySelector('.compass-rose');
    if (rose) {
      rose.style.transform = 'rotate(360deg)';
      rose.style.transition = 'transform 0.6s ease';
      setTimeout(function() { rose.style.transform = ''; }, 700);
    }
  });

  /* ---- mouse tracking for HUD coords ---- */
  map.addEventListener('mousemove', function(e) {
    var rect = map.getBoundingClientRect();
    var x = Math.round((e.clientX - rect.left) / rect.width * 100);
    var y = Math.round((e.clientY - rect.top) / rect.height * 100);
    if (hudCoords) hudCoords.textContent = x + ', ' + y;
  });

})();

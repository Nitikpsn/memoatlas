(function() {
  var map = document.getElementById('gameMap');
  var radar = document.getElementById('radarSweep');
  if (!map) return;

  /* beacon ring pulse */
  var beacons = document.querySelectorAll('.map-beacon');
  beacons.forEach(function(b) {
    var ring = b.querySelector('.beacon-ring');
    if (!ring) return;
    var delay = parseFloat(b.style.getPropertyValue('--delay')) * 1000 || 0;
    setInterval(function() {
      ring.style.transform = 'scale(2.5)';
      ring.style.opacity = '0';
      setTimeout(function() {
        ring.style.transform = 'scale(1)';
        ring.style.opacity = '0.5';
      }, 700);
    }, 2200 + delay);
  });

  /* radar sweep */
  var angle = 0;
  setInterval(function() {
    angle = (angle + 1.5) % 360;
    radar.style.transform = 'rotate(' + angle + 'deg)';
  }, 25);
})();

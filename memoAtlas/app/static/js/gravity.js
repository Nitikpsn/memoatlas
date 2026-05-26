/*
 * gravity.js - the "focus tunnel" that shows similar notes
 * when you hover over a note, it pulls in related notes by tag matching
 */

function FocusTunnel(tunnelId, itemsId) {
    this.tunnelElement = document.getElementById(tunnelId);
    this.itemsElement = document.getElementById(itemsId);
    this.currentFocusId = null;
    this.isGameMap = document.getElementById('mapCanvas') !== null;
}

FocusTunnel.prototype.zoomToCluster = function(noteId) {
    var self = this;
    self.currentFocusId = noteId;
    self.tunnelElement.classList.add('pull-animation');

    // fetch similar notes
    fetch('/api/gravity/' + noteId)
        .then(function(res) { return res.json(); })
        .then(function(neighbors) {
            self.renderNeighbors(neighbors.slice(0, 3));
        })
        .catch(function() {});

    // remove animation after it plays
    setTimeout(function() {
        self.tunnelElement.classList.remove('pull-animation');
    }, 400);
};

FocusTunnel.prototype.renderNeighbors = function(notes) {
    var self = this;
    if (!self.itemsElement) {
        return;
    }

    if (notes.length === 0) {
        self.itemsElement.innerHTML = '<div class="tunnel-node dim"><span class="pixel-prefix">>></span> no gravity pull...</div>';
        return;
    }

    var html = '';
    for (var i = 0; i < notes.length; i++) {
        var n = notes[i];
        var pct = Math.round((n.proximityScore || 0) * 100);
        var linkBtn = '';

        if (self.isGameMap && self.currentFocusId) {
            linkBtn = '<button class="link-btn" data-target-id="' + n.id + '">LINK</button>';
        }

        html += '<div class="tunnel-node entering">' +
                    '<span class="pixel-prefix">>></span> ' +
                    '<span class="node-title">' + n.title + '</span>' +
                    linkBtn +
                    '<div class="gravity-meter"><div class="gravity-meter-fill" style="width:' + pct + '%"></div></div>' +
                '</div>';
    }

    self.itemsElement.innerHTML = html;

    // add link button handlers for the game map
    if (self.isGameMap) {
        var linkButtons = self.itemsElement.querySelectorAll('.link-btn');
        for (var j = 0; j < linkButtons.length; j++) {
            (function(btn) {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    var targetId = parseInt(btn.getAttribute('data-target-id'));
                    if (window.mapInstance) {
                        window.mapInstance.createLink(targetId);
                    }
                });
            })(linkButtons[j]);
        }
    }

    // remove the entering class after animation
    requestAnimationFrame(function() {
        var entering = document.querySelectorAll('.tunnel-node.entering');
        for (var k = 0; k < entering.length; k++) {
            entering[k].classList.remove('entering');
        }
    });
};

FocusTunnel.prototype.renderNeighborsWithLink = function(sourceId, targetId) {
    if (!this.itemsElement) {
        return;
    }

    var items = this.itemsElement.querySelectorAll('.tunnel-node');
    for (var i = 0; i < items.length; i++) {
        var btn = items[i].querySelector('.link-btn');
        if (btn) {
            var btnTargetId = parseInt(btn.getAttribute('data-target-id'));
            if (btnTargetId === targetId) {
                btn.disabled = true;
                btn.textContent = 'LINKED';
                btn.style.borderColor = 'rgba(239,68,68,0.6)';
                btn.style.color = 'rgba(239,68,68,0.6)';
            }
        }
    }
};

class FocusTunnel {
    constructor(tunnelId, itemsId) {
        this.tunnelElement = document.getElementById(tunnelId);
        this.itemsElement = document.getElementById(itemsId);
        this.currentFocusId = null;
        this.isGameMap = document.getElementById('mapCanvas') !== null;
    }

    async zoomToCluster(noteId) {
        this.currentFocusId = noteId;
        this.tunnelElement.classList.add('pull-animation');
        try {
            const res = await fetch('/api/gravity/' + noteId);
            const neighbors = await res.json();
            this.renderNeighbors(neighbors.slice(0, 3));
        } catch (_) {}
        setTimeout(() => this.tunnelElement.classList.remove('pull-animation'), 400);
    }

    renderNeighbors(notes) {
        if (!this.itemsElement) return;
        if (notes.length === 0) {
            this.itemsElement.innerHTML =
                '<div class="tunnel-node dim"><span class="pixel-prefix">>></span> no gravity pull...</div>';
            return;
        }
        this.itemsElement.innerHTML = notes.map(function(n) {
            var pct = Math.round((n.proximityScore || 0) * 100);
            var linkBtn = '';
            if (this.isGameMap && this.currentFocusId) {
                linkBtn = '<button class="link-btn" data-target-id="' + n.id + '">LINK</button>';
            }
            return (
                '<div class="tunnel-node entering">' +
                    '<span class="pixel-prefix">>></span> ' +
                    '<span class="node-title">' + n.title + '</span>' +
                    linkBtn +
                    '<div class="gravity-meter"><div class="gravity-meter-fill" style="width:' + pct + '%"></div></div>' +
                '</div>'
            );
        }.bind(this)).join('');

        if (this.isGameMap) {
            this.itemsElement.querySelectorAll('.link-btn').forEach(function(btn) {
                btn.addEventListener('click', function(e) {
                    e.stopPropagation();
                    var targetId = parseInt(btn.getAttribute('data-target-id'));
                    if (window.mapInstance) {
                        window.mapInstance.createLink(targetId);
                    }
                });
            });
        }

        requestAnimationFrame(function() {
            document.querySelectorAll('.tunnel-node.entering').forEach(function(el) {
                el.classList.remove('entering');
            });
        });
    }

    renderNeighborsWithLink(sourceId, targetId) {
        if (!this.itemsElement) return;
        var allItems = this.itemsElement.querySelectorAll('.tunnel-node');
        allItems.forEach(function(item) {
            var btn = item.querySelector('.link-btn');
            if (btn) {
                var btnTargetId = parseInt(btn.getAttribute('data-target-id'));
                if (btnTargetId === targetId) {
                    btn.disabled = true;
                    btn.textContent = 'LINKED';
                    btn.style.borderColor = 'rgba(239,68,68,0.6)';
                    btn.style.color = 'rgba(239,68,68,0.6)';
                }
            }
        });
    }
}

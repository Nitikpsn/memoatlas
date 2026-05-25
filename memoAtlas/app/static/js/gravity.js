class FocusTunnel {
    constructor(tunnelId, itemsId) {
        this.tunnelElement = document.getElementById(tunnelId);
        this.itemsElement = document.getElementById(itemsId);
        this.currentFocusId = null;
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
            return (
                '<div class="tunnel-node entering">' +
                    '<span class="pixel-prefix">>></span> ' +
                    '<span class="node-title">' + n.title + '</span>' +
                    '<div class="gravity-meter"><div class="gravity-meter-fill" style="width:' + pct + '%"></div></div>' +
                '</div>'
            );
        }).join('');
        requestAnimationFrame(function() {
            document.querySelectorAll('.tunnel-node.entering').forEach(function(el) {
                el.classList.remove('entering');
            });
        });
    }
}

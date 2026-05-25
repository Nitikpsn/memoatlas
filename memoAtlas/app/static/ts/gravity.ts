interface GravityNode {
    id: string;
    title: string;
    proximityScore: number;
    tags: string[];
}

class FocusTunnel {
    private tunnelElement: HTMLElement;
    private itemsElement: HTMLElement;
    public currentFocusId: string | null = null;

    constructor(tunnelId: string, itemsId: string) {
        this.tunnelElement = document.getElementById(tunnelId)!;
        this.itemsElement = document.getElementById(itemsId)!;
    }

    public async zoomToCluster(noteId: string): Promise<void> {
        this.currentFocusId = noteId;
        this.tunnelElement.classList.add('pull-animation');
        try {
            const res = await fetch(`/api/gravity/${noteId}`);
            const neighbors: GravityNode[] = await res.json();
            this.renderNeighbors(neighbors.slice(0, 3));
        } catch (_) {}
        setTimeout(() => this.tunnelElement.classList.remove('pull-animation'), 400);
    }

    private renderNeighbors(notes: GravityNode[]): void {
        if (!this.itemsElement) return;
        if (notes.length === 0) {
            this.itemsElement.innerHTML =
                '<div class="tunnel-node dim"><span class="pixel-prefix">>></span> no gravity pull...</div>';
            return;
        }
        this.itemsElement.innerHTML = notes.map(n => {
            const pct = Math.round((n.proximityScore || 0) * 100);
            return (
                '<div class="tunnel-node entering">' +
                    '<span class="pixel-prefix">>></span> ' +
                    '<span class="node-title">' + n.title + '</span>' +
                    '<div class="gravity-meter"><div class="gravity-meter-fill" style="width:' + pct + '%"></div></div>' +
                '</div>'
            );
        }).join('');
        requestAnimationFrame(() => {
            document.querySelectorAll('.tunnel-node.entering').forEach(el => el.classList.remove('entering'));
        });
    }
}

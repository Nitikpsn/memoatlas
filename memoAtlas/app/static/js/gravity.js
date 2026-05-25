class FocusTunnel {
    constructor(elementId) {
        this.tunnelElement = document.getElementById(elementId);
        this.prevNodes = [];
        this.animFrame = null;
    }

    updateGravity(nodes) {
        nodes.sort((a, b) => b.proximityScore - a.proximityScore);
        const top3 = nodes.slice(0, 3);

        if (JSON.stringify(top3) === JSON.stringify(this.prevNodes)) return;
        this.prevNodes = top3;
        this.tunnelElement.innerHTML = '';

        if (top3.length === 0) {
            const div = document.createElement('div');
            div.className = 'tunnel-node dim';
            div.innerHTML = `<span class="pixel">>></span> no gravity pull...`;
            this.tunnelElement.appendChild(div);
            return;
        }

        top3.forEach((node, i) => {
            setTimeout(() => this.attractNode(node), i * 180);
        });
    }

    attractNode(node) {
        const div = document.createElement('div');
        div.className = 'tunnel-node entering';
        div.innerHTML = `<span class="pixel">>></span> ${node.title}`;
        this.tunnelElement.appendChild(div);
        requestAnimationFrame(() => {
            div.classList.remove('entering');
            div.classList.add('pulse-red');
        });
    }
}

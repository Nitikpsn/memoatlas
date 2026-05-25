class FocusTunnel {
    constructor(elementId) {
        this.tunnelElement = document.getElementById(elementId);
    }

    updateGravity(nodes) {
        this.tunnelElement.innerHTML = '';
        nodes.sort((a, b) => b.proximityScore - a.proximityScore)
             .slice(0, 3)
             .forEach(node => this.renderNode(node));
    }

    renderNode(node) {
        const div = document.createElement('div');
        div.className = 'tunnel-node pulse-red';
        div.innerHTML = `<span class="pixel">>></span> ${node.title}`;
        this.tunnelElement.appendChild(div);
    }
}

interface GravityNode {
    id: string;
    title: string;
    proximityScore: number;
    tags: string[];
}

class FocusTunnel {
    private tunnelElement: HTMLElement;

    constructor(elementId: string) {
        this.tunnelElement = document.getElementById(elementId)!;
    }

    public updateGravity(nodes: GravityNode[]): void {
        this.tunnelElement.innerHTML = '';
        nodes.sort((a, b) => b.proximityScore - a.proximityScore)
             .slice(0, 3)
             .forEach(node => this.renderNode(node));
    }

    private renderNode(node: GravityNode): void {
        const div = document.createElement('div');
        div.className = 'tunnel-node pulse-red';
        div.innerHTML = `<span class="pixel">>></span> ${node.title}`;
        this.tunnelElement.appendChild(div);
    }
}

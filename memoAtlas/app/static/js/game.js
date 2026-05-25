class SpatialMap {
  constructor(canvasId, tunnel) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.tunnel = tunnel;
    this.nodes = [];
    this.edges = [];
    this.selectedId = null;
    this.offsetX = 0;
    this.offsetY = 0;
    this.scale = 1;
    this.dragging = false;
    this.dragStartX = 0;
    this.dragStartY = 0;
    this.dragOffX = 0;
    this.dragOffY = 0;
    this.animFrame = null;
    this.branchCache = {};

    this._resize();
    window.addEventListener('resize', function() { this._resize(); this.render(); }.bind(this));

    this.canvas.addEventListener('mousedown', this._onMouseDown.bind(this));
    this.canvas.addEventListener('mousemove', this._onMouseMove.bind(this));
    this.canvas.addEventListener('mouseup', this._onMouseUp.bind(this));
    this.canvas.addEventListener('click', this._onClick.bind(this));
    this.canvas.addEventListener('wheel', this._onWheel.bind(this));
  }

  _resize() {
    var rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height;
  }

  async load() {
    try {
      var res = await fetch('/api/graph-data');
      var data = await res.json();
      this.nodes = data.nodes || [];
      this.edges = data.links || [];
      this._layout();
      this.render();
    } catch(e) { console.error('SpatialMap load error', e); }
  }

  _layout() {
    var cx = this.canvas.width / 2;
    var cy = this.canvas.height / 2;
    var n = this.nodes.length;
    if (n === 0) return;

    var radius = Math.min(cx, cy) * 0.55;
    for (var i = 0; i < n; i++) {
      var angle = (i / n) * 2 * Math.PI - Math.PI / 2;
      this.nodes[i].x = cx + radius * Math.cos(angle);
      this.nodes[i].y = cy + radius * Math.sin(angle);
    }

    this._hashBranches();
  }

  _hashBranches() {
    this.branchCache = {};
    this.edges.forEach(function(e) {
      var fromId = e.from || e.source;
      var toId = e.to || e.target;
      var key = fromId < toId ? fromId + '-' + toId : toId + '-' + fromId;
      if (!this.branchCache[key]) {
        this.branchCache[key] = (Math.random() * 40 - 20);
      }
    }.bind(this));
  }

  render() {
    if (this.animFrame) cancelAnimationFrame(this.animFrame);
    this._draw();
  }

  _draw() {
    var ctx = this.ctx;
    var w = this.canvas.width;
    var h = this.canvas.height;

    ctx.clearRect(0, 0, w, h);

    ctx.strokeStyle = 'rgba(239,68,68,0.03)';
    ctx.lineWidth = 1;
    for (var x = 0; x < w; x += 60) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (var y = 0; y < h; y += 60) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }

    ctx.save();
    ctx.translate(this.offsetX, this.offsetY);
    ctx.translate(w / 2, h / 2);
    ctx.scale(this.scale, this.scale);
    ctx.translate(-w / 2, -h / 2);

    var nodeMap = {};
    this.nodes.forEach(function(n) { nodeMap[n.id] = n; });

    this.edges.forEach(function(e) {
      var from = nodeMap[e.from || e.source];
      var to = nodeMap[e.to || e.target];
      if (!from || !to) return;
      var key = (from.id < to.id ? from.id + '-' + to.id : to.id + '-' + from.id);
      var cpOff = this.branchCache[key] || 0;
      var cpX = (from.x + to.x) / 2 + cpOff;
      var cpY = (from.y + to.y) / 2 + cpOff * 0.6;
      ctx.beginPath();
      ctx.moveTo(from.x, from.y);
      ctx.quadraticCurveTo(cpX, cpY, to.x, to.y);
      ctx.strokeStyle = 'rgba(239,68,68,0.2)';
      ctx.lineWidth = 1.2;
      ctx.stroke();
    }.bind(this));

    this.nodes.forEach(function(n) {
      var isSel = n.id == this.selectedId;
      var r = isSel ? 9 : 6;
      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = isSel ? '#EF4444' : 'rgba(239,68,68,0.6)';
      if (isSel) {
        ctx.shadowColor = '#EF4444';
        ctx.shadowBlur = 20;
      }
      ctx.fill();
      ctx.shadowBlur = 0;

      if (n.title) {
        ctx.font = '13px Pixelify Sans';
        ctx.fillStyle = '#F4F4F5';
        ctx.textAlign = 'center';
        ctx.fillText(n.title, n.x, n.y + r + 16);
      }
    }.bind(this));

    ctx.restore();
  }

  _getNodeAt(clientX, clientY) {
    var rect = this.canvas.getBoundingClientRect();
    var mx = clientX - rect.left;
    var my = clientY - rect.top;
    var w = this.canvas.width;
    var h = this.canvas.height;
    var tx = (mx - this.offsetX - w / 2 * (1 - this.scale)) / this.scale;
    var ty = (my - this.offsetY - h / 2 * (1 - this.scale)) / this.scale;

    for (var i = this.nodes.length - 1; i >= 0; i--) {
      var n = this.nodes[i];
      var dx = tx - n.x;
      var dy = ty - n.y;
      if (dx * dx + dy * dy < 400) return n;
    }
    return null;
  }

  _onMouseDown(e) {
    this.dragging = true;
    this.dragStartX = e.clientX;
    this.dragStartY = e.clientY;
    this.dragOffX = this.offsetX;
    this.dragOffY = this.offsetY;
  }

  _onMouseMove(e) {
    if (!this.dragging) return;
    this.offsetX = this.dragOffX + (e.clientX - this.dragStartX);
    this.offsetY = this.dragOffY + (e.clientY - this.dragStartY);
    this.render();
  }

  _onMouseUp() {
    this.dragging = false;
  }

  _onClick(e) {
    var n = this._getNodeAt(e.clientX, e.clientY);
    if (!n) return;
    this.selectedId = n.id;
    this.render();
    if (this.tunnel) this.tunnel.zoomToCluster(n.id);
  }

  _onWheel(e) {
    e.preventDefault();
    var delta = e.deltaY > 0 ? -0.08 : 0.08;
    this.scale = Math.max(0.3, Math.min(3, this.scale + delta));
    this.render();
  }

  zoom(delta) {
    this.scale = Math.max(0.3, Math.min(3, this.scale + delta));
    this.render();
  }

  resetView() {
    this.offsetX = 0;
    this.offsetY = 0;
    this.scale = 1;
    this.selectedId = null;
    this._layout();
    this.render();
  }
}

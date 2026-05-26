/*
 * game.js - the interactive "explore map" mode
 * draws a canvas with all your notes as nodes you can click and connect
 */

function SpatialMap(canvasId, tunnel) {
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
    this.linkInProgress = false;

    // set up canvas size
    this._resize();
    var self = this;
    window.addEventListener('resize', function() {
        self._resize();
        self.render();
    });

    // mouse events
    this.canvas.addEventListener('mousedown', function(e) { self._onMouseDown(e); });
    this.canvas.addEventListener('mousemove', function(e) { self._onMouseMove(e); });
    this.canvas.addEventListener('mouseup', function(e) { self._onMouseUp(e); });
    this.canvas.addEventListener('click', function(e) { self._onClick(e); });
    this.canvas.addEventListener('wheel', function(e) { self._onWheel(e); });
}

SpatialMap.prototype._resize = function() {
    var rect = this.canvas.parentElement.getBoundingClientRect();
    this.canvas.width = rect.width;
    this.canvas.height = rect.height;
};

SpatialMap.prototype.load = function() {
    var self = this;
    fetch('/api/graph-data')
        .then(function(res) { return res.json(); })
        .then(function(data) {
            self.nodes = data.nodes || [];
            self.edges = data.links || [];
            self._layout();
            self.render();
        })
        .catch(function(e) {
            console.error('SpatialMap load error', e);
        });
};

SpatialMap.prototype._layout = function() {
    var cx = this.canvas.width / 2;
    var cy = this.canvas.height / 2;
    var n = this.nodes.length;

    if (n === 0) {
        return;
    }

    // arrange nodes in a circle
    var radius = Math.min(cx, cy) * 0.55;
    for (var i = 0; i < n; i++) {
        var angle = (i / n) * 2 * Math.PI - Math.PI / 2;
        this.nodes[i].x = cx + radius * Math.cos(angle);
        this.nodes[i].y = cy + radius * Math.sin(angle);
    }

    this._hashBranches();
};

SpatialMap.prototype._hashBranches = function() {
    this.branchCache = {};
    for (var i = 0; i < this.edges.length; i++) {
        var e = this.edges[i];
        var fromId = e.from || e.source;
        var toId = e.to || e.target;
        var key = fromId < toId ? fromId + '-' + toId : toId + '-' + fromId;
        if (!this.branchCache[key]) {
            this.branchCache[key] = (Math.random() * 40 - 20);
        }
    }
};

SpatialMap.prototype.render = function() {
    if (this.animFrame) {
        cancelAnimationFrame(this.animFrame);
    }
    this._draw();
};

SpatialMap.prototype._draw = function() {
    var ctx = this.ctx;
    var w = this.canvas.width;
    var h = this.canvas.height;

    // clear canvas
    ctx.clearRect(0, 0, w, h);

    // draw grid lines
    ctx.strokeStyle = 'rgba(239,68,68,0.03)';
    ctx.lineWidth = 1;
    for (var x = 0; x < w; x += 60) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, h);
        ctx.stroke();
    }
    for (var y = 0; y < h; y += 60) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
    }

    // apply pan and zoom
    ctx.save();
    ctx.translate(this.offsetX, this.offsetY);
    ctx.translate(w / 2, h / 2);
    ctx.scale(this.scale, this.scale);
    ctx.translate(-w / 2, -h / 2);

    // build a map of node ids to nodes
    var nodeMap = {};
    for (var i = 0; i < this.nodes.length; i++) {
        nodeMap[this.nodes[i].id] = this.nodes[i];
    }

    // draw edges (connections between nodes)
    for (var i = 0; i < this.edges.length; i++) {
        var e = this.edges[i];
        var from = nodeMap[e.from || e.source];
        var to = nodeMap[e.to || e.target];
        if (!from || !to) {
            continue;
        }

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
    }

    // draw nodes
    for (var i = 0; i < this.nodes.length; i++) {
        var n = this.nodes[i];
        var isSel = n.id == this.selectedId;
        var isMatched = n.is_matched === true;
        var r = isSel ? 9 : 7;

        // unmatched nodes are dimmed
        if (!isMatched) {
            ctx.globalAlpha = 0.35;
        }

        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);

        if (isMatched) {
            ctx.fillStyle = isSel ? '#EF4444' : '#EF4444';
            if (isSel) {
                ctx.shadowColor = '#EF4444';
                ctx.shadowBlur = 20;
            } else {
                ctx.shadowColor = 'rgba(239,68,68,0.4)';
                ctx.shadowBlur = 8;
            }
        } else {
            ctx.fillStyle = isSel ? 'rgba(239,68,68,0.8)' : 'rgba(160,160,160,0.5)';
            ctx.shadowBlur = 0;
        }

        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.globalAlpha = 1;

        // draw node title
        if (n.title) {
            ctx.font = '13px Pixelify Sans';
            ctx.fillStyle = isMatched ? '#F4F4F5' : 'rgba(160,160,160,0.5)';
            ctx.textAlign = 'center';
            ctx.fillText(n.title, n.x, n.y + r + 16);
        }

        // show LOCKED for unmatched selected nodes
        if (!isMatched && isSel) {
            ctx.font = '9px Pixelify Sans';
            ctx.fillStyle = 'rgba(239,68,68,0.5)';
            ctx.textAlign = 'center';
            ctx.fillText('[LOCKED]', n.x, n.y + r + 30);
        }
    }

    ctx.restore();
};

SpatialMap.prototype._getNodeAt = function(clientX, clientY) {
    var rect = this.canvas.getBoundingClientRect();
    var mx = clientX - rect.left;
    var my = clientY - rect.top;
    var w = this.canvas.width;
    var h = this.canvas.height;
    var tx = (mx - this.offsetX - w / 2 * (1 - this.scale)) / this.scale;
    var ty = (my - this.offsetY - h / 2 * (1 - this.scale)) / this.scale;

    // check each node (reverse order so top nodes are checked first)
    for (var i = this.nodes.length - 1; i >= 0; i--) {
        var n = this.nodes[i];
        var dx = tx - n.x;
        var dy = ty - n.y;
        if (dx * dx + dy * dy < 400) {
            return n;
        }
    }
    return null;
};

SpatialMap.prototype._onMouseDown = function(e) {
    this.dragging = true;
    this.dragStartX = e.clientX;
    this.dragStartY = e.clientY;
    this.dragOffX = this.offsetX;
    this.dragOffY = this.offsetY;
};

SpatialMap.prototype._onMouseMove = function(e) {
    if (!this.dragging) {
        return;
    }
    this.offsetX = this.dragOffX + (e.clientX - this.dragStartX);
    this.offsetY = this.dragOffY + (e.clientY - this.dragStartY);
    this.render();
};

SpatialMap.prototype._onMouseUp = function() {
    this.dragging = false;
};

SpatialMap.prototype._onClick = function(e) {
    var n = this._getNodeAt(e.clientX, e.clientY);
    if (!n) {
        return;
    }
    this.selectedId = n.id;
    this.render();
    if (this.tunnel) {
        this.tunnel.zoomToCluster(n.id);
    }
};

SpatialMap.prototype._onWheel = function(e) {
    e.preventDefault();
    var delta = e.deltaY > 0 ? -0.08 : 0.08;
    this.scale = Math.max(0.3, Math.min(3, this.scale + delta));
    this.render();
};

SpatialMap.prototype.zoom = function(delta) {
    this.scale = Math.max(0.3, Math.min(3, this.scale + delta));
    this.render();
};

SpatialMap.prototype.resetView = function() {
    this.offsetX = 0;
    this.offsetY = 0;
    this.scale = 1;
    this.selectedId = null;
    this._layout();
    this.render();
};

SpatialMap.prototype.createLink = function(targetId) {
    if (this.linkInProgress) {
        return;
    }
    this.linkInProgress = true;

    var sourceId = this.selectedId;
    if (!sourceId || !targetId || sourceId == targetId) {
        this.linkInProgress = false;
        return;
    }

    var self = this;
    fetch('/api/link', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_id: sourceId, target_id: targetId })
    })
    .then(function(res) { return res.json(); })
    .then(function(data) {
        if (data.error) {
            console.error('Link error:', data.error);
            self.linkInProgress = false;
            return;
        }

        // show XP toast
        if (data.xp_gained > 0) {
            self._showMatchToast();
        }

        // mark nodes as matched
        var sourceNode = null;
        var targetNode = null;
        for (var i = 0; i < self.nodes.length; i++) {
            if (self.nodes[i].id === data.connection.source_id) {
                sourceNode = self.nodes[i];
            }
            if (self.nodes[i].id === data.connection.target_id) {
                targetNode = self.nodes[i];
            }
        }
        if (sourceNode) { sourceNode.is_matched = true; }
        if (targetNode) { targetNode.is_matched = true; }

        // add the new edge
        self.edges.push({
            source: data.connection.source_id,
            target: data.connection.target_id,
            value: 1,
            manual: true
        });
        self._hashBranches();
        self.render();

        // update the tunnel UI
        if (self.tunnel && data.xp_gained > 0) {
            self.tunnel.renderNeighborsWithLink(data.connection.source_id, data.connection.target_id);
        }

        self.linkInProgress = false;
    })
    .catch(function(e) {
        console.error('Link creation error', e);
        self.linkInProgress = false;
    });
};

SpatialMap.prototype._showMatchToast = function() {
    var container = document.getElementById('matchToastContainer');
    if (!container) {
        return;
    }

    var toast = document.createElement('div');
    toast.className = 'match-toast';
    toast.innerHTML = 'MATCH CAUGHT<span class="xp-sub">+100 XP</span>';
    container.appendChild(toast);

    var xpContainer = document.getElementById('xpContainer');
    if (xpContainer) {
        xpContainer.classList.remove('xp-flash');
        // force reflow
        void xpContainer.offsetWidth;
        xpContainer.classList.add('xp-flash');
    }

    setTimeout(function() {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 2000);
};

function showMatchToast(message, xp) {
    var container = document.getElementById('matchToastContainer');
    if (!container) {
        return;
    }

    var toast = document.createElement('div');
    toast.className = 'match-toast';
    toast.innerHTML = (message || 'MATCH CAUGHT') + '<span class="xp-sub">+' + (xp || 100) + ' XP</span>';
    container.appendChild(toast);

    var xpContainer = document.getElementById('xpContainer');
    if (xpContainer) {
        xpContainer.classList.remove('xp-flash');
        void xpContainer.offsetWidth;
        xpContainer.classList.add('xp-flash');
    }

    setTimeout(function() {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 2000);
}

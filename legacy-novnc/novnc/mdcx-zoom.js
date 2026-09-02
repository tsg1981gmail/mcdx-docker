/* mdcx-zoom.js —— 手机/触屏双指捏合缩放 + 悬浮缩放条（本地缩放 noVNC 画面，不发送给远程应用） */
(function () {
  if (window.top !== window.self) return;
  var max = 5, min = 0.2;
  function clamp(v) { return Math.min(max, Math.max(min, v)); }
  function dist(e) {
    var dx = e.touches[0].clientX - e.touches[1].clientX;
    var dy = e.touches[0].clientY - e.touches[1].clientY;
    return Math.sqrt(dx * dx + dy * dy);
  }
  var screen = null, display = null;
  function findScreen() {
    var ids = ['noVNC_container', 'noVNC_screen', 'screen'];
    for (var i = 0; i < ids.length; i++) {
      var el = document.getElementById(ids[i]);
      if (el) return el;
    }
    return document.querySelector('canvas') !== null ? document.querySelector('canvas').parentElement : null;
  }
  function pct() {
    var el = document.getElementById('mdcx-zoom-pct');
    if (el && display) el.textContent = Math.round(display.scale * 100) + '%';
  }
  function zoomTo(n) { if (!display) return; try { display.scale = clamp(n); pct(); } catch (e) {} }
  function buildBar() {
    var bar = document.createElement('div');
    bar.id = 'mdcx-zoom-bar';
    bar.style.cssText =
      'position:fixed;right:10px;bottom:64px;z-index:999999;display:flex;flex-direction:column;gap:5px;' +
      'background:rgba(15,23,42,.78);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:6px;';
    [['−', 0.82], ['＋', 1.22]].forEach(function (b) {
      var btn = document.createElement('button');
      btn.textContent = b[0];
      btn.style.cssText = 'width:38px;height:38px;border:0;border-radius:9px;background:rgba(64,158,255,.9);color:#fff;font-size:20px;cursor:pointer;touch-action:manipulation;';
      btn.onclick = function () { zoomTo((display ? display.scale : 1) * b[1]); };
      bar.appendChild(btn);
    });
    var fit = document.createElement('button');
    fit.textContent = '适';
    fit.title = '自适应窗口';
    fit.style.cssText = 'width:38px;height:38px;border:0;border-radius:9px;background:rgba(80,170,90,.9);color:#fff;font-size:15px;cursor:pointer;touch-action:manipulation;';
    fit.onclick = function () { if (screen && display) { try { display.autoscale(screen.clientWidth, screen.clientHeight - 10); pct(); } catch (e) {} } };
    bar.appendChild(fit);
    var p = document.createElement('span');
    p.id = 'mdcx-zoom-pct';
    p.style.cssText = 'color:#fff;font:12px system-ui;text-align:center;';
    p.textContent = '100%';
    bar.appendChild(p);
    document.body.appendChild(bar);
  }
  var startDist = 0, startScale = 1, pinching = false;
  function wire() {
    if (!screen) return;
    screen.addEventListener('touchstart', function (e) {
      if (e.touches.length === 2) { startDist = dist(e); startScale = display ? display.scale : 1; pinching = true; }
    }, { passive: true, capture: true });
    screen.addEventListener('touchmove', function (e) {
      if (pinching && e.touches.length === 2 && startDist > 0) {
        var d = dist(e);
        zoomTo(startScale * d / startDist);
        if (e.cancelable) e.preventDefault();          // 阻止 noVNC 将其当作远程滚轮
        e.stopPropagation();                            // 阻止 noVNC 手势把缩放发给远程应用
      }
    }, { passive: false, capture: true });
    screen.addEventListener('touchend', function (e) {
      if (e.touches.length < 2) pinching = false;
    }, { passive: true, capture: true });
  }
  function init() {
    if (!window.UI || !UI.rfb) { setTimeout(init, 500); return; }
    display = UI.rfb._display;
    screen = findScreen();
    if (!screen) { setTimeout(init, 1000); return; }
    buildBar();
    wire();
    pct();
  }
  if (document.readyState === 'complete') init(); else window.addEventListener('load', init);
})();
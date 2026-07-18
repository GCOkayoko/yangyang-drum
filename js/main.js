document.addEventListener('DOMContentLoaded', () => {

const drumAudio = new Audio('audio/鼓声.mp3');
drumAudio.preload = 'auto';
function playDrumOnce() { drumAudio.currentTime = 0; drumAudio.play().catch(()=>{}); }

let f1 = 0, f2 = 0;
const TOTAL1 = 20, TOTAL2 = 60;

const img1 = document.getElementById('img1');
const img2 = document.getElementById('img2');
const char1 = document.getElementById('char1');
const char2 = document.getElementById('char2');
const zone1 = document.getElementById('zone1');
const zone2 = document.getElementById('zone2');
const stage1 = document.getElementById('stage1');
const stage2 = document.getElementById('stage2');

function framePath1(n) { return 'img/drum1_frame_' + String(n+1).padStart(3,'0') + '.png'; }
function framePath2(n) { return 'img/frame_' + String(n+1).padStart(3,'0') + '.png'; }

function advanceFrame() {
  f1 = (f1 + 1) % TOTAL1; f2 = (f2 + 1) % TOTAL2;
  img1.src = framePath1(f1); img2.src = framePath2(f2);
  char1.classList.add('shake'); zone1.classList.add('flash');
  char2.classList.add('shake'); zone2.classList.add('flash');
  setTimeout(function() {
    char1.classList.remove('shake'); zone1.classList.remove('flash');
    char2.classList.remove('shake'); zone2.classList.remove('flash');
  }, 100);
  spawnFx(stage1, '咚'); spawnFx(stage2, '嗒');
}

function hitDrum() { advanceFrame(); playDrumOnce(); }

function spawnFx(parent, text) {
  var fx = document.createElement('div');
  fx.className = 'hit-fx'; fx.textContent = text;
  fx.style.left = '42%'; fx.style.top = '38%';
  parent.appendChild(fx);
  setTimeout(function() { fx.remove(); }, 600);
}

function resetAll() {
  stopAuto();
  f1 = 0; f2 = 0;
  img1.src = framePath1(0); img2.src = framePath2(0);
}

// 自动播放
var autoTimer = null, autoRunning = false;
var SPEED = 100;

function toggleAuto() { if (autoRunning) stopAuto(); else startAuto(); }
function startAuto() {
  autoRunning = true;
  document.getElementById('btnAuto').textContent = '⏸ 停止';
  document.getElementById('btnAuto').classList.add('active');
  autoStep();
}
function stopAuto() {
  autoRunning = false;
  if (autoTimer) clearTimeout(autoTimer);
  autoTimer = null;
  document.getElementById('btnAuto').textContent = '▶ 自动播放';
  document.getElementById('btnAuto').classList.remove('active');
}
function autoStep() {
  if (!autoRunning) return;
  advanceFrame();
  drumAudio.currentTime = 0; drumAudio.play().catch(function(){});
  autoTimer = setTimeout(autoStep, SPEED);
}

// 按钮事件
document.getElementById('btnAuto').addEventListener('click', toggleAuto);
document.getElementById('btnReset').addEventListener('click', resetAll);

// 键盘事件
document.addEventListener('keydown', function(e) {
  if (e.repeat) return;
  var k = e.key.toLowerCase();
  if (k === 'f' || k === 'j') hitDrum();
  if (k === ' ') { e.preventDefault(); toggleAuto(); }
});

// 点击鼓区
zone1.addEventListener('click', hitDrum);
zone2.addEventListener('click', hitDrum);

// 粒子
var particlesEl = document.getElementById('particles');
var symbols = ['🐦','🕊️','🦜','🦅','🦉','🐤','🦆','🐧','🐓','🦢'];
for (var i = 0; i < 12; i++) {
  var p = document.createElement('span');
  p.className = 'particle';
  p.textContent = symbols[Math.floor(Math.random() * symbols.length)];
  p.style.left = Math.random() * 100 + '%';
  p.style.animationDelay = Math.random() * 6 + 's';
  p.style.animationDuration = (3 + Math.random() * 5) + 's';
  p.style.fontSize = (10 + Math.random() * 14) + 'px';
  particlesEl.appendChild(p);
}

// 标题逐字从左到右变大
var titleText = '大鼓 大鼓 敲敲敲！！！';
var titleEl = document.getElementById('titleEl');
var chars = titleText.split('');
chars.forEach(function(ch, i) {
  var s = document.createElement('span');
  s.textContent = ch;
  var size = 16 + (i / (chars.length - 1)) * 24;
  s.style.fontSize = size + 'px';
  titleEl.appendChild(s);
});

});

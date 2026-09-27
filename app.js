// 마법 적성 감정소 — 손 제스처(검지 왼→오 스와이프)로 불/물/흙/공기/빛 속성을 랜덤 감정한다.

const VISION_VERSION = "0.10.14";
const VISION_SOURCES = [
  { module: "./vendor/tasks-vision/vision_bundle.mjs", wasm: "./vendor/tasks-vision/wasm" },
  {
    module: `https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@${VISION_VERSION}/vision_bundle.mjs`,
    wasm: `https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@${VISION_VERSION}/wasm`,
  },
];
const MODEL_SOURCES = [
  "./vendor/hand_landmarker.task",
  "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
];

const SWIPE_DISTANCE = 0.28; // 화면 너비 대비 이동 비율
const SWIPE_WINDOW_MS = 800; // 이 시간 안에 SWIPE_DISTANCE만큼 움직이면 스와이프
const CAST_MS = 2600;
const REVEAL_MS = 15000;
const NEXT_READY_MS = 6000; // 결과 화면에서 이 시간이 지나면 다음 스와이프 허용
const STATS_KEY = "arcanum-stats-v1";

const ELEMENTS = {
  fire: {
    name: "불",
    title: "불의 마법사",
    klass: "화염술사 · PYROMANCER",
    c1: "#ff6a2b",
    c2: "#ffc27a",
    desc: "가슴 속에 꺼지지 않는 불꽃을 품은 당신. 한 번 마음먹은 일은 끝까지 태워내는 열정과 용기가 당신의 마법입니다.",
    traits: ["열정", "용기", "추진력"],
    spell: "“이그니스 플라마 — 타올라라!”",
    palette: ["#ff3d00", "#ff7a1a", "#ffb347", "#ffe08a"],
    root: 196,
  },
  water: {
    name: "물",
    title: "물의 마법사",
    klass: "수류술사 · HYDROMANCER",
    c1: "#2fa8ff",
    c2: "#a8e6ff",
    desc: "어떤 그릇에도 담기는 물처럼 유연한 당신. 부드럽지만 바위도 깎아내는 끈기로 사람들의 마음을 감싸 안습니다.",
    traits: ["공감", "유연함", "치유"],
    spell: "“아쿠아 룩스 — 흘러라!”",
    palette: ["#1e88e5", "#4fc3f7", "#a8e6ff", "#e1f5fe"],
    root: 220,
  },
  earth: {
    name: "흙",
    title: "흙의 마법사",
    klass: "대지술사 · GEOMANCER",
    c1: "#9ccc65",
    c2: "#e6c98f",
    desc: "모두가 흔들릴 때 묵묵히 자리를 지키는 당신. 단단한 대지처럼 든든한 믿음과 성실함이 당신의 마법입니다.",
    traits: ["인내", "신뢰", "성실"],
    spell: "“테라 솔리다 — 일어나라!”",
    palette: ["#7cb342", "#aed581", "#c8a165", "#8d6e63"],
    root: 174.6,
  },
  air: {
    name: "공기",
    title: "공기의 마법사",
    klass: "풍령술사 · AEROMANCER",
    c1: "#5ff2d2",
    c2: "#d8fff6",
    desc: "바람처럼 자유롭고 호기심 가득한 당신. 번뜩이는 생각으로 어디든 날아가 세상에 새로운 바람을 일으킵니다.",
    traits: ["자유", "창의력", "호기심"],
    spell: "“벤투스 알라 — 날아올라라!”",
    palette: ["#5ff2d2", "#b2fff0", "#e0fffa", "#9ad0ff"],
    root: 246.9,
  },
  light: {
    name: "빛",
    title: "빛의 마법사",
    klass: "광휘술사 · LUMOMANCER",
    c1: "#ffd84d",
    c2: "#fff6cc",
    desc: "어둠 속에서도 희망을 찾아내는 당신. 곁에 있는 모두의 길을 환하게 비춰주는 따뜻함이 당신의 마법입니다.",
    traits: ["희망", "긍정", "지혜"],
    spell: "“룩스 에테르나 — 빛나라!”",
    palette: ["#fff6cc", "#ffe27a", "#ffd84d", "#ffffff"],
    root: 261.6,
  },
};
// 오각별 꼭짓점 순서(맨 위부터 시계방향)
const GEM_ORDER = ["light", "fire", "earth", "water", "air"];

function symbolSvg(key, extraClass = "") {
  const shapes = {
    fire: '<polygon pathLength="1" points="50,10 92,84 8,84"/>',
    water: '<polygon pathLength="1" points="8,16 92,16 50,90"/>',
    air: '<polygon pathLength="1" points="50,10 92,84 8,84"/><line pathLength="1" x1="24" y1="58" x2="76" y2="58"/>',
    earth: '<polygon pathLength="1" points="8,16 92,16 50,90"/><line pathLength="1" x1="24" y1="42" x2="76" y2="42"/>',
    light:
      '<circle pathLength="1" cx="50" cy="50" r="15"/>' +
      Array.from({ length: 8 }, (_, i) => {
        const a = (i * Math.PI) / 4 - Math.PI / 2;
        const r1 = 24;
        const r2 = i % 2 === 0 ? 42 : 34;
        const f = (n) => n.toFixed(2);
        return `<line pathLength="1" x1="${f(50 + r1 * Math.cos(a))}" y1="${f(50 + r1 * Math.sin(a))}" x2="${f(50 + r2 * Math.cos(a))}" y2="${f(50 + r2 * Math.sin(a))}"/>`;
      }).join(""),
  };
  return `<svg class="${extraClass}" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">${shapes[key]}</svg>`;
}

// ---------------------------------------------------------------------------
// DOM
const $ = (s) => document.querySelector(s);
const body = document.body;
const video = $("#cam");
const bg = $("#bg");
const bgCtx = bg.getContext("2d");
const trailCanvas = $("#trail");
const trailCtx = trailCanvas.getContext("2d");
const statusText = $("#status-text");
const meterFill = $(".swipe-meter .fill");
const meterSpark = $(".swipe-meter .spark");
const castSymbol = $(".cast-symbol");
const flash = $(".flash");
const ringOuter = $("#ring-outer");
const ringInner = $("#ring-inner");
const circleWrap = $(".circle-wrap");

const state = {
  phase: "intro",
  pick: null,
  revealAt: 0,
  revealTimer: 0,
  handOn: false,
  lastHandAt: 0,
  cameraError: false,
  modelReady: false,
  statusKey: "",
};
const history = []; // 최근 손끝 위치 {x, y, t} (0~1, 거울 좌표)
const trail = []; // 화면 좌표 손끝 궤적
let pointerDown = false;
let W = 0;
let H = 0;
let DPR = 1;

// ---------------------------------------------------------------------------
// 마법진 & 보석 배치
(function buildCircle() {
  const ticks = $("#ticks");
  let html = "";
  for (let i = 0; i < 72; i++) {
    const a = (i * 5 * Math.PI) / 180;
    const long = i % 6 === 0;
    const r1 = 190;
    const r2 = long ? 180 : 185;
    html += `<line class="tick${long ? " long" : ""}" x1="${(r1 * Math.cos(a)).toFixed(2)}" y1="${(r1 * Math.sin(a)).toFixed(2)}" x2="${(r2 * Math.cos(a)).toFixed(2)}" y2="${(r2 * Math.sin(a)).toFixed(2)}"/>`;
  }
  ticks.innerHTML = html;

  const gems = $("#gems");
  gems.innerHTML = GEM_ORDER.map((key, i) => {
    const a = ((-90 + i * 72) * Math.PI) / 180;
    const r = 35; // % (= 140 / 400)
    const lr = 53; // 이름표는 마법진 바깥쪽에
    const el = ELEMENTS[key];
    const pos = (rr) => `left:${50 + rr * Math.cos(a)}%;top:${50 + rr * Math.sin(a)}%`;
    return (
      `<div class="gem" data-key="${key}" style="--c:${el.c1};${pos(r)}">${symbolSvg(key)}</div>` +
      `<span class="gem-label" style="--c:${el.c1};${pos(lr)}">${el.name}</span>`
    );
  }).join("");
})();

function highlightGem(key) {
  document.querySelectorAll(".gem").forEach((g) => g.classList.toggle("active", g.dataset.key === key));
}

function setTheme(key) {
  const el = ELEMENTS[key];
  document.documentElement.style.setProperty("--c1", el.c1);
  document.documentElement.style.setProperty("--c2", el.c2);
}

// ---------------------------------------------------------------------------
// 상태 표시
const STATUS = {
  loading: "마법 거울을 깨우는 중이에요…",
  noHand: "거울 앞에 손을 들어 보여주세요",
  hand: "손이 보여요! 검지를 오른쪽으로 힘차게 휘두르세요",
  error: "카메라를 쓸 수 없어요 · 화면을 왼쪽→오른쪽으로 드래그하거나 스페이스바를 눌러주세요",
  modelError: "손 인식 마법을 불러오지 못했어요 · 드래그 또는 스페이스바로 시전할 수 있어요",
};
function setStatus(key) {
  if (state.statusKey === key) return;
  state.statusKey = key;
  statusText.textContent = STATUS[key];
}

function setPhase(p) {
  state.phase = p;
  body.dataset.phase = p;
  history.length = 0;
  setProgress(0);
}

function setProgress(p) {
  meterFill.style.width = `${p * 100}%`;
  if (body.dataset.hand === "on" || pointerDown) meterSpark.style.left = `${p * 100}%`;
  else meterSpark.style.left = "";
}

// ---------------------------------------------------------------------------
// 사운드 (WebAudio로 직접 합성)
const sfx = {
  ctx: null,
  master: null,
  muted: false,
  init() {
    if (this.ctx) return;
    try {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      this.master = this.ctx.createGain();
      this.master.gain.value = 0.5;
      this.master.connect(this.ctx.destination);
    } catch {
      this.ctx = null;
    }
  },
  tone(freq, start, dur, { type = "sine", gain = 0.2, to = null } = {}) {
    if (!this.ctx || this.muted) return;
    const t0 = this.ctx.currentTime + start;
    const osc = this.ctx.createOscillator();
    const g = this.ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(freq, t0);
    if (to) osc.frequency.exponentialRampToValueAtTime(to, t0 + dur);
    g.gain.setValueAtTime(0.0001, t0);
    g.gain.exponentialRampToValueAtTime(gain, t0 + Math.min(0.04, dur / 3));
    g.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(g).connect(this.master);
    osc.start(t0);
    osc.stop(t0 + dur + 0.05);
  },
  tick() {
    this.tone(1400 + Math.random() * 600, 0, 0.08, { type: "triangle", gain: 0.06 });
  },
  cast() {
    this.tone(180, 0, CAST_MS / 1000, { type: "sawtooth", gain: 0.035, to: 900 });
    this.tone(360, 0, CAST_MS / 1000, { type: "sine", gain: 0.08, to: 1800 });
  },
  reveal(key) {
    const root = ELEMENTS[key].root;
    this.tone(55, 0, 1.6, { type: "sine", gain: 0.35, to: 40 });
    [1, 1.25, 1.5, 2, 2.5, 3].forEach((m, i) => {
      this.tone(root * m, 0.05 + i * 0.09, 2.2, { type: "triangle", gain: 0.09 });
    });
    this.tone(root * 4, 0.6, 2.5, { type: "sine", gain: 0.05 });
  },
};

// ---------------------------------------------------------------------------
// 통계
function loadStats() {
  try {
    return JSON.parse(localStorage.getItem(STATS_KEY)) || {};
  } catch {
    return {};
  }
}
function saveStats(stats) {
  try {
    localStorage.setItem(STATS_KEY, JSON.stringify(stats));
  } catch {
    /* 저장 불가 환경이면 통계만 생략 */
  }
}
let stats = loadStats();
function renderStats() {
  const total = GEM_ORDER.reduce((s, k) => s + (stats[k] || 0), 0);
  $(".stats").innerHTML =
    `<span>탄생한 마법사 ${total}명</span>` +
    GEM_ORDER.map((k) => `<span class="stat" style="--c:${ELEMENTS[k].c1}">${symbolSvg(k)}${stats[k] || 0}</span>`).join("");
}
renderStats();

// ---------------------------------------------------------------------------
// 시전 & 결과
function randomElementKey() {
  const keys = Object.keys(ELEMENTS);
  const buf = new Uint32Array(1);
  crypto.getRandomValues(buf);
  return keys[buf[0] % keys.length];
}

function cast() {
  if (state.phase === "casting") return;
  clearTimeout(state.revealTimer);
  body.dataset.nextReady = "off";
  trail.length = 0;
  state.pick = randomElementKey();
  setPhase("casting");
  sfx.cast();

  const start = performance.now();
  let i = Math.floor(Math.random() * GEM_ORDER.length);
  let delay = 70;
  const step = () => {
    const elapsed = performance.now() - start;
    if (elapsed < CAST_MS - 500) {
      const key = GEM_ORDER[i++ % GEM_ORDER.length];
      showCastSymbol(key);
      sfx.tick();
      delay *= 1.13;
      setTimeout(step, delay);
    } else {
      showCastSymbol(state.pick);
      setTimeout(reveal, Math.max(250, CAST_MS - elapsed));
    }
  };
  step();
}

function showCastSymbol(key) {
  setTheme(key);
  highlightGem(key);
  castSymbol.innerHTML = symbolSvg(key);
}

function reveal() {
  const key = state.pick;
  const el = ELEMENTS[key];
  setTheme(key);

  $(".reveal-symbol").innerHTML = symbolSvg(key);
  $(".reveal-title").textContent = el.title;
  $(".reveal-class").textContent = el.klass;
  $(".reveal-desc").textContent = el.desc;
  $(".reveal-traits").innerHTML = el.traits.map((t) => `<li>${t}</li>`).join("");
  $(".reveal-spell").textContent = el.spell;

  flash.classList.remove("on");
  void flash.offsetWidth; // 애니메이션 재시작
  flash.classList.add("on");

  setPhase("reveal");
  highlightGem(null);
  state.revealAt = performance.now();
  burst(key);
  sfx.reveal(key);

  stats[key] = (stats[key] || 0) + 1;
  saveStats(stats);
  renderStats();

  state.revealTimer = setTimeout(backToIdle, REVEAL_MS);
}

function backToIdle() {
  clearTimeout(state.revealTimer);
  body.dataset.nextReady = "off";
  document.documentElement.style.setProperty("--c1", "#f5d27a");
  document.documentElement.style.setProperty("--c2", "#fff3c4");
  setPhase("idle");
}

function canSwipe(now) {
  if (state.phase === "idle") return true;
  if (state.phase === "reveal") return now - state.revealAt > NEXT_READY_MS;
  return false;
}

// ---------------------------------------------------------------------------
// 스와이프 판정 (손/마우스 공용)
function feedPoint(x, y, now) {
  history.push({ x, y, t: now });
  while (history.length && now - history[0].t > SWIPE_WINDOW_MS) history.shift();

  trail.push({ x: x * W, y: y * H, t: now });
  if (state.phase !== "casting" && Math.random() < 0.7) spawnTrailSpark(x * W, y * H);

  if (!canSwipe(now)) {
    setProgress(0);
    return;
  }
  const cur = history[history.length - 1];
  let start = cur;
  for (const p of history) if (p.x < start.x) start = p;
  const dx = cur.x - start.x;
  const dy = Math.abs(cur.y - start.y);
  setProgress(Math.max(0, Math.min(1, dx / SWIPE_DISTANCE)));
  if (dx >= SWIPE_DISTANCE && dy < dx * 0.9 && cur.t - start.t > 60) {
    cast();
  }
}

window.addEventListener("pointerdown", (e) => {
  if (state.phase === "intro") return;
  pointerDown = true;
  history.length = 0;
  feedPoint(e.clientX / W, e.clientY / H, performance.now());
});
window.addEventListener("pointermove", (e) => {
  if (!pointerDown) return;
  feedPoint(e.clientX / W, e.clientY / H, performance.now());
});
window.addEventListener("pointerup", () => {
  pointerDown = false;
  history.length = 0;
  setProgress(0);
});

window.addEventListener("keydown", (e) => {
  if (state.phase === "intro") return;
  if (e.code === "Space" || e.code === "Enter") {
    e.preventDefault();
    if (state.phase === "idle") cast();
    else if (state.phase === "reveal") backToIdle();
  } else if (e.code === "KeyF") {
    toggleFullscreen();
  } else if (e.code === "KeyM") {
    sfx.muted = !sfx.muted;
  } else if (e.code === "KeyR" && e.shiftKey) {
    stats = {};
    saveStats(stats);
    renderStats();
  }
});

function toggleFullscreen() {
  if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
  else document.documentElement.requestFullscreen?.().catch(() => {});
}

// ---------------------------------------------------------------------------
// 카메라 & 손 인식
let landmarker = null;
let lastVideoTime = -1;

async function startCamera() {
  const stream = await navigator.mediaDevices.getUserMedia({
    video: { width: { ideal: 1280 }, height: { ideal: 720 }, facingMode: "user" },
    audio: false,
  });
  video.srcObject = stream;
  await video.play();
}

async function loadLandmarker() {
  let lastError;
  for (const src of VISION_SOURCES) {
    let vision;
    try {
      vision = await import(src.module);
    } catch (err) {
      lastError = err;
      continue;
    }
    const fileset = await vision.FilesetResolver.forVisionTasks(src.wasm);
    for (const model of MODEL_SOURCES) {
      for (const delegate of ["GPU", "CPU"]) {
        try {
          return await vision.HandLandmarker.createFromOptions(fileset, {
            baseOptions: { modelAssetPath: model, delegate },
            runningMode: "VIDEO",
            numHands: 1,
            minHandDetectionConfidence: 0.5,
            minHandPresenceConfidence: 0.5,
            minTrackingConfidence: 0.5,
          });
        } catch (err) {
          lastError = err;
        }
      }
    }
  }
  throw lastError;
}

async function initTracking() {
  setStatus("loading");
  try {
    await startCamera();
  } catch (err) {
    console.warn("camera error", err);
    state.cameraError = true;
    body.dataset.camera = "error";
    setStatus("error");
    return;
  }
  try {
    landmarker = await loadLandmarker();
    state.modelReady = true;
    setStatus("noHand");
  } catch (err) {
    console.warn("hand model error", err);
    body.dataset.camera = "error";
    setStatus("modelError");
  }
}

function trackHands(now) {
  if (!landmarker || video.readyState < 2 || video.currentTime === lastVideoTime) return;
  lastVideoTime = video.currentTime;
  let result;
  try {
    result = landmarker.detectForVideo(video, now);
  } catch {
    return;
  }
  const hand = result.landmarks && result.landmarks[0];
  if (hand) {
    const tip = hand[8]; // 검지 끝
    state.lastHandAt = now;
    if (!state.handOn) {
      state.handOn = true;
      body.dataset.hand = "on";
    }
    feedPoint(1 - tip.x, tip.y, now); // 거울처럼 좌우 반전
  } else if (state.handOn && now - state.lastHandAt > 400) {
    state.handOn = false;
    body.dataset.hand = "off";
    history.length = 0;
    setProgress(0);
  }
  if (state.modelReady) setStatus(state.handOn ? "hand" : "noHand");
}

// ---------------------------------------------------------------------------
// 파티클
const particles = [];
const stars = [];
const MAX_PARTICLES = 700;

function resize() {
  DPR = Math.min(window.devicePixelRatio || 1, 2);
  W = window.innerWidth;
  H = window.innerHeight;
  for (const c of [bg, trailCanvas]) {
    c.width = W * DPR;
    c.height = H * DPR;
  }
  bgCtx.setTransform(DPR, 0, 0, DPR, 0, 0);
  trailCtx.setTransform(DPR, 0, 0, DPR, 0, 0);
  stars.length = 0;
  const n = Math.round((W * H) / 9000);
  for (let i = 0; i < n; i++) {
    stars.push({
      x: Math.random() * W,
      y: Math.random() * H,
      r: Math.random() * 1.4 + 0.2,
      p: Math.random() * Math.PI * 2,
      s: 0.5 + Math.random() * 1.5,
    });
  }
}
window.addEventListener("resize", resize);
resize();

const rand = (a, b) => a + Math.random() * (b - a);
const pickOne = (arr) => arr[(Math.random() * arr.length) | 0];

function addParticle(p) {
  if (particles.length >= MAX_PARTICLES) particles.shift();
  particles.push({ age: 0, rot: 0, vr: 0, ...p });
}

function circleCenter() {
  const r = circleWrap.getBoundingClientRect();
  return { x: r.left + r.width / 2, y: r.top + r.height / 2, r: r.width / 2 };
}

function spawnTrailSpark(x, y) {
  addParticle({
    kind: "spark",
    x, y,
    vx: rand(-0.4, 0.4),
    vy: rand(-0.6, 0.2),
    life: rand(0.5, 1.1),
    size: rand(1.5, 3.5),
    color: pickOne(["#fff3c4", "#f5d27a", "#c9b8ff"]),
  });
}

function spawnElement(key, x, y, burstMode = false) {
  const el = ELEMENTS[key];
  const color = pickOne(el.palette);
  if (burstMode) {
    const a = rand(0, Math.PI * 2);
    const sp = rand(2, 11);
    addParticle({ kind: key === "light" ? "star" : "spark", x, y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: rand(0.8, 2), size: rand(2, 6), color, drag: 0.96 });
    return;
  }
  switch (key) {
    case "fire":
      addParticle({ kind: "ember", x: rand(0, W), y: H + 10, vx: rand(-0.5, 0.5), vy: rand(-4, -1.5), life: rand(2, 4), size: rand(2, 6), color, wob: rand(0, 6) });
      break;
    case "water":
      addParticle({ kind: "bubble", x: rand(0, W), y: H + 20, vx: 0, vy: rand(-2.2, -0.8), life: rand(3, 6), size: rand(3, 12), color, wob: rand(0, 6) });
      break;
    case "earth":
      addParticle({ kind: "shard", x: rand(0, W), y: -20, vx: rand(-0.6, 0.6), vy: rand(1, 2.6), life: rand(4, 7), size: rand(4, 10), color, rot: rand(0, 6), vr: rand(-0.05, 0.05) });
      break;
    case "air":
      addParticle({ kind: "streak", x: -80, y: rand(0, H), vx: rand(6, 14), vy: 0, life: rand(1.5, 3), size: rand(40, 140), color, wob: rand(0, 6) });
      break;
    case "light": {
      const a = rand(0, Math.PI * 2);
      const sp = rand(0.6, 2.4);
      const c = revealCenter();
      addParticle({ kind: "star", x: c.x, y: c.y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, life: rand(2, 4), size: rand(2, 6), color });
      break;
    }
  }
}

function revealCenter() {
  const r = $(".reveal-symbol").getBoundingClientRect();
  return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
}

function burst(key) {
  const { x, y } = revealCenter();
  for (let i = 0; i < 180; i++) spawnElement(key, x, y, true);
}

function drawStar(ctx, x, y, r) {
  ctx.beginPath();
  for (let i = 0; i < 8; i++) {
    const a = (i * Math.PI) / 4;
    const rr = i % 2 === 0 ? r : r * 0.3;
    ctx.lineTo(x + Math.cos(a) * rr, y + Math.sin(a) * rr);
  }
  ctx.closePath();
  ctx.fill();
}

function updateParticles(dt, t) {
  const f = dt * 60;
  for (let i = particles.length - 1; i >= 0; i--) {
    const p = particles[i];
    p.age += dt;
    if (p.age >= p.life) {
      particles.splice(i, 1);
      continue;
    }
    if (p.drag) {
      p.vx *= Math.pow(p.drag, f);
      p.vy *= Math.pow(p.drag, f);
    }
    if (p.kind === "ember" || p.kind === "bubble") p.x += Math.sin(t * 2 + p.wob) * 0.6 * f;
    if (p.kind === "streak") p.y += Math.sin(t * 3 + p.wob) * 1.2 * f;
    p.x += p.vx * f;
    p.y += p.vy * f;
    p.rot += p.vr * f;
  }
}

function drawParticles(ctx) {
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  for (const p of particles) {
    const k = 1 - p.age / p.life;
    const alpha = Math.min(1, k * 1.5) * Math.min(1, p.age * 6);
    ctx.globalAlpha = alpha;
    ctx.fillStyle = p.color;
    ctx.strokeStyle = p.color;
    switch (p.kind) {
      case "bubble":
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(p.x - p.size * 0.35, p.y - p.size * 0.35, p.size * 0.2, 0, Math.PI * 2);
        ctx.fill();
        break;
      case "shard":
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rot);
        ctx.beginPath();
        ctx.moveTo(0, -p.size);
        ctx.lineTo(p.size * 0.8, p.size * 0.3);
        ctx.lineTo(-p.size * 0.2, p.size * 0.8);
        ctx.lineTo(-p.size * 0.7, -p.size * 0.1);
        ctx.closePath();
        ctx.fill();
        ctx.restore();
        break;
      case "streak": {
        const grad = ctx.createLinearGradient(p.x - p.size, p.y, p.x, p.y);
        grad.addColorStop(0, "rgba(255,255,255,0)");
        grad.addColorStop(1, p.color);
        ctx.strokeStyle = grad;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(p.x - p.size, p.y + Math.sin(p.wob) * 6);
        ctx.quadraticCurveTo(p.x - p.size / 2, p.y - 10, p.x, p.y);
        ctx.stroke();
        break;
      }
      case "star":
        drawStar(ctx, p.x, p.y, p.size * 1.6);
        break;
      default: {
        // ember / spark: 부드러운 빛 점
        const r = p.size * (p.kind === "ember" ? k : 1);
        const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r * 3);
        g.addColorStop(0, p.color);
        g.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(p.x, p.y, r * 3, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
  ctx.restore();
}

function drawStars(ctx, t) {
  ctx.fillStyle = "#fff";
  for (const s of stars) {
    ctx.globalAlpha = 0.25 + 0.55 * (0.5 + 0.5 * Math.sin(t * s.s + s.p));
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.globalAlpha = 1;
}

function drawTrail(ctx, now) {
  while (trail.length && now - trail[0].t > 450) trail.shift();
  if (trail.length < 2) return;
  ctx.save();
  ctx.globalCompositeOperation = "lighter";
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  for (let i = 1; i < trail.length; i++) {
    const a = trail[i - 1];
    const b = trail[i];
    const k = 1 - (now - b.t) / 450;
    ctx.strokeStyle = `rgba(245, 210, 122, ${0.5 * k})`;
    ctx.lineWidth = 18 * k;
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
    ctx.strokeStyle = `rgba(255, 255, 255, ${0.9 * k})`;
    ctx.lineWidth = 5 * k;
    ctx.stroke();
  }
  const tip = trail[trail.length - 1];
  const g = ctx.createRadialGradient(tip.x, tip.y, 0, tip.x, tip.y, 30);
  g.addColorStop(0, "rgba(255,255,255,0.95)");
  g.addColorStop(0.3, "rgba(245,210,122,0.6)");
  g.addColorStop(1, "rgba(245,210,122,0)");
  ctx.fillStyle = g;
  ctx.beginPath();
  ctx.arc(tip.x, tip.y, 30, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

// ---------------------------------------------------------------------------
// 메인 루프
let lastT = performance.now();
let spin = 0;
let spinSpeed = 6; // deg/s
let spawnAcc = 0;

function frame(now) {
  const dt = Math.min(0.05, (now - lastT) / 1000);
  lastT = now;
  const t = now / 1000;

  trackHands(now);

  // 마법진 회전: 시전 중에는 빠르게
  const targetSpeed = state.phase === "casting" ? 240 : 6;
  spinSpeed += (targetSpeed - spinSpeed) * Math.min(1, dt * 2.5);
  spin = (spin + spinSpeed * dt) % 360;
  ringOuter.setAttribute("transform", `rotate(${spin.toFixed(2)})`);
  ringInner.setAttribute("transform", `rotate(${(-spin * 0.6).toFixed(2)})`);

  // 원소 파티클 방출
  if (state.phase === "reveal" && state.pick) {
    const rate = { fire: 70, water: 30, earth: 22, air: 26, light: 45 }[state.pick];
    spawnAcc += rate * dt;
    while (spawnAcc >= 1) {
      spawnElement(state.pick);
      spawnAcc -= 1;
    }
    if (now - state.revealAt > NEXT_READY_MS && body.dataset.nextReady !== "on") body.dataset.nextReady = "on";
  } else if (state.phase === "casting") {
    // 마법진으로 빨려드는 기운
    const c = circleCenter();
    for (let i = 0; i < 4; i++) {
      const a = rand(0, Math.PI * 2);
      const r = c.r * rand(1.1, 1.8);
      const x = c.x + Math.cos(a) * r;
      const y = c.y + Math.sin(a) * r;
      addParticle({ kind: "spark", x, y, vx: (c.x - x) / 40, vy: (c.y - y) / 40, life: 0.7, size: rand(1.5, 3.5), color: pickOne(["#fff", "#f5d27a", "#c9b8ff"]) });
    }
  }

  updateParticles(dt, t);

  bgCtx.clearRect(0, 0, W, H);
  drawStars(bgCtx, t);
  drawParticles(bgCtx);

  trailCtx.clearRect(0, 0, W, H);
  if (state.phase !== "casting") drawTrail(trailCtx, now);

  requestAnimationFrame(frame);
}
requestAnimationFrame(frame);

// ---------------------------------------------------------------------------
// 시작
$("#start-btn").addEventListener("click", () => {
  sfx.init();
  document.documentElement.requestFullscreen?.().catch(() => {});
  setPhase("idle");
  initTracking();
});

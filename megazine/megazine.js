/* Me-gazine 2026 — 편집 · 저장 · 인쇄
   - 글: .ed 요소를 눌러 바로 입력 → localStorage에 자동 저장
   - 사진: .photo 칸을 눌러 파일 선택 → 크기를 줄여 IndexedDB에 저장
   - 이름: 도구 막대의 이름을 바꾸면 .js-name 전체가 함께 바뀜
   - 내보내기/불러오기: 글+사진을 JSON 파일 하나로 옮길 수 있음 */
(() => {
  const PREFIX = 'megazine2026:';
  const NAME_KEY = PREFIX + 'name';
  const DEFAULT_NAME = 'ㅇㅇㅇ';

  const ls = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch {} },
    del(k) { try { localStorage.removeItem(k); } catch {} },
  };

  /* ── IndexedDB (사진) ── */
  const idb = (() => {
    let dbp;
    const open = () => dbp ||= new Promise((res, rej) => {
      const r = indexedDB.open('megazine2026', 1);
      r.onupgradeneeded = () => r.result.createObjectStore('img');
      r.onsuccess = () => res(r.result);
      r.onerror = () => rej(r.error);
    });
    const tx = async (mode, fn) => {
      const db = await open();
      return new Promise((res, rej) => {
        const t = db.transaction('img', mode);
        const req = fn(t.objectStore('img'));
        t.oncomplete = () => res(req && req.result);
        t.onerror = () => rej(t.error);
      });
    };
    return {
      get: k => tx('readonly', s => s.get(k)).catch(() => null),
      set: (k, v) => tx('readwrite', s => s.put(v, k)).catch(() => {}),
      del: k => tx('readwrite', s => s.delete(k)).catch(() => {}),
      clear: () => tx('readwrite', s => s.clear()).catch(() => {}),
    };
  })();

  /* ── 이름 ── */
  const nameInput = document.getElementById('nameInput');
  const applyName = n => {
    const v = (n || '').trim() || DEFAULT_NAME;
    document.querySelectorAll('.js-name').forEach(el => { el.textContent = v; });
    // 받침 유무에 따라 조사 고르기 (을/를, 이가/가)
    const c = v.charCodeAt(v.length - 1);
    const batchim = c >= 0xAC00 && c <= 0xD7A3 ? (c - 0xAC00) % 28 !== 0 : true;
    document.querySelectorAll('.js-josa').forEach(el => {
      const j = el.dataset.j;
      el.textContent = j === '이가' ? (batchim ? '이가' : '가') : (batchim ? j[0] : j[1]);
    });
    document.title = `Me-gazine 2026 · ${v}`;
  };
  nameInput.value = ls.get(NAME_KEY) || '';
  applyName(nameInput.value);
  nameInput.addEventListener('input', () => { ls.set(NAME_KEY, nameInput.value); applyName(nameInput.value); });

  /* ── 글 칸 ── */
  const edits = [...document.querySelectorAll('.ed')];
  edits.forEach((el, i) => {
    const key = PREFIX + 't' + i;
    el.dataset.key = key;
    try { el.contentEditable = 'plaintext-only'; } catch { el.contentEditable = 'true'; }
    if (el.contentEditable !== 'plaintext-only') el.contentEditable = 'true';
    el.spellcheck = false;
    const saved = ls.get(key);
    if (saved) el.innerText = saved;
    el.addEventListener('input', () => {
      const text = el.innerText.replace(/\n$/, '');
      if (!text.trim()) { el.innerHTML = ''; ls.del(key); } else ls.set(key, text);
    });
    el.addEventListener('paste', e => {          // 서식 없이 붙여넣기
      if (el.contentEditable === 'plaintext-only') return;
      e.preventDefault();
      document.execCommand('insertText', false, e.clipboardData.getData('text/plain'));
    });
  });

  /* ── 사진 칸 ── */
  const picker = document.createElement('input');
  picker.type = 'file'; picker.accept = 'image/*'; picker.hidden = true;
  document.body.appendChild(picker);
  let target = null;

  const setImg = (el, url) => {
    if (url) { el.style.setProperty('--img', `url("${url}")`); el.classList.add('has-img'); }
    else { el.style.removeProperty('--img'); el.classList.remove('has-img'); }
  };

  const shrink = file => new Promise((res, rej) => {
    const img = new Image();
    img.onload = () => {
      const max = 1600, s = Math.min(1, max / Math.max(img.width, img.height));
      const c = document.createElement('canvas');
      c.width = Math.round(img.width * s); c.height = Math.round(img.height * s);
      c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
      URL.revokeObjectURL(img.src);
      res(c.toDataURL('image/jpeg', 0.86));
    };
    img.onerror = rej;
    img.src = URL.createObjectURL(file);
  });

  const photos = [...document.querySelectorAll('.photo')];
  photos.forEach((el, i) => {
    const key = 'p' + i;
    el.dataset.key = key;
    el.title = '눌러서 사진 넣기';
    const clear = document.createElement('button');
    clear.type = 'button'; clear.className = 'clear-btn'; clear.textContent = '×'; clear.title = '사진 지우기';
    clear.addEventListener('click', e => { e.stopPropagation(); setImg(el, null); idb.del(key); });
    el.appendChild(clear);
    el.addEventListener('click', () => { target = el; picker.value = ''; picker.click(); });
    idb.get(key).then(url => url && setImg(el, url));
  });

  picker.addEventListener('change', async () => {
    const f = picker.files[0];
    if (!f || !target) return;
    try {
      const url = await shrink(f);
      setImg(target, url);
      await idb.set(target.dataset.key, url);
    } catch { alert('사진을 불러오지 못했어요. 다른 사진으로 시도해 주세요.'); }
  });

  /* ── 내보내기 / 불러오기 / 초기화 / 인쇄 ── */
  document.getElementById('btnExport').addEventListener('click', async () => {
    const data = { v: 1, name: nameInput.value, text: {}, img: {} };
    edits.forEach(el => { const t = ls.get(el.dataset.key); if (t) data.text[el.dataset.key.slice(PREFIX.length)] = t; });
    for (const el of photos) { const u = await idb.get(el.dataset.key); if (u) data.img[el.dataset.key] = u; }
    const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `megazine-${(nameInput.value || 'me').trim()}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 1000);
  });

  const importFile = document.getElementById('importFile');
  document.getElementById('btnImport').addEventListener('click', () => { importFile.value = ''; importFile.click(); });
  importFile.addEventListener('change', async () => {
    const f = importFile.files[0];
    if (!f) return;
    try {
      const data = JSON.parse(await f.text());
      nameInput.value = data.name || ''; ls.set(NAME_KEY, nameInput.value); applyName(nameInput.value);
      edits.forEach(el => {
        const t = data.text?.[el.dataset.key.slice(PREFIX.length)];
        if (t) { el.innerText = t; ls.set(el.dataset.key, t); } else { el.innerHTML = ''; ls.del(el.dataset.key); }
      });
      for (const el of photos) {
        const u = data.img?.[el.dataset.key];
        setImg(el, u || null);
        if (u) await idb.set(el.dataset.key, u); else await idb.del(el.dataset.key);
      }
    } catch { alert('불러올 수 없는 파일이에요.'); }
  });

  document.getElementById('btnReset').addEventListener('click', async () => {
    if (!confirm('입력한 글과 사진을 모두 지울까요? (되돌릴 수 없어요)')) return;
    edits.forEach(el => { el.innerHTML = ''; ls.del(el.dataset.key); });
    photos.forEach(el => setImg(el, null));
    await idb.clear();
    nameInput.value = ''; ls.del(NAME_KEY); applyName('');
  });

  document.getElementById('btnPrint').addEventListener('click', () => window.print());

  /* ── 작은 화면에서 페이지 크기 맞추기 ── */
  const PAGE_PX = 210 * 96 / 25.4;
  const fit = () => {
    const s = Math.min(1, (window.innerWidth - 32) / PAGE_PX);
    document.documentElement.style.setProperty('--fit', s.toFixed(4));
  };
  fit();
  window.addEventListener('resize', fit);
})();

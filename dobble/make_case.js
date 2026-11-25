// case/small.html -> case/*.jpg (800x800)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 800, height: 800 } });
  await p.goto('file://' + path.resolve(__dirname, 'case/small.html'));
  await p.waitForLoadState('networkidle');
  for (const el of await p.$$('.sq')) {
    const id = await el.getAttribute('id');
    await el.screenshot({ path: path.resolve(__dirname, `case/${id}.jpg`), type: 'jpeg', quality: 95 });
  }
  await b.close();
  console.log('케이스 이미지 저장 완료');
})();

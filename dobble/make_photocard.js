// photocard.html -> photocard/front_01.png ... front_57.png, back.png (300dpi, 874x1110px)
// node make_photocard.js [미리보기 폴더]
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const DPI = 300;
const PX_W = Math.round(74 / 25.4 * DPI);   // 874
const PX_H = Math.round(94 / 25.4 * DPI);   // 1110

(async () => {
  const out = path.resolve(__dirname, 'photocard');
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1200 }, deviceScaleFactor: DPI / 96 });
  await page.goto('file://' + path.resolve(__dirname, 'photocard.html'));
  await page.waitForLoadState('networkidle');
  const cards = await page.$$('.pc');
  for (const c of cards) {
    const id = await c.getAttribute('id');
    const file = path.join(out, id + '.png');
    await c.screenshot({ path: file });
  }
  // 화면 좌표의 소수점 때문에 1~6px 차이가 나므로 정확한 크기(300dpi)로 맞추고 dpi 정보를 넣는다
  const { execSync } = require('child_process');
  const sizes = execSync(`python3 -c "
import glob
from PIL import Image
for f in glob.glob('${out}/*.png'):
    im = Image.open(f).convert('RGB').resize((${PX_W}, ${PX_H}), Image.LANCZOS)
    im.save(f, dpi=(${DPI}, ${DPI}))
print(sorted({Image.open(f).size for f in glob.glob('${out}/*.png')}))
"`).toString().trim();
  console.log(`${cards.length}개 저장 (목표 ${PX_W}x${PX_H}px):`, sizes);
  if (process.argv[2]) {
    // 재단선(빨강)·안전선(파랑) 표시한 미리보기
    await page.evaluate(() => document.body.classList.add('guides'));
    await page.setViewportSize({ width: 1200, height: 900 });
    for (const id of ['back', 'front_01', 'front_02', 'front_05']) {
      await (await page.$('#' + id)).screenshot({ path: path.join(process.argv[2], `pc_${id}.png`), scale: 'css' });
    }
  }
  await browser.close();
})();

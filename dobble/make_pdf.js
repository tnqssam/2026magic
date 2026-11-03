// print.html -> dobble_cards_duplex.pdf, guide.html -> dobble_guide.pdf (+ 미리보기 PNG)
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  for (const [src, out] of [['print.html', 'dobble_cards_duplex.pdf'], ['guide.html', 'dobble_guide.pdf']]) {
    await page.goto('file://' + path.resolve(__dirname, src));
    await page.waitForLoadState('networkidle');
    await page.pdf({ path: path.resolve(__dirname, out), format: 'A4', printBackground: true });
    if (process.argv[2] && src === 'print.html') {
      const s = await page.$$('section');
      for (const i of [0, 1, 18, 19]) await s[i].screenshot({ path: path.join(process.argv[2], `duplex${i + 1}.png`) });
    }
    console.log(out + ' 저장 완료');
  }
  await browser.close();
})();

// print.html -> dobble_cards.pdf (+ 미리보기 PNG)
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(__dirname, 'print.html'));
  await page.pdf({ path: path.resolve(__dirname, 'dobble_cards.pdf'), format: 'A4', printBackground: true });
  if (process.argv[2]) {
    const sections = await page.$$('section');
    for (const i of [0, 1]) await sections[i].screenshot({ path: path.join(process.argv[2], `page${i + 1}.png`) });
  }
  await browser.close();
  console.log('dobble_cards.pdf 저장 완료');
})();

// Gera as cenas de design/telas.html em PNG (2x). Uso: node design/render.js <pasta-saida>
const { chromium } = require('playwright');
const path = require('path');
const out = process.argv[2] || '.';
const cenas = [
  ['dash','s=dash'], ['relatorios','s=relatorios'], ['perfis','s=perfis'], ['importacao','s=importacao'],
  ['phone-prod','s=phone&h=850'], ['tablet-prod','s=tablet&w=1260&h=801'],
];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 }, deviceScaleFactor: 2 });
  // tela da hero (arquivo próprio)
  await p.setViewportSize({ width: 1334, height: 834 });
  await p.goto('file://' + path.join(__dirname, 'dashboard-tela.html'), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(400);
  await p.screenshot({ path: path.join(out, 'hero-tela.png') });
  await p.setViewportSize({ width: 1400, height: 1000 });
  for (const [nome, q] of cenas) {
    await p.goto('file://' + path.join(__dirname, 'telas.html') + '?' + q, { waitUntil: 'networkidle' });
    await p.waitForSelector('body[data-pronto]');
    await p.waitForTimeout(300);
    await (await p.$('#scene')).screenshot({ path: path.join(out, nome + '.png'), omitBackground: true });
  }
  await b.close();
})();

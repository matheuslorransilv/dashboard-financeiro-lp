# Design das imagens

As telas do dashboard na identidade azul são geradas a partir de HTML.

- `dashboard-tela.html`: tela do MacBook da hero (`assets/img/hero-azul.webp`)
- `telas.html`: demais telas (cards da assinatura, tablet e celulares). Cada cena abre com `?s=dash|relatorios|perfis|importacao|phone|tablet`
- `render.js`: captura as cenas de `telas.html` em PNG 2x
- `compor.py`: redimensiona as cenas e encaixa nas molduras de `molduras/` (tablet e celular originais)

Para regenerar:

```bash
node design/render.js /tmp/cenas
python3 design/compor.py /tmp/cenas design/molduras assets/img
```

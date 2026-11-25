"""Monta as imagens finais da LP a partir das cenas renderizadas por render.js.
Uso: python3 design/compor.py <pasta-das-cenas> design/molduras assets/img
As molduras de aparelho (tablet, celular, MacBook com vídeo) vêm das imagens originais."""
import sys
from PIL import Image, ImageDraw
R, ORIG, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
L = Image.LANCZOS

def mascara(w, h, r, s=4):
    m = Image.new('L', (w*s, h*s), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w*s-1, h*s-1), r*s, fill=255)
    return m.resize((w, h), L)

def tela(base, cena, x, y, w, h, r, corte=None):
    img = Image.open(f'{R}/{cena}.png').convert('RGBA').resize((w, h), L)
    m = mascara(w, h, r)
    if corte:  # tablet que continua por baixo do celular: corta em x=corte e só arredonda os cantos da esquerda
        cx = corte - x
        img = img.crop((0, 0, cx, h))
        m = m.crop((0, 0, cx, h))
        m.paste(255, (cx // 2, 0, cx, h))
    base.paste(img, (x, y), m)

# cards da oferta (sem moldura)
for n, arq in [('dash', 'offer-dashboard'), ('relatorios', 'offer-relatorios'), ('perfis', 'offer-perfis'), ('importacao', 'offer-importacao')]:
    Image.open(f'{R}/{n}.png').convert('RGBA').resize((1300, 932), L).save(f'{OUT}/{arq}-azul.webp', quality=92, method=6)

# tablet + celular
b = Image.open(f'{ORIG}/produto.webp').convert('RGBA')
tela(b, 'tablet-prod', 183, 241, 900, 572, 17, corte=970)
sombra = Image.new('RGBA', (26, 572), (0, 0, 0, 0))
for i in range(26):
    ImageDraw.Draw(sombra).line([(i, 0), (i, 571)], fill=(13, 22, 48, int(34 * (i / 25) ** 2)))
b.alpha_composite(sombra, (944, 241))
tela(b, 'phone-prod', 987, 167, 339, 739, 40)
b.save(f'{OUT}/produto-azul.webp', quality=92, method=6)

# aulas: celular + tablet sobre o MacBook com o vídeo
a = Image.open(f'{ORIG}/offer-aulas.webp').convert('RGBA')
tela(a, 'phone-aulas', 189, 101, 215, 471, 34)
tela(a, 'tablet-aulas', 858, 516, 392, 253, 10)
a.save(f'{OUT}/offer-aulas-azul.webp', quality=92, method=6)

from mandelbrot_zoom import generarImagenSector
import colorsys
from PIL import Image

def color_a_iter(r, g, b, max_iter):
    """
    Inverteix el teu esquema de color a un valor d'iteració n aproximat.
    Retorna un enter 0..max_iter, o None si no s'hi pot mapear amb confiança.
    """
    # normalitzar a [0,1]
    rf, gf, bf = r/255.0, g/255.0, b/255.0

    # cas negre pur (dins del conjunt)
    if r < 10 and g < 10 and b < 10:
        return max_iter

    # convertir a HSV
    h, s, v = colorsys.rgb_to_hsv(rf, gf, bf)

    # Tram 1: blanc -> vermell (t in [0,0.1])
    # En el teu codi: hsv(0, ratio, 1.0) amb ratio = t/0.1 -> s = ratio, v = 1
    if abs(v - 1.0) < 1e-9 and h < 1e-6 and s <= 1.0:
        # si és blanc pur s≈0? blanc pur té s=0, v=1 -> t=0
        # si és vermell pàl·lid s entre 0..1 amb h≈0
        t = s * 0.1
        return int(t * max_iter)

    # Tram 2: arc de Sant Martí (t in [0.1,0.9])
    # hsv(hue, 1.0, 1.0) amb hue = (t-0.1)/0.8
    if abs(v - 1.0) < 1e-9 and abs(s - 1.0) < 1e-9:
        t = h * 0.8 + 0.1
        return int(t * max_iter)

    # Tram 3: colors -> negre (t in [0.9,1.0])
    # hsv(1.0,1.0, 1.0 - ratio) amb ratio = (t-0.9)/0.1
    # En HSV, hue=0 o 1 per vermell; detectem per h≈0, s≈1 i v<1
    if (h < 1e-6 or h > 0.999999) and abs(s - 1.0) < 1e-6 and v < 1.0:
        ratio = 1.0 - v
        t = ratio * 0.1 + 0.9
        return int(t * max_iter)

    # Si no encaixa clarament, retornem None (tractar com a "interessant")
    return None

def es_inutil_iters(ruta, max_iter=100, umbral=0.90):
    """
    Retorna True si la imatge a `ruta` és inútil:
      - > umbral píxels amb n == max_iter (negres)  OR
      - > umbral píxels amb n < 0.1*max_iter (llunyans: blanc/rosa/vermell pàl·lid)
    Si no es pot inferir el color->iter per un píxel, es considera 'interessant'.
    """
    img = Image.open(ruta).convert("RGB")
    w, h = img.size
    total = w * h

    negres = 0
    llunyans = 0

    data = img.tobytes()  # bytes plans R,G,B,R,G,B,...
    # recorrem de 3 en 3
    for i in range(0, len(data), 3):
        r = data[i]
        g = data[i+1]
        b = data[i+2]

        n = color_a_iter(r, g, b, max_iter)
        if n is None:
            # no podem inferir: tractem com a interessant (no incrementem cap comptador)
            continue

        if n == max_iter:
            negres += 1
        elif n < max_iter * 0.1:
            llunyans += 1

    # percentatges
    if negres / total > umbral:
        return True
    if llunyans / total > umbral:
        return True
    return False

def recursivePreRender(reps):
    if reps == 0:
        return
    
    cc = 2**reps

    for x in range(cc):
        for y in range(cc):
            _, ruta = generarImagenSector(x, y, reps)
            if es_inutil_iters(ruta):
                continue
    
    recursivePreRender(reps-1)





if __name__ == '__main__':
    reps = int(input("Nombre de capes renderitzades: "))
    recursivePreRender(reps)

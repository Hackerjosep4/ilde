from PIL import Image
import colorsys





import ctypes
import os

# Carregar la DLL (assegura't que està al mateix directori)
dll_path = os.path.join(os.path.dirname(__file__), "mandelbrot.dll")
lib = ctypes.CDLL(dll_path)

# Definir tipus d'arguments i retorn
lib.mandelbrot_iter.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_int]
lib.mandelbrot_iter.restype = ctypes.c_int

def mandelbrot_iter(a, b, max_iter=100):
    return lib.mandelbrot_iter(a, b, max_iter)










def calcula_color(n, max_iter):
    """
    Degradat: Blanc → Arc de Sant Martí → Negre
    """
    if n == max_iter:
        return (0, 0, 0)  # Negre (dins del conjunt)
    
    # Normalitzar entre 0 i 1
    t = n / max_iter
    
    if t < 0.1:
        # Transició de blanc a colors (10% inicial)
        ratio = t / 0.1
        r, g, b = colorsys.hsv_to_rgb(0, ratio, 1.0)
    elif t < 0.9:
        # Arc de Sant Martí (80% central)
        hue = (t - 0.1) / 0.8  # De 0 a 1
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
    else:
        # Transició de colors a negre (10% final)
        ratio = (t - 0.9) / 0.1
        r, g, b = colorsys.hsv_to_rgb(1.0, 1.0, 1.0 - ratio)
    
    return (int(r * 255), int(g * 255), int(b * 255))

def calcula_color_ocean(n, max_iter):
    if n == max_iter:
        return (0, 0, 50)  # Blau molt fosc
    
    t = n / max_iter
    r = int(50 * t)
    g = int(150 * t)
    b = int(200 + 55 * t)
    
    return (r, g, b)

def calcula_color_inferno(n, max_iter):
    if n == max_iter:
        return (0, 0, 0)
    
    t = n / max_iter
    r = int(255 * min(1, t * 2.5))
    g = int(255 * max(0, (t - 0.3) * 2))
    b = int(255 * max(0, (t - 0.7) * 3))
    
    return (r, g, b)



# Crear imatge (mode RGB)
def mandelbrot(escala=1.0, max_iter=100, xmin=-2, xmax=1, ymin=-1.5, ymax=1.5, color_func = calcula_color):

    amplada = int(1000*escala)
    alcada = int(1000*escala)

    imatge = Image.new('RGB', (amplada, alcada))

    for x in range(amplada):
        print(f'{(x)/amplada*100:.2f}% completat', end='\r')
        for y in range(alcada):
            # Convertim píxel a nombre complex
            a = xmin + (x / amplada) * (xmax - xmin)
            b = ymax - (y / alcada) * (ymax - ymin)
            # c = complex(a, b)

            # z = 0
            # n = 0
            # while abs(z) <= 2 and n < max_iter:
            #     z = z*z + c
            #     n += 1

            n = mandelbrot_iter(a, b, max_iter)

            # Assignar color segons iteracions
            color = color_func(n, max_iter)
            imatge.putpixel((x, y), color)
    print('100.00% completat')
    
    return imatge


if __name__ == '__main__':
    # Paràmetres
    # max_iter = 100
    # escala = 1.0
    max_iter = int(input("Màxim d'iteracions: ") or 100)
    escala = float(input("Escala (1 per defecte): ").replace(',', '.') or 1)

    # Rang del pla complex
    # xmin, xmax = -2, 1
    # ymin, ymax = -1.5, 1.5
    xmin = float(input("xmin (per defecte -2): ").replace(',', '.') or -2)
    xmax = float(input("xmax (per defecte 1): ").replace(',', '.') or 1)
    ymin = float(input("ymin (per defecte -1.5): ").replace(',', '.') or -1.5)
    ymax = float(input("ymax (per defecte 1.5): ").replace(',', '.') or 1.5)


    img = mandelbrot(escala, max_iter, xmin, xmax, ymin, ymax, calcula_color)
    img.save(f'mandelbrot_x{escala}_{max_iter}iter_{xmin}-{xmax}_{ymin}-{ymax}.png')
    img.show()

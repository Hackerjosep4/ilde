from PIL import Image
import colorsys
import ctypes
import os
import numpy as np  

# Carregar la DLL (assegura't que està al mateix directori)
dll_path = os.path.join(os.path.dirname(__file__), "mandelbrot.dll")
lib = ctypes.CDLL(dll_path)

# Definir tipus d'arguments i retorn
lib.mandelbrot_grid.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
lib.mandelbrot_grid.restype = ctypes.POINTER(ctypes.c_int)
lib.free_grid.argtypes = [ctypes.POINTER(ctypes.c_int)]

def mandelbrot_grid(amplada, alcada, max_iter, xmin, xmax, ymin, ymax):
    return lib.mandelbrot_grid(amplada, alcada, max_iter, xmin, xmax, ymin, ymax)

def free_grid(grid):
    lib.free_grid(grid)







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


def hsv_to_rgb_np(h, s, v):
    """Versió numpy de colorsys.hsv_to_rgb, funciona amb matrius"""
    i = (h * 6).astype(int)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = i % 6

    r = np.select([i==0, i==1, i==2, i==3, i==4, i==5], [v, q, p, p, t, v])
    g = np.select([i==0, i==1, i==2, i==3, i==4, i==5], [t, v, v, q, p, p])
    b = np.select([i==0, i==1, i==2, i==3, i==4, i==5], [p, p, t, v, v, q])
    return r, g, b

def grid_a_imatge(grid, max_iter):
    t = grid / max_iter

    r = np.zeros_like(t)
    g = np.zeros_like(t)
    b = np.zeros_like(t)

    dins  = (grid == max_iter)
    zona1 = (t < 0.1) & ~dins
    zona2 = (t >= 0.1) & (t < 0.9) & ~dins
    zona3 = (t >= 0.9) & ~dins

    # Zona 1: blanc → colors
    ratio = t[zona1] / 0.1
    r[zona1], g[zona1], b[zona1] = hsv_to_rgb_np(
        np.zeros_like(ratio), ratio, np.ones_like(ratio)
    )

    # Zona 2: arc de sant martí
    hue = (t[zona2] - 0.1) / 0.8
    r[zona2], g[zona2], b[zona2] = hsv_to_rgb_np(
        hue, np.ones_like(hue), np.ones_like(hue)
    )

    # Zona 3: colors → negre
    ratio = (t[zona3] - 0.9) / 0.1
    r[zona3], g[zona3], b[zona3] = hsv_to_rgb_np(
        np.ones_like(ratio), np.ones_like(ratio), 1.0 - ratio
    )

    # dins → negre (ja és 0 per defecte)

    rgb = np.stack([r, g, b], axis=-1)
    rgb = (rgb * 255).astype(np.uint8)
    return Image.fromarray(rgb)



# Crear imatge (mode RGB)
def mandelbrot(escala=1.0, max_iter=100, xmin=-2, xmax=1, ymin=-1.5, ymax=1.5):

    amplada = int(1000*escala)
    alcada = int(1000*escala)

    imatge = Image.new('RGB', (amplada, alcada))

    ptr = mandelbrot_grid(amplada, alcada, max_iter, xmin, xmax, ymin, ymax)
    grid = np.ctypeslib.as_array(ptr, shape=(alcada * amplada,)).reshape((alcada, amplada))
    imatge = grid_a_imatge(grid, max_iter)
    free_grid(ptr)

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

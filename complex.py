import matplotlib.pyplot as plt

# Paràmetres
amplada = 800
alcada = 800
max_iter = 100

# Rang del pla complex
xmin, xmax = -2, 1
ymin, ymax = -1.5, 1.5

mandelbrot = [[0]*amplada for _ in range(alcada)]

for x in range(amplada):
    for y in range(alcada):
        # Convertim píxel a nombre complex
        a = xmin + (x / amplada) * (xmax - xmin)
        b = ymin + (y / alcada) * (ymax - ymin)
        c = complex(a, b)

        z = 0
        n = 0
        while abs(z) <= 2 and n < max_iter:
            z = z*z + c
            n += 1

        mandelbrot[y][x] = n

# Representació
plt.imshow(mandelbrot, cmap="inferno")
plt.colorbar(label="Iteracions")
plt.title("Conjunt de Mandelbrot")
plt.show()

from mandelbrot import mandelbrot

dst = 3
inx = -2
iny = -1.5

img = None

while True:
    img = mandelbrot(0.5, 100, inx, inx+dst, iny, iny+dst)
    img.save(f"mdbt_zoom_{inx:.3f}_{iny:.3f}_{dst:.3f}.png")
    img.show()
    cc = int(input("Tamany de c de la cuadricula (0 per sortir): ") or 1)
    if cc == 0:
        break
    sx = float(input("Coordenada x de la cuadricula: ") or 0)-1
    sy = float(input("Coordenada y de la cuadricula: ") or 0)-1
    tm = float(input("Cantitat de cuadrats de la cuadricala agafats: ") or 1)
    dst = dst / cc * tm
    inx = inx + sx * dst
    iny = iny + sy * dst
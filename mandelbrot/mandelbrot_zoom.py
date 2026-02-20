from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import filedialog
import os
import re
from mandelbrot import mandelbrot


def mostrar_imagen(root, ruta):
    for widget in root.winfo_children():
        widget.destroy()
    imgtk = ImageTk.PhotoImage(Image.open(ruta))
    root.img_ref = imgtk
    tk.Label(root, image=imgtk).pack()
    # tk.Label(root, image=ImageTk.PhotoImage(Image.open(ruta))).pack()

def validar_imagen(ruta):
    # Comprobar si el archivo existe
    if not os.path.exists(ruta):
        return False
    try:
        # Intentar abrir la imagen
        with Image.open(ruta) as img:
            # Comprobar tamaño exacto
            return img.size == (500, 500)
    except Exception:
        # Si no se puede abrir como imagen, también es inválida
        return False

def generarImagen(inx, iny, dst):
    ruta = f"mdbt_zoom_{inx}_{iny}_{dst}.png"
    if validar_imagen(ruta):
        return Image.open(ruta), ruta
    else:
        img = mandelbrot(0.5, 100, inx, inx+dst, iny, iny+dst)
        img.save(ruta)
        return img, ruta

def generarOverlay(cc, sx, sy, tm):
    imgc = Image.new("RGBA", (500,500), (0,0,0,0))
    imgcd = ImageDraw.Draw(imgc)
    tc = 500 / cc
    x1 = (sx - 1) * tc
    x2 = x1 + tm * tc
    y1 = (cc - tm - (sy - 1)) * tc
    y2 = (cc - sy + 1) * tc
    imgcd.rectangle((x1, y1, x2, y2), fill=(0,255,0,100))
    for i in range(1, cc):
        pas = (500*i)//cc
        #print(f"Pas: {pas}")
        imgcd.line((pas, 0, pas, 500), fill=(255, 0, 0, 100))
        imgcd.line((0, pas, 500, pas), fill=(255, 0, 0, 100))
    return imgc

def actualizarOverlay(root, img, cc, sx, sy, tm):
    imgc = Image.alpha_composite(img.convert("RGBA"), generarOverlay(cc, sx, sy, tm))
    imgc.save("temp.png")
    mostrar_imagen(root, "temp.png")

def loadImagen():
    while True:
        ruta = filedialog.askopenfilename( title="Selecciona un arxiu PNG", filetypes=[("Imatges PNG", "*.png")] )
        if ruta and validar_imagen(ruta):
            nom = os.path.basename(ruta)
            patron = r"^mdbt_zoom_([-+]?\d*\.?\d+)_([-+]?\d*\.?\d+)_([-+]?\d*\.?\d+)\.png$"
            m = re.match(patron, nom)
            if not m:
                continue
            inx, iny, dst = map(float, m.groups())
            img = Image.open(ruta)
            img.save(nom)
            return img, nom, inx, iny, dst
                


if __name__ == '__main__':

    root = tk.Tk()

    dst = 3
    inx = -2
    iny = -1.5

    cc = 1
    sx = 1
    sy = 1
    tm = 1

    img = None

    menu = "r"


    while menu != "s":
        if menu == "c":
            cc = int(input("Tamany de costat de la quadricula: ") or 1)
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif menu == "x":
            sx = float(input("Coordenada x de la quadricula: ") or 1)
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif menu == "y":
            sy = float(input("Coordenada y de la quadricula: ") or 1)
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif menu == "t":
            tm = float(input("Cantitat de cuadrats de la cuadricala agafats: ") or 1)
            actualizarOverlay(root, img, cc, sx, sy, tm)
        elif menu == "r":
            tc = dst / cc
            inx = inx + ((sx-1) * tc)
            iny = iny + ((sy-1) * tc)
            dst = tc * tm
            img, ruta = generarImagen(inx, iny, dst)
            mostrar_imagen(root, ruta)
            cc = 1
            sx = 1
            sy = 1
            tm = 1
        elif menu == "o":
            img, ruta, inx, iny, dst = loadImagen()
            mostrar_imagen(root, ruta)
            cc = 1
            sx = 1
            sy = 1
            tm = 1
        menu = input(f"\n\nDades:\nCuadricula: {cc}\nX: {sx}\nY: {sy}\nTamany: {tm}\nMenu:\nC - Cuadricula\nX - Set x\nY - Set y\nT - Set tamany\nR - Renderitzar\nO - Obrir imatge\nAccio: ").lower()

if os.path.exists("temp.png"):
    os.remove("temp.png")


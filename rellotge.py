import turtle as t

def rellotge():
    t.penup()
    t.left(90)
    t.forward(200)
    t.right(90)
    t.pendown()
    for i in range(12):
        t.circle(-200, 30)
        t.right(90)
        t.forward(50)
        t.back(50)
        t.left(90)
    t.penup()
    t.right(90)
    t.forward(200)
    t.left(90)
    t.pendown()

def agulla(tamany, angle):
    t.left(90)
    t.right(angle)
    t.forward(tamany)
    t.begin_fill()
    t.right(150)
    t.forward(25)
    t.right(120)
    t.forward(25)
    t.right(120)
    t.forward(25)
    t.end_fill()
    t.right(150)
    t.forward(tamany)
    t.right(180)
    t.left(angle)
    t.right(90)




h = int(input("Hores: "))
m = int(input("Minuts: "))

t.speed(0)

rellotge()
agulla(90, (30*h)+(0.5 * m))
agulla(140, (6*m))

input()
from turtle import *



def dibFrac(n, c):
  cp2 = c/2
  move(-cp2,-cp2)
  fillcolor("Black")
  dibQua(c)
  move(cp2,cp2)
  fillcolor("White")
  pasFrac(n, c/3)
  

def pasFrac(n, c):
  cp2 = c/2
  if n >=1:
    move(-cp2,-cp2)
    dibQua(c)
    move(cp2,cp2)
  if n >=2:
    cp3 = c/3
    for i in range(-1,2):
      for j in range(-1,2):
        if i==0 and j==0:
          continue
        move(c*i,c*j)
        pasFrac(n-1, cp3)
        move(-c*i,-c*j)

def dibQua(c):
  begin_fill()
  for i in range(4):
    forward(c)
    left(90)
  end_fill()

def move(x, y):
  goto(pos()[0]+x,pos()[1]+y)



penup()
goto(0,0)
speed(0)

reps = int(input("Introdueix el numero de repeticions: "))

dibFrac(reps, 387.420489)
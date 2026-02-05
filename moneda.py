from random import random

reps = int(input("Cuants estudis vols fer? "))

winsDoble = 0

for i in range(reps):
    # print(f"{i/reps*100:.2f}%", end="\r")
    m1 = random() < 0.5
    m2 = random() < 0.5
    if m1 and m2:
        winsDoble += 1
# print("100.00%")

print(f"+,+: {winsDoble/reps:.2f}%")
print(f"-,+: {(reps - winsDoble)/reps:.2f}%")
print(f"Cara + Cara: {winsDoble/reps}%")
print(f"Creu + Cara: {(reps - winsDoble)/reps}%")

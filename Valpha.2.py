from tkinter import *
from random import randint
from time import sleep
from math import *

########### Environment Data ###########
basin = {'height': 700, 'width': 700}
food_amount = 100
########################################

tk = Tk()
tk.title("Model Show")
tk.resizable(0, 0)
canvas = Canvas(tk, width=basin['width'], height=basin['height'], bd=0, highlightthickness=0)
canvas.pack()
tk.update()

class Blob:
  def __init__(self, canvas, speed, x, y):
    self.canvas = canvas
    self.id = canvas.create_oval(x, y, x+10, y+10, fill="blue")
    self.speed = speed
    self.facing = {"x": 0, "y": 0}
    self.state = "idle"
    tk.update()

  def move(self):
    dx = self.facing["x"] - canvas.coords(self.id)[0]
    dy = self.facing["y"] - canvas.coords(self.id)[1]
    distance = sqrt(dx**2 + dy**2)
    time = distance / self.speed
    canvas.move(self.id, dx/time, dy/time)
    tk.update()

  def pointToward(self, x, y):
    self.facing = {"x": x, 'y': y}

class Food:
  def __init__(self, canvas, draw=True):
    self.x = randint(50, basin['width']-50)
    self.y = randint(50, basin['height']-50)
    if draw:
      self.id = canvas.create_oval(self.x-3, self.y-3, self.x+3, self.y+3, fill="orange")
    tk.update()

food = []
for i in range(0, food_amount):
  food.append(Food(canvas))

testBlob = Blob(canvas, 3, 50, 50)

fatBlob = Blob(canvas, 1, 50, 50)
speedyBlob = Blob(canvas, 5, 50, 50)
blobs = [fatBlob, speedyBlob, testBlob]

while True:
  for i in range(0, len(blobs)):
    closestFood = Food(canvas, False)
    closestFood.distance = inf
    closestFood.x = inf
    closestFood.y = inf
    for j in range(0, len(food)):
      dx = canvas.coords(blobs[i].id)[0] - food[j].x
      dy = canvas.coords(blobs[i].id)[1] - food[j].y
      distance = sqrt(dx**2 + dy**2)
      if distance < closestFood.distance:
        closestFood = food[j]
        closestFood.distance = distance
        
    if blobs[i].state == "idle":
      # Decide what to do
      if 10 < closestFood.distance <= 100:
        blobs[i].state = "eat food"
        blobs[i].pointToward(closestFood.x, closestFood.y)
      elif closestFood.distance <= 10:
        food.remove(closestFood)
        blobs[i].state = "idle"
      else:
        blobs[i].state = "idle"
        if randint(1, 10) <= 3:
          blobs[i].pointToward(randint(0, basin['width']), randint(0, basin['height']))
    else:
      foodExist = False
      for j in range(0, len(food)):
        if (food[j].x == blobs[i].facing["x"]) and (food[j].y == blobs[i].facing["y"]):
          foodExist = True

      if not(foodExist):
        blobs[i].state = "idle"

      if closestFood.distance <= 10:
        food.remove(closestFood)
        canvas.delete(closestFood.id)
        blobs[i].state = "idle"

    print(blobs[i].state)
    blobs[i].move()
  print("-------------------------------")
  sleep(0.01)

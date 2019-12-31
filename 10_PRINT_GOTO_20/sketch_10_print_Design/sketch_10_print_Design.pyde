## 10 Print Design
from random import random

x, y = 0, 0
spacing = 10

def setup(): 
    size(800, 300)
    background(0)
    
def draw(): 
    global x 
    global y
    global spacing 
    stroke(255)
    if random() < 0.5: 
        line(x, y, x+spacing, y+spacing)
    else: 
        line(x, y+spacing, x+spacing, y)
    x = x + 10
    if x > width: 
        x = 0
        y = y + 10
    if y > height: 
        noLoop()

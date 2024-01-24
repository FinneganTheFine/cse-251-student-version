import turtle
num_turtles = 5
my_turtles = [turtle.Turtle() for i in range(num_turtles)]
for i, turt in enumerate(my_turtles):
    turt.forward(50*i)
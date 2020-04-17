from turtle import Turtle, Screen
print(1//10)
wn = Screen()
wn.bgcolor('lightblue')

spaceship = Turtle()
spaceship.color('red')
spaceship.penup()

speed = 1

def travel():
    spaceship.forward(speed)
    wn.ontimer(travel, 10)

wn.onkey(lambda: spaceship.setheading(90), 'Up')
wn.onkey(lambda: spaceship.setheading(180), 'Left')
wn.onkey(lambda: spaceship.setheading(0), 'Right')
wn.onkey(lambda: spaceship.setheading(270), 'Down')

wn.listen()

travel()

wn.mainloop()
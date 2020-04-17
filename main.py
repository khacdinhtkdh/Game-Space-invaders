import math
import turtle
import random
import winsound
import playsound

is_game_over = False
exit_game = False

# set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invader")
wn.bgpic("images/space_invaders_background.gif")

# register the shapes
wn.register_shape("images/invader.gif")
wn.register_shape("images/player.gif")
wn.tracer(0)

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()
# Score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
score_string = "Score: {}".format(score)
score_pen.write(score_string, False, align="left", font=("Arial", 8, "normal"))
score_pen.hideturtle()

# Game_over
Game_over = turtle.Turtle()
Game_over.speed(0)
Game_over.color("white")
Game_over.penup()
Game_over.setposition(0, 200)
Game_over_string = "Game Over!"
# Game_over.write(score_string, False, align="left", font=("Arial", 10, "bold"))
Game_over.hideturtle()

# Creat the play turtle
player = turtle.Turtle()
player.color("blue")
player.shape("images/player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
player_speed = 15

# Choose a number of enemies
number_of_enemies = 30
enemies = []

# Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -200
enemy_start_y = 250
enemy_number = 0
for enemy in enemies:
    # Creat the enemy
    enemy.color("red")
    enemy.shape("images/invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * (enemy_number % 10))
    y = enemy_start_y - 50 * (enemy_number // 10)
    enemy_number += 1
    enemy.setposition(x, y)

enemy_speed = 0.2
enemy_speed_down = 30

# Creat the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.setposition(0, -300)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bullet_speed = 5

# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bullet_state = "ready"


# Move player left right
def move_left():
    x = player.xcor()
    x -= player_speed
    if x < -280:
        x = -280
    player.setx(x)


# Move Player right
def move_right():
    x = player.xcor()
    x += player_speed
    if x > 280:
        x = 280
    player.setx(x)


def move_player():
    x = player.xcor()
    x += player.speed
    if x > 280:
        x = 280
    if x < -280:
        x = -280
    player.setx(x)


def fire_bullet():
    # Declare bullet as global if it needs changed
    global bullet_state
    if bullet_state == "ready":
        winsound.PlaySound("audio/laser.wav", winsound.SND_ASYNC)
        bullet_state = "fire"
        # Move the bullet to the just above the player
        x = player.xcor()
        y = player.ycor() + 11
        bullet.setposition(x, y)
        bullet.showturtle()


def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


def esc_game():
    global exit_game
    exit_game = True


def retry_game():
    global exit_game
    exit_game = False


# Creat keyboard
wn.onkeypress(move_left, "Left")
wn.onkeypress(move_right, "Right")
wn.onkeypress(fire_bullet, "space")
wn.onkeypress(esc_game, "a")
wn.onkeypress(retry_game, "r")
wn.listen()
#winsound.PlaySound("audio/background", winsound.SND_LOOP | winsound.SND_ASYNC)
playsound.playsound("audio/background.mp3", False)

# Main game loop
while True:
    wn.update()
    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemy_speed
        enemy.setx(x)

        # Move all enemies and down
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            for e in enemies:
                y = e.ycor()
                y -= enemy_speed_down
                e.sety(y)
            # change direction
            enemy_speed *= -1

        # Check for a collision between the bullet and the enemy
        if is_collision(bullet, enemy):
            # Reset the bullet
            winsound.PlaySound("audio/explosion", winsound.SND_ASYNC)
            bullet.hideturtle()
            bullet_state = "ready"
            bullet.setposition(0, -400)
            # Reset the enemy
            enemy.setposition(0, 10000)
            # update score
            score += 10
            score_string = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(score_string, False, align="left", font=("Arial", 8, "normal"))

        if is_collision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            Game_over.write(Game_over_string, False, align="center", font=("Arial", 15, "bold"))
            playsound.playsound("audio/gameover.mp3", True)
            is_game_over = True
            break

    # Move the bullet
    if bullet_state == "fire":
        y = bullet.ycor()
        y += bullet_speed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 280:
        bullet.hideturtle()
        bullet_state = "ready"

    if is_game_over:
        if not exit_game:
            continue
        else:
            break

wn.bye()
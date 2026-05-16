import tkinter
from tkinter import *
import random

GAME_WIDTH = 900
GAME_HEIGHT = 650
SPEED = 100
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        while True:
            x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 1)) * SPACE_SIZE
            y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 1)) * SPACE_SIZE

            # Check if the new food coordinates overlap with the snake
            if (x, y) not in snake.coordinates:
                break

        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, highscore
        score += 1
        if score > highscore:
            highscore = score
            save_highscore(highscore)
        label.config(text="Score:{}".format(score))
        highscore_label.config(text="Highscore:{}".format(highscore))

        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]: #check everything after the head [1:]
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global highscore
    if score > highscore:
        highscore = score
        save_highscore(highscore)
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    window.after(1300, show_start_screen)  # Nach 1,3 Sekunden zurück zum Startbildschirm

def restart_game():
    global snake, food, score, direction
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)

def show_start_screen():
    global start_button, logo_label, start_text, text_label

    canvas.delete(ALL)


    # Logo hinzufügen
    logo = PhotoImage(file="startlogo.png")  # Pfad zum Logo
    logo_label = Label(window, image=logo, bg=BACKGROUND_COLOR)
    logo_label.image = logo
    logo_label.place(relx=0.5, rely=0.3, anchor=CENTER)
    #logo_label.grid(row=1, columnspan=2)

    #start_text = canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50,font=('consolas', 50), text="Snake Game", fill="white", tag="startscreen")
    start_text = "Snake Game"
    text_label = Label(window, text=start_text, font=("consolas", 50), fg="white", bg="black")
    text_label.place(x=(GAME_WIDTH / 3.3),y=(GAME_HEIGHT / 2))
    start_button = Button(window, text="Start Game", command=start_game, font=("consolas", 20))
    start_button.place(relx=0.5, rely=0.7, anchor=CENTER)

   # label.pack_forget()
    highscore_label.config(text="Highscore: {}".format(highscore))



def start_game():
    global snake, food, score, direction, start_button, logo_label, start_text

    start_button.destroy()
    text_label.destroy()
    logo_label.destroy()
    canvas.delete(start_text)
    score = 0
    direction = 'down'
    #label.config(text="Score:{}".format(score), font=("consolas", 40))
    #label.pack()
    #highscore_label.pack()
    snake = Snake()
    food = Food()
    next_turn(snake, food)


def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(highscore):
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))


window = Tk()
window.title("Snake game")
window.resizable(False, False)

highscore = load_highscore()
score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=("consolas", 30))
label.grid(row=0, column=0)
#label.pack()
highscore_label = Label(window, text="Highscore:{}".format(highscore), font=("consolas", 30))
highscore_label.grid(row=0, column=1)
#highscore_label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.grid(row=1, column=0, columnspan=2)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

show_start_screen()

window.mainloop()
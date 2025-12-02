import tkinter
import random

#Sets the board as 25 rows by 25 columns, with each tile being 25 pixels
ROW = 25 #Number of rows
COL = 25 #Number of columns
TILE_SIZE = 25 #size of each tile
loop_id = None #Holds the ID of the repeating draw() loop

#Creates variables representing the width and height of the window
WINDOW_WIDTH = TILE_SIZE * COL
WINDOW_HEIGHT = TILE_SIZE * ROW

class Tile:
#can create an object representing a single tile
    def __init__(self, x, y):
    #initializes a Tile object with coordinates
        self.x = x #x coordinate in pixels
        self.y = y #y coordinate in pixels

window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

#creates a window that cannot be resized, with the title snake
canvas = tkinter.Canvas(window, bg = "#660099", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#centers the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#creates the hidden Play Again button
play_again_button = tkinter.Button(window, text = "Play Again", font = ("Comic Sans MS", 14, "bold"), command = lambda: restart_game())
play_again_button.place_forget()

#creates the hidden Back to Level Select button
back_button = tkinter.Button(window, text = "Back to Level Select", font = ("Comic Sans MS", 14, "bold"), command = lambda: back_to_menu())
back_button.place_forget()

def load_scores():
    '''Load high scores from scores.txt. Returns a list of numbers'''
    try:
        with open("scores.txt", "r") as f:
            scores = [int(line.strip()) for line in f.readlines()]
            return sorted(scores, reverse = True)[:5]
    except FileNotFoundError:
        return[]

#initialize snake, single tile for head
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #snakes head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE) #food
snake_body = [] #multiple snake tiles
velocityX = 0 #beginning horizontal velocity
velocityY = 0 #beginning vertical velocity
game_over = False
score = 0 #starting score
selected_speed = None #starting speed
highscore = load_scores()
paused = False


    
def save_scores(scores):
    '''Saves the top 5 scores to scores.txt'''
    with open("scores.txt", "w") as f:
        for score in scores[:5]:
            f.write(str(score) + "\n")

def start_level(speed):
    '''Sets the speed and gets rid of the starting menu'''
    global selected_speed
    selected_speed = speed
    start_menu.destroy()
    draw()

#creates the starting screen and the level select buttons
start_menu = tkinter.Frame(window, bg = "black")
start_menu.place(relx = 0.5, rely = 0.5, anchor = "center")
title = tkinter.Label(start_menu, text = "Select Level", fg = "white", bg = "black", font = ("Comic Sans MS", 24, "bold"))
title.pack(pady = 10)
btn1 = tkinter.Button(start_menu, text = "Level 1 (Easy)", width = 20, font = ("Comic Sans MS", 14, "bold"), command = lambda: start_level(150))
btn1.pack(pady = 5)
btn2 = tkinter.Button(start_menu, text = "Level 2 (Medium)", width = 20, font = ("Comic Sans MS", 14, "bold"), command = lambda: start_level(100))
btn2.pack(pady = 5)
btn3 = tkinter.Button(start_menu, text = "Level 3 (Hard)", width = 20, font = ("Comic Sans MS", 14, "bold"), command = lambda: start_level(70))
btn3.pack(pady = 5)

def change_direction(e):
    '''Sets the direction of the snake based on what key is pressed'''
    global velocityX, velocityY, game_over, paused

    #returns if the snake has a collision with the wall or itself
    if game_over:
        return
    
    #pauses the game if space is pressed
    if e.keysym == "space" and not game_over:
        paused = not paused
        if paused:
            if loop_id is not None:
                window.after_cancel(loop_id)
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, text = "Paused :)", fill = "white", font = ("Comic Sans MS", 24, "bold"), tag = "pause_text")
        else:
            canvas.delete("pause_text")
            draw()
        return

    #sets the velocity of the snake depending on what button is pressed
    #prevents the snake from reversing direction
    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    '''returns if the snake hits the wall or itself. Adds one block on the body
    and adds one on the score if the snake collides with an apple. Moves the snake.'''
    global snake, game_over, snake_body, food, score

    #returns if snake collides with wall or itself
    if game_over:
        return
    
    #defines if snake hits the wall
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    #defines if snake hits itself
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #defines a collision with food and increments score
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x, food.y = spawn_food()
        score += 1

    #moves the snakes tail from back to front
    for i in range (len(snake_body) -1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    #moves the snakes head
    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def restart_game():
    '''Resets the global variables. Erases the play again button and level select button'''
    global snake, food, snake_body, velocityX, velocityY, game_over, score, loop_id

    #cancels the loop id when the game is over
    if loop_id is not None:
        window.after_cancel(loop_id)

    #resets the global variables
    snake.x = 5 * TILE_SIZE
    snake.y = 5 * TILE_SIZE
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0
    
    #erases the Play Again and Back buttons
    play_again_button.place_forget()
    back_button.place_forget()

    draw()

def back_to_menu():
    '''Resets the global variables, erases the play again and back buttons, creates the start menu'''
    global snake, food, snake_body, velocityX, velocityY, game_over, score, loop_id, selected_speed, start_menu

    #cancels the loop id
    if loop_id is not None:
        window.after_cancel(loop_id)
    
    #resets the global variables
    loop_id = None
    snake.x = 5 * TILE_SIZE
    snake.y = 5 * TILE_SIZE
    snake_body = []
    velocityX = 0
    velocityY = 0
    game_over = False
    score = 0

    #erases the Play Again and Back buttons
    play_again_button.place_forget()
    back_button.place_forget()

    #rebuilds the starting menu
    start_menu = tkinter.Frame(window, bg = "black")
    start_menu.place(relx = 0.5, rely = 0.5, anchor = "center")
    title = tkinter.Label(start_menu, text = "Select Level", fg = "white", bg = "black", font = ("Comic Sans MS", 24, "bold"))
    title.pack(pady = 10)
    btn1 = tkinter.Button(start_menu, text = "Level 1 (Easy)", width = 20, font = ("Comic Sans MS", 14, "bold"), command = lambda: start_level(150))
    btn1.pack(pady = 5)
    btn2 = tkinter.Button(start_menu, text = "Level 2 (Medium)", width = 20, font = ("Comic Sans MS", 14, "bold"), command = lambda: start_level(100))
    btn2.pack(pady = 5)
    btn3 = tkinter.Button(start_menu, text = "Level 3 (Hard)", width = 20, font = ("Comic Sans MS", 14, "bold"), command = lambda: start_level(70))
    btn3.pack(pady = 5)

def spawn_food():
    '''Spawns new food in a spot not occupied by the snake'''
    while True:
        new_food_x = random.randint(0, COL - 1) * TILE_SIZE
        new_food_y = random.randint(0, ROW - 1) * TILE_SIZE

        occupied = [(snake.x, snake.y)] + [(tile.x, tile.y) for tile in snake_body]

        if (new_food_x, new_food_y) not in occupied:
            return new_food_x, new_food_y

def draw():
    '''Clears and redraws the entire canvas, displays the game over screen when game_over
    is true, updates and displays the high score list'''
    global snake, food, snake_body, game_over, score, selected_speed, loop_id, highscore
    
    if selected_speed is None:
        return
    
    move()
    #clears the screen
    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")
    
    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")

    #creates the green for the body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green")

    #creates the game over screen 
    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 15, font = ("Comic Sans MS", 20, "bold"), text = f"Game Over: {score}", fill = "white")
        play_again_button.place(relx = 0.5, rely = 0.6, anchor = "center")
        back_button.place(relx = 0.5, rely = 0.7, anchor = "center")

        #updates the highscore list
        highscore.append(score)
        highscore = sorted(highscore, reverse = True)[:5]
        save_scores(highscore)
        
        #draws the highscores at the top of the screen
        y = 40
        x = WINDOW_WIDTH // 2
        canvas.create_text(x, y, font = "Arial 14", text = "Highscores: ", fill = "yellow")
        for i, hs in enumerate(highscore):
            canvas.create_text(x, y + 25*(i+1), font = "Arial 12", text = f"{i+1}. {hs}", fill = "white")

    #draws the score during the game
    else:
        canvas.create_text(30, 20, font = ("Comic Sans MS", 10, "bold"), text = f"Score: {score}", fill = "white")
    
    if game_over:
        return
    else:
        loop_id = window.after(selected_speed, draw) #how fast snake moves

#starts the game
draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()


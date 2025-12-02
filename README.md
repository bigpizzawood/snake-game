### **Snake Game**



A classic snake game, where the player moves the snake using the arrow keys and attempts to eat the food. Every time the snake eats a piece of food, it grows longer. This game features high score tracking and three levels of difficulty, with the speed increasing with each level. The player loses by colliding with the wall or the snakes own body.



#### How to run the program



Download the file called snake.py. Open it in an editor/compiler. Run the game.



#### Required Libraries



It is necessary to have Python installed. All required libraries (tkinter and random) are included in the standard Python library.



#### Features



* The snake is moved using the arrow keys
* Three distinct difficulty levels, selected by the user
* High score tracking using a text file
* Options to restart the game or select a different level
* Ability to pause the game using the space bar
* Food respawning in random spots
* Collisions with the wall and snake are detected



#### Function Docstrings



def load\_scores():

 	'''Load high scores from scores.txt. Returns a list of numbers'''



def save\_scores():

 	'''Saves the top five scores to scores.txt.'''



def start\_level(speed):

 	'''Sets the speed and gets ride of the starting menu'''



def change\_direction(e):

 	'''Sets the direction of the snake based on what key is pressed'''



def move():

 	'''Returns if the snake hits the wall or itself. Adds one block on the body and increments the score by one if the snake collides with food. Moves the snake'''



def restart\_game():

 	'''Resets the global variables. Erases the play again and back buttons and level select button.'''



def back\_to\_menu():

 	'''Resets the global variables, erases the play again and back buttons, and creates the starting menu'''



def spawn\_food():

 	'''spawns new food in a spot not occupied by the snake'''



def draw():

 	'''Clears and redraws the entire canvas, displays the game over screen if game\_over is true, and updates and displays the high score list'''


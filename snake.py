import tkinter # Importing the tkinter module for GUI creation
import random # Importing the random module for random number generation

ROWS=25
COLS=25
TILE_SIZE=25

WINDOW_WIDTH=TILE_SIZE*ROWS
WINDOW_HEIGHT=TILE_SIZE*COLS

class Tile: # Class representing a tile in the game grid
    def __init__(self,x,y):
        self.x = x # x-coordinate of the tile
        self.y = y # y-coordinate of the tile

#game window
window = tkinter.Tk() #Creating the main window
window.title("Snake Game") #Setting the title of the window
window.resizable(False, False) #Disabling window resizing



canvas = tkinter.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black", borderwidth=0, highlightthickness=0) #Creating a canvas for drawing
canvas.pack() #Packing the canvas into the window
window.update() #Updating the window to reflect changes

#center the window
window_width=window.winfo_width()
window_height=window.winfo_height()
screen_width=window.winfo_screenwidth()
screen_height=window.winfo_screenheight()

window_x=int((screen_width/2-window_width/2))
window_y=int((screen_height/2-window_height/2))

window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}") #Setting the geometry of the window to center it on the screen

#initializing the grid
snake=Tile(5*TILE_SIZE, 5*TILE_SIZE) #Initial position of the snake # 5 is in the pixels
food=Tile(10*TILE_SIZE, 10*TILE_SIZE) #Initial position of the food
snake_body=[] # List to hold the snake's body segments
velocity_X=0 # Initial velocity in the x direction
velocity_Y=0 # Initial velocity in the y direction
game_over=False # Flag to indicate if the game is over
score=0 # Initial score

def change_direction(e): # event handler for key release events
    #print(e.keysym) # Printing the key that was released
    global velocity_X, velocity_Y,game_over
    if game_over: # If the game is over, do nothing
        return

    if (e.keysym == "Up" and velocity_Y !=1): # If the Up arrow key is released
        velocity_X = 0 # Set x velocity to 0
        velocity_Y = -1 # Set y velocity to -1 (moving up)
    elif (e.keysym == "Down" and velocity_Y !=-1): # If the Down arrow key is released
        velocity_X = 0 # Set x velocity to 0
        velocity_Y = 1 # Set y velocity to 1 (moving down)  
    elif (e.keysym == "Left" and velocity_X!=1): # If the Left arrow key is released
        velocity_X = -1 # Set x velocity to -1 (moving left)
        velocity_Y = 0 # Set y velocity to 0
    elif (e.keysym == "Right" and velocity_X!=-1): # If the Right arrow key is released
        velocity_X = 1 # Set x velocity to 1 (moving right)
        velocity_Y = 0 # Set y velocity to 0

def move():
    global snake,game_over, snake_body, food,score
    if (game_over): # If the game is over, do nothing
        return
    
    #collision detection with walls
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT): # If the snake goes out of bounds
        game_over = True
        return # Set game over flag to True and exit the function
    
    for tile in snake_body: # Loop through each segment of the snake's body 
        if (tile.x == snake.x and tile.y == snake.y): # If the snake collides with its own body
            game_over = True # Set game over flag to True

    #collision detection with food
    if (snake.x == food.x and snake.y == food.y): # If the snake's position matches the food's position
        snake_body.append(Tile(food.x, food.y)) # Add a new segment to the snake's body
        food.x = random.randint(0, COLS-1) * TILE_SIZE # Generate a new random x position for the food
        food.y = random.randint(0, ROWS-1) * TILE_SIZE # Generate a new random y position for the food
        score += 1

    #update snake body
    for i in range(len(snake_body)-1, -1, -1): # Loop through the snake's body segments in reverse order
        tile= snake_body[i] # Get the current segment
        if i == 0:
            tile.x = snake.x # Update the first segment to the snake's current position
            tile.y = snake.y    
        else:
            prev_tile = snake_body[i-1] # Get the previous segment
            tile.x = prev_tile.x # Update the current segment's position to the previous segment's position 
            tile.y = prev_tile.y

    #move snake
    snake.x += velocity_X * TILE_SIZE # Update the x position of the snake
    snake.y += velocity_Y * TILE_SIZE # Update the y position of the snake

def draw():
    global snake, food, snake_body, game_over, score

    move()# Move the snake based on the current velocity

    canvas.delete("all") # Clear the canvas before drawing the new state
    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red") #Drawing the food tile

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill="green") #Drawing the snake tile

    for tile in snake_body: # Loop through each segment of the snake's body
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill="green") #Drawing each segment of the snake's body

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,font="Arial 20", text=f"Game Over! Score: {score}", fill="white") # Displaying game over message and score
    else: # If the game is not over, display the current score
        canvas.create_text(30,20,font="Arial 10", text=f"Score: {score}", fill="white") # Displaying the current score

    window.after(100, draw) #Calling the draw function every 10 seconds to update the game state

draw() #Calling the draw function to start the game    

window.bind("<KeyRelease>", change_direction) #Binding the key release event to the change_direction function
# Main game loop
window.mainloop() #Starting the main event loop of the window

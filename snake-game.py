from tkinter import *
from PIL import Image, ImageTk
import random

MOVE_INCREMENT = 20 
MOVE_PER_SECOND = 10
GAME_SPEED = 1000 // MOVE_PER_SECOND

class Snake(Canvas):
    def __init__(self):
        super().__init__(
            width=600,
            height=620,
            background='black',
            highlightthickness=0
        )
        self.reset = [(100, 100), (80, 100), (60, 100)]
        self.snake_position = [(100, 100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.loop = None
        self.direction = 'Right'
        self.starting = True

        self.bind_all('<Key>',self.on_key_press)
        self.bind_all('<F1>',self.rungame())


        self.load_assets()
        self.create_object()
        self.rungame()

    def load_assets(self):
        self.snake_body_image = Image.open('./assets/body.png')
        self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

        self.food_image = Image.open('./assets/food.png')
        self.food = ImageTk.PhotoImage(self.food_image)

    def create_object(self):
        FONT = (None,14)
        self.create_text(45,12,text='Score: {}'.format(self.score),tag='score',fill='green',font=FONT)

        for x_pos, y_pos in self.snake_position:
            self.create_image(x_pos, y_pos, image=self.snake_body, tag='snake')

        self.create_image(self.food_position[0],self.food_position[1],image=self.food,tag="food")
        self.create_rectangle(7,27,593,613,outline="#FFF")
    
    def move_snake(self):


        head_x,head_y = self.snake_position[0]
        if self.direction == 'Right':
            new_head_pos = (head_x + MOVE_INCREMENT,head_y )
        elif self.direction == 'Left':
            new_head_pos = (head_x - MOVE_INCREMENT,head_y )
        elif self.direction == 'Up':
            new_head_pos = (head_x ,head_y - MOVE_INCREMENT)
        elif self.direction == 'Down':
            new_head_pos = (head_x,head_y + MOVE_INCREMENT)

        self.snake_position = [new_head_pos] + self.snake_position[:-1]
        
        findsnake = self.find_withtag('snake')
        for segment,pos in zip(findsnake,self.snake_position):
            self.coords(segment,pos)
    
    def rungame(self):
        if self.check_collision() and self.starting == True:
            # when colluisions
            self.after_cancel(self.loop)
            self.starting = False
            self.delete('all')
            self.create_text(300,300,justify=CENTER,text=f'GAME OVER \n\n Score:{self.score}\n\n New Game <F1>',fill='red',font=(None,30))
        
        elif self.check_collision() and self.starting == False:
            # when F1
            self.delete('all')
            self.snake_position = self.reset
            self.food_position = self.set_new_food_position()
            self.create_object()
            self.starting = True
            self.direction ='Right'
            self.score = 0
            score = self.find_withtag('score')
            self.itemconfigure(score,text='Score: {}'.format(self.score),tag='score')

            self.loop =  self.after(GAME_SPEED,self.rungame)
        else :
            #when moving
            self.check_food_collision()
            self.move_snake()
            self.loop = self.after(GAME_SPEED,self.rungame) # loop game 
    
    def on_key_press(self,e):
        new_direction = e.keysym # key pressed

        all_direction =('Up', 'Down','Left','Right')
        opposite = ({'Up','Down'},{'Left','Right'})

        if (new_direction in all_direction) and {new_direction,self.direction} not in opposite :
            self.direction  = new_direction
        elif new_direction == 'F1' :
            self.rungame()
    def check_collision(self) :
        head_x,head_y = self.snake_position[0]
        return (head_x in (0,600) or head_y in (20,620) or ( head_x,head_y) in self.snake_position[1:])

    
    def check_food_collision(self):
        if self.snake_position[0] == self.food_position :
            self.score += 1 
            self.snake_position.append(self.snake_position[-1])

            self.create_image(*self.snake_position[-1],image=self.snake_body, tag='snake')

            score = self.find_withtag('score')
            self.itemconfigure(score,text='Score: {}'.format(self.score),tag='score')

            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag('food'),self.food_position)

    def set_new_food_position (self):
        while True:
            x_pos = random.randint(1,29) * MOVE_INCREMENT
            y_pos = random.randint(3,30) * MOVE_INCREMENT

            food_position = (x_pos,y_pos)

            if food_position not in self.snake_position : 
                return food_position


GUI = Tk()
GUI.title("Snake Fame Nokia 3310")
GUI.resizable(False, False)

game = Snake()
game.pack()

GUI.mainloop()

import random
import turtle


class duckietown(list):

    def __init__(self, height, width, obstacles_file):
        random.seed(2501)
        super().__init__()
        self.height = height
        self.width = width
        self.obstacles = obstacles_file
        self._inner_list = [[random.uniform(0, 0.1) for i in range(width)] for j in range(height)]       
        self.load_obstacles()
        
    def load_obstacles(self):
        with open(self.obstacles) as f:
            for line in f:
                coordinates = [int(x) for x in line.strip().split()]
                #Set obstacle cell cost to -1.0
                self.__setitem__(coordinates[0], coordinates[1], -1.0)
                
    def __len__(self):
        return self.height
        
    def __setitem__(self, i, j, value):
        self._inner_list[i][j] = value
        
    def __getitem__(self,index):
        return self._inner_list[index]
        

     
def visualize_path(grid, path, speed):
    donald = turtle.Turtle(shape="turtle", visible=False)
    visualize_grid(donald, speed)
    draw_path(grid, path, donald)
    turtle.exitonclick()


# helper functions for display
           
def visualize_grid(donald, speed):
    s = turtle.Screen()
    s.setup(1300, 800)
    s.title("Path Finder")
    s.bgpic('gfx/grid.gif')
    duck_shape = "gfx/donald_duckie_icon.gif"
    s.register_shape(duck_shape)
    donald.shape(duck_shape)
    s.update()
    donald.pen(fillcolor="yellow", pencolor="violet", pensize=5)
    donald.penup()
    donald.speed(10)
    donald.setpos(-588.00, 348.00) # starting position: top left-most cell
    donald.pendown()
    donald.speed(speed)
    donald.showturtle()


    
def draw_path(grid, path, donald):
    r = 0
    c = 0
    for dir in path:
        if dir == 'East':
            donald.setheading(0)
            c += 1
        elif dir == 'South':
            donald.setheading(270)
            r += 1
        else:
            print(f"Invalid direction '{dir}' found!")
            break
        donald.forward(24)
        
        if r >= grid.height and c >= grid.width:
            print("Oh no! Donald has ventured into the wilderness!")
            break
        elif grid[r][c] < 0:
            print("Oh no! Donald has had an unfriendly encounter with an obstacle!")
            break
            
    if r == grid.height-1 and c == grid.width-1:
        print("Donald has succesfully reached the charging station!")

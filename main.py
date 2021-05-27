from tkinter import Canvas, Button, Label, Tk, StringVar
from windows import set_dpi_awareness
from random import choice, randint
from ai import Ai

# code for windows appearance
set_dpi_awareness()

FIRST_COLOR = 'black'
SECOND_COLOR = '#d9d9d9'


class Game:
    WIDTH = 250
    HEIGHT = 500

    def __init__(self):
        # level and score variables
        self.level_int = 1
        self.score_int = 0
        self.cars_counter = 0
        self.bars_counter = 0
        self.max_score_size = 6
        self.score_to_level_up = [5000, 15000, 36000, 57000, 78000, 99000, 200000, 500000]

        # variables to position of next cars
        self.next_point = choice((50, 125))
        self.last_point = self.next_point

        # speeds lists
        self.cars_speed = [400, 300, 250, 200, 150, 100, 75, 50, 20]
        self.bars_speed = [550, 450, 400, 350, 300, 250, 225, 200, 150]

        # all the possible actions
        self.action_dict = {0: "Left", 1: 'Right'}

        # list with all cars and all bars
        self.cars = []
        self.bars = []

        # status of running and artificial intelligence
        self.running = True
        self.ai_is_activated = False

        # block code to create root reference on tkinter by Tk()
        self.root = Tk()
        self.root.title("BRICK CAR AI")
        self.root.resizable(False, False)
        self.root.configure(bg=SECOND_COLOR)

        # create status level
        self.level = StringVar()
        self.set_level_label()
        self.level_label = Label(self.root,
                                 textvariable=self.level,
                                 font=("Helvetica", 10, "bold"), bg=SECOND_COLOR)
        # create status score
        self.score = StringVar()
        self.set_score_label()
        self.score_label = Label(self.root,
                                 textvariable=self.score,
                                 font=("Helvetica", 10, "bold"), bg=SECOND_COLOR)
        # create button for AI
        self.AI_button = Button(self.root, text='AI', highlightbackground="#bce8f1", highlightcolor="#bce8f1",
                                highlightthickness=1, command=self.activate_ai)

        # create status bar in the window
        self.level_label.grid(row=0, column=0, pady=5, padx=10, sticky='EW')
        self.score_label.grid(row=0, column=1, pady=5, padx=10, sticky='EW')
        self.AI_button.grid(row=0, column=2, pady=5, padx=10, sticky='EW')

        # create canvas
        self.canvas = Canvas(
            self.root,
            width=Game.WIDTH,
            height=Game.HEIGHT,
            bg=SECOND_COLOR
        )
        self.canvas.grid(column=0, row=1, columnspan=3, sticky="NSEW", padx=2)

        # The main car is the car that you control
        self.main_car = Shape(self.canvas, 50, 'car', 25 * 20, True, True)

    def start(self):
        # method for start the game

        # key event reference
        self.root.bind("<Key>", self.handle_events)

        # create the side bars before game start
        self.fill_bars()

        # start timer for car and bars
        self.timer_bars()
        self.timer_cars()

        # start the game
        print("Start")
        self.root.mainloop()

    def activate_ai(self):
        # class to activate the ai status.
        # this changes the style of the button

        self.ai_is_activated = not self.ai_is_activated
        if self.ai_is_activated:
            self.AI_button.configure(fg='blue')
        else:
            self.AI_button.configure(fg='black')

    def ai_execution(self):
        # code for Ai call and execution
        if self.ai_is_activated:
            distance = self.get_cars_distance()
            new_ai = Ai()
            new_ai.set_rewards(distance[0], distance[1])
            new_ai.training()
            self.action_taking(self.action_dict[new_ai.get_shortest_path(0, 0)[1][1]])

    def get_cars_distance(self):
        # this will calculate the distance between the last two cars on each way
        # function inter to reduce value
        def calc_distance(x1, y1, x2, y2):
            return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

        # code to get the two cars closest to each road
        coordinates = self.main_car.get_coordinates()
        coordinates[0] = coordinates[0] / 3 - 1

        max_right = -5
        max_left = -5
        for car in self.cars:
            current_xy = car.get_coordinates()
            if current_xy[0] / 3 - 1 == 0 and max_left <= current_xy[1]:
                max_left = car.get_coordinates()[1]
            elif current_xy[0] / 3 - 1 == 1 and max_right <= current_xy[1]:
                max_right = car.get_coordinates()[1]

        distance_next_right = calc_distance(coordinates[0], coordinates[1], 0, max_right)
        distance_next_left = calc_distance(coordinates[0], coordinates[1], 1, max_left)

        return distance_next_left, distance_next_right

    def set_score_label(self):
        # update the score on screen
        self.score.set(f"Score: {self.score_int}")

    def set_level(self):
        # update the level
        if self.score_int >= self.score_to_level_up[0]:

            if len(self.score_to_level_up) > 1:
                del self.score_to_level_up[0]

            if self.level_int < 9:
                self.level_int += 1

                if len(self.cars_speed) > 1 and len(self.bars_speed) > 1:
                    del self.cars_speed[0]
                    del self.bars_speed[0]
            self.set_level_label()

    def set_level_label(self):
        # update the level on screen
        self.level.set(f"Level: {self.level_int}")

    def timer_bars(self):
        # timer for bars
        if self.running:
            if self.bars_counter == 0:
                self.bars.append(Shape(self.canvas, 0, 'bar', 0, False, False))
                self.bars.append(Shape(self.canvas, 225, 'bar', False, False))
                self.bars_counter = 5

            self.bars_counter -= 1

            to_delete = ''
            for shape in self.bars:
                if not shape.fall():
                    to_delete = self.bars.index(shape)

            # delete shapes out of canvas
            if to_delete != '':
                del self.bars[to_delete]

            self.root.after(self.bars_speed[0], self.timer_bars)

    def timer_cars(self):
        # timer execution for cars

        if self.running:

            # code to create new car
            if self.cars_counter == 0:

                # A new shape type car will be created and added to cars list
                # the parameters are canvas, reference point on canvas to create a car (x), the type of shape,
                # reference point to y (0=default) and 2 type of collision check
                self.cars.append(Shape(self.canvas, self.next_point, 'car', 0, False, True))
                self.next_point = choice((50, 125))

                # this defines the spacing between the cars
                if self.next_point == self.last_point:
                    self.cars_counter = randint(4, 10)

                else:
                    self.last_point = self.next_point
                    self.cars_counter = 10

            self.cars_counter -= 1

            to_delete = ''
            for shape in self.cars:
                if not shape.fall():
                    if shape.crashed:
                        self.running = False
                        self.collision_color()
                        return False
                    to_delete = self.cars.index(shape)
                    # delete shapes on canvas
                    self.cars[to_delete].del_shape()

            # delete shapes out of canvas
            if to_delete != '':
                # delete shape on car list
                del self.cars[to_delete]
                if len(str(self.score_int + self.level_int * 100)) <= self.max_score_size:
                    self.score_int += self.level_int * 100
                    self.set_score_label()
                    self.set_level()

            # call the Ai method
            self.ai_execution()

            # increment the score
            if len(str(self.score_int + 1)) <= self.max_score_size:
                self.score_int += 1
                self.set_score_label()

            # this checks if the car has crashed
            if self.main_car.crashed:
                self.running = False
                return False

            self.root.after(self.cars_speed[0], self.timer_cars)

    def fill_bars(self):
        # fill the bars on the screen
        for side_bar in (0, 225):
            for x in range(1, 5):
                self.bars.append(Shape(self.canvas, side_bar, 'bar', x * 25 * 5, False, False))

    def handle_events(self, event):
        # this gets the keys pressed by the player on keyboard and calls the actions
        if event.keysym == "Left" or event.keysym == "Right":
            self.action_taking(event.keysym)

    def action_taking(self, action):
        # actions to move car

        if self.running:
            result = True
            if action == "Left":
                result = self.main_car.move(-3, 0)
            if action == "Right":
                result = self.main_car.move(3, 0)
            if not result and self.main_car.crashed:
                self.running = False
                self.collision_color()

    def collision_color(self):
        # this will change the color of the car when the main car has crashed
        self.main_car.change_color('#dc3545')


class Shape:
    BOX_SIZE = 25

    START_POINT = {
        'bar': (0, 225,),
        'car': (50, 125,),
    }
    SHAPES = {
        'car': ((0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 3),),
        'bar': ((0, 1), (0, 2), (0, 3))
    }

    def __init__(self, canvas, side, shape_name, y_additional=0, overrun_check=False, collision_check=False):
        global FIRST_COLOR, SECOND_COLOR

        aux_color = FIRST_COLOR
        side = Shape.START_POINT[shape_name].index(side)
        self.boxes = []  # the squares drawn by canvas.create_rectangle()
        self.point = Shape.START_POINT[shape_name][side]
        self.canvas = canvas
        self.overrun_check = overrun_check
        self.collision_check = collision_check
        self.crashed = False

        Shape.BOX_SIZE = 25
        for point in Shape.SHAPES[shape_name]:

            # this condition refers to the block (1,3) which is a block camouflaged with the background color.
            if point == (1, 3):
                FIRST_COLOR = SECOND_COLOR
            else:
                FIRST_COLOR = aux_color

            # create
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + self.point,
                point[1] * Shape.BOX_SIZE - (4 * Shape.BOX_SIZE) + y_additional,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + self.point,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE - (4 * Shape.BOX_SIZE) + y_additional,
                fill=FIRST_COLOR, outline=SECOND_COLOR)
            self.boxes.append(box)

    def change_color(self, color):
        # method to change color of the shape
        for box in self.boxes:
            if self.canvas.itemcget(box, "fill") == FIRST_COLOR:
                self.canvas.itemconfig(box, fill=color)

    def del_shape(self):
        # method to delete the box

        for box in self.boxes:
            self.canvas.delete(box)

    def move(self, x, y):
        # move the box
        if not self.can_move_shape(x, y):
            return False
        elif not self.crashed:
            for box in self.boxes:
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def get_coordinates(self, number_box=3):
        # method that return the coordinates of and shape
        # number_box is the shape reference block

        box_list = []
        for box in self.boxes:
            current_box = self.canvas.coords(box)
            current_list = []
            for item in range(2):
                current_list.append(current_box[item] / self.BOX_SIZE)
            box_list.append(current_list)
        return box_list[number_box]

    def fall(self):
        # Moves this shape one box-length down.
        if not self.can_move_shape(0, 1):
            return False
        elif not self.crashed:
            # make a collision check
            for box in self.boxes:
                self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
                relative_position = self.canvas.coords(box)[1]
                if relative_position > 575:
                    return False
        return True

    def can_move_box(self, box, x, y):
        # Check if box can move (x, y) boxes.
        x = x * Shape.BOX_SIZE
        y = y * Shape.BOX_SIZE
        cords = self.canvas.coords(box)

        if self.overrun_check:
            if cords[3] + y > Game.HEIGHT:
                return False
            if cords[0] + x < 0:
                return False
            if cords[2] + x >= Game.WIDTH:
                return False

        if self.collision_check:
            # Returns False if moving box (x, y) would overlap another box
            overlap = set(self.canvas.find_overlapping(
                (cords[0] + cords[2]) / 2 + x,
                (cords[1] + cords[3]) / 2 + y,
                (cords[0] + cords[2]) / 2 + x,
                (cords[1] + cords[3]) / 2 + y
            ))

            other_items = set(self.canvas.find_all()) - set(self.boxes)
            if overlap & other_items:
                print("Game over")
                self.crashed = True
                return False
        return True

    def can_move_shape(self, x, y):
        # Check if the shape can move (x, y) boxes.
        for box in self.boxes:
            if not self.can_move_box(box, x, y):
                return False
        return True


if __name__ == "__main__":
    game = Game()
    game.start()

from tkinter import Canvas, Button, Label, Tk, StringVar
from windows import set_dpi_awareness
from random import choice, randint

set_dpi_awareness()

FIRST_COLOR = 'black'
SECOND_COLOR = '#d9d9d9'
LEFT = 50


class Game:
    WIDTH = 250
    HEIGHT = 500

    def start(self):
        self.level_int = 1
        self.score_int = 0
        self.cars_speed = [600, 500, 400, 250, 150, 125, 100, 75, 50]
        self.bars_speed = [800, 700, 600, 450, 350, 250, 200, 100, 75]
        self.cars_counter = 0
        self.bars_counter = 0
        self.last_point = 50
        self.next_point = 50
        self.score_to_level_up = [5000, 15000, 36000, 57000, 78000, 99000, 200000, 500000]

        self.root = Tk()
        self.root.resizable(False, False)
        self.root.configure(bg=SECOND_COLOR)
        self.root.title("BRICK CAR AI")

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
                                highlightthickness=1)

        # create status bar in the window
        self.level_label.grid(row=0, column=0, pady=5, padx=10, sticky='EW')
        self.score_label.grid(row=0, column=1, pady=5, padx=10, sticky='EW')
        self.AI_button.grid(row=0, column=2, pady=5, padx=10, sticky='EW')

        self.canvas = Canvas(
            self.root,
            width=Game.WIDTH,
            height=Game.HEIGHT,
            bg=SECOND_COLOR
        )
        self.canvas.grid(column=0, row=1, columnspan=3, sticky="NSEW", padx=2)

        self.main_car = Shape(self.canvas, 50, 'car', 25 * 20)
        self.cars = []
        self.bars = []
        self.side_zero = []
        self.side_one = []
        self.root.bind("<Key>", self.handle_events)
        self.fill_bar()
        self.timer_bars()
        self.timer_cars()

        self.root.mainloop()

    def set_score_label(self):
        self.score.set(f"Score: {self.score_int}")

    def set_level(self):
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
        self.level.set(f"Level: {self.level_int}")

    def timer_bars(self):
        if self.bars_counter == 0:
            self.bars.append(Shape(self.canvas, 0, 'bar'))
            self.bars.append(Shape(self.canvas, 225, 'bar'))
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

        if self.cars_counter == 0:
            self.cars.append(Shape(self.canvas, self.next_point, 'car'))

            # AI code
            if self.next_point == 50:
                self.side_zero.append(0)
            else:
                self.side_one.append(0)

            self.next_point = choice((50, 125))

            if self.next_point == self.last_point:
                self.cars_counter = randint(4, 10)
            else:
                self.last_point = self.next_point
                self.cars_counter = 10

        self.cars_counter -= 1

        to_delete = ''
        for shape in self.cars:
            if not shape.fall():
                to_delete = self.cars.index(shape)

        # delete shapes out of canvas
        if to_delete != '':
            del self.cars[to_delete]
            self.score_int += self.level_int * 100
            self.set_score_label()
            self.set_level()
            print(self.level_int, self.score_int, self.score_to_level_up[0], self.cars_speed[0], self.bars_speed[0])

        if len(self.side_zero):
            for i in range(len(self.side_zero)):
                self.side_zero[i] += 1
            if self.side_zero[0] > 22:
                del self.side_zero[0]

        if len(self.side_one):
            for i in range(len(self.side_one)):
                self.side_one[i] += 1
            if self.side_one[0] > 22:
                del self.side_one[0]

        self.score_int += 1
        self.set_score_label()
        # print(self.side_zero, self.side_one)
        self.root.after(self.cars_speed[0], self.timer_cars)

    def fill_bar(self):
        for side_bar in (0, 225):
            for x in range(1, 5):
                self.bars.append(Shape(self.canvas, side_bar, 'bar', x * 25 * 5))

    def handle_events(self, event):
        """Handle all user events."""
        if event.keysym == "Left":
            self.main_car.move(-3, 0)
        if event.keysym == "Right":
            self.main_car.move(3, 0)


class Shape:
    BOX_SIZE = 25

    START_POINT = {
        'bar': (0, 225,),
        'car': (50, 125,),
    }
    SHAPES = {
        'car': ((0, 1), (0, 3), (1, 0), (1, 1), (1, 2), (2, 1), (2, 3),),
        'bar': ((0, 1), (0, 2), (0, 3))
    }

    def __init__(self, canvas, side, shape_name, y_adicional=0):
        side = Shape.START_POINT[shape_name].index(side)
        self.boxes = []  # the squares drawn by canvas.create_rectangle()
        self.point = Shape.START_POINT[shape_name][side]
        self.canvas = canvas

        Shape.BOX_SIZE = 25
        for point in Shape.SHAPES[shape_name]:
            box = canvas.create_rectangle(
                point[0] * Shape.BOX_SIZE + self.point,
                point[1] * Shape.BOX_SIZE - (4 * Shape.BOX_SIZE) + y_adicional,
                point[0] * Shape.BOX_SIZE + Shape.BOX_SIZE + self.point,
                point[1] * Shape.BOX_SIZE + Shape.BOX_SIZE - (4 * Shape.BOX_SIZE) + y_adicional,
                fill=FIRST_COLOR, outline=SECOND_COLOR)
            self.boxes.append(box)

    def move(self, x, y):
        """Moves this shape (x, y) boxes."""
        if not self.can_move_shape(x, y):
            return False
        else:
            for box in self.boxes:
                self.canvas.move(box, x * Shape.BOX_SIZE, y * Shape.BOX_SIZE)
            return True

    def fall(self):
        """Moves this shape one box-length down."""
        # if not self.can_move_shape(0, 1):
        #     return False
        # else:

        # make a collision check
        for box in self.boxes:
            self.canvas.move(box, 0 * Shape.BOX_SIZE, 1 * Shape.BOX_SIZE)
            relative_position = self.canvas.coords(box)[1]
            if relative_position > 575:
                return False
        return True

    def can_move_box(self, box, x_value, y_value):
        """Check if box can move (x, y) boxes."""
        x = x_value - 1
        y = y_value
        for i in range(2):
            x = x * Shape.BOX_SIZE
            y = y * Shape.BOX_SIZE
            cords = self.canvas.coords(box)

            # Returns False if moving the box would overrun the screen
            if cords[3] + y > Game.HEIGHT:
                return False
            if cords[0] + x < 0:
                return False
            if cords[2] + x > Game.WIDTH:
                return False

            # Returns False if moving box (x, y) would overlap another box
            overlap = set(self.canvas.find_overlapping(
                (cords[0] + cords[2]) / 2 + x,
                (cords[1] + cords[3]) / 2 + y,
                (cords[0] + cords[2]) / 2 + x,
                (cords[1] + cords[3]) / 2 + y
            ))
            other_items = set(self.canvas.find_all()) - set(self.boxes)
            x = x_value
            if overlap & other_items:
                return False

        return True

    def can_move_shape(self, x, y):
        """Check if the shape can move (x, y) boxes."""
        for box in self.boxes:
            if not self.can_move_box(box, x, y):
                return False
        return True


if __name__ == "__main__":
    game = Game()
    game.start()

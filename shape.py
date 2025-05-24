from config import FIRST_COLOR, SECOND_COLOR, CANVAS_HEIGHT, CANVAS_WIDTH

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
            if cords[3] + y > CANVAS_HEIGHT:
                return False
            if cords[0] + x < 0:
                return False
            if cords[2] + x >= CANVAS_WIDTH:
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

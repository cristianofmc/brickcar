from tkinter import Canvas, Frame
from random import choice, randint
from ai import Ai
from datetime import datetime
from shape import Shape
from config import SECOND_COLOR, COLLISION_COLOR, CANVAS_HEIGHT, CANVAS_WIDTH
from game_status_bar import GameStatusBar


class Game:
    def __init__(self, root, on_game_over):
        self.root = root
        self.on_game_over = on_game_over

        # Cria um frame container para a tela do jogo
        self.frame = Frame(root, bg=SECOND_COLOR)
        self.frame.pack(expand=True, fill="both")
                
        # Status bar
        self.status_bar = GameStatusBar(
            self.frame,
            on_ai_toggle=self.activate_ai,
        )

        # Variáveis de status
        self.start_time = datetime.now()
        self.end_time = 0
        self.interval = 0
        self.level_int = 1
        self.score_int = 0
        self.cars_counter = 0
        self.bars_counter = 0
        self.max_score_size = 6
        self.score_to_level_up = [5000, 15000, 36000, 57000, 78000, 99000, 200000, 500000]

        self.next_point = choice((50, 125))
        self.last_point = self.next_point

        self.cars_speed = [350, 250, 200, 150, 100, 75, 50, 40, 25]
        self.bars_speed = [500, 400, 350, 300, 250, 225, 200, 190, 195]

        self.action_dict = {0: "Left", 1: 'Right'}

        self.cars = []
        self.bars = []

        self.running = True
        self.ai_is_activated = False

        # Canvas do jogo
        self.canvas = Canvas(
            self.frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=SECOND_COLOR
        )

        self.canvas.grid(column=0, row=1, columnspan=3, sticky="NSEW", padx=2)

        # Carro principal
        self.main_car = Shape(self.canvas, 50, 'car', 25 * 20, True, True)

        self.update_status_labels()

    def update_status_labels(self):
        self.status_bar.set_level(self.level_int)
        self.status_bar.set_score(self.score_int)

    def execution_log(self):
        self.end_time = datetime.now()
        self.interval = self.end_time - self.start_time
        print(f'Level: {self.level_int}\nScore: {self.score_int}\nSpeed: {self.cars_speed[0]}\nTime: {self.interval}')

    def start(self):
        self.frame.focus_set()
        self.frame.bind("<Key>", self.handle_events)

        self.fill_bars()

        self.timer_bars()
        self.timer_cars()

    def activate_ai(self):
        self.ai_is_activated = not self.ai_is_activated
        self.status_bar.set_ai_status(self.ai_is_activated)

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


    def execution_log(self):
        self.end_time = datetime.now()
        self.interval = self.end_time - self.start_time
        print(f'Level: {self.level_int}\nScore: {self.score_int}\nSpeed: {self.cars_speed[0]}\nTime: {self.interval}')

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
            self.update_status_labels()

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

            to_delete = None
            for shape in self.bars:
                if not shape.fall():
                    to_delete = self.bars.index(shape)

            # delete shapes out of canvas
            if to_delete is not None:
                del self.bars[to_delete]

            self.root.after(self.bars_speed[0], self.timer_bars)

    def timer_cars(self):
        if self.running:
            if self.cars_counter == 0:
                self.cars.append(Shape(self.canvas, self.next_point, 'car', 0, False, True))
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
                    if shape.crashed:
                        self.collision_color()
                        self.execution_log()
                        self.game_over()
                        return  # interrompe se houve colisão
                    to_delete = self.cars.index(shape)
                    shape.del_shape()

            if to_delete != '':
                del self.cars[to_delete]
                if len(str(self.score_int + self.level_int * 100)) <= self.max_score_size:
                    self.score_int += self.level_int * 100
                    self.update_status_labels()
                    self.set_level()

            self.ai_execution()

            if len(str(self.score_int + 1)) <= self.max_score_size:
                self.score_int += 1
                self.update_status_labels()

            if self.main_car.crashed:
                self.collision_color()
                self.execution_log()
                self.game_over()
                return

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
        if not self.running:
            return

        result = True
        if action == "Left":
            result = self.main_car.move(-3, 0)
        elif action == "Right":
            result = self.main_car.move(3, 0)

        if not result and self.main_car.crashed:
            self.collision_color()
            self.game_over()


    def game_over(self):
        self.running = False
        self.canvas.destroy()
        self.end_game()

    def end_game(self):
        self.frame.destroy()
        self.on_game_over()


    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


    def collision_color(self):
        self.main_car.change_color(COLLISION_COLOR)
import tkinter as tk
from game import Game
from start_modal import StartModal
from config import WINDOW_HEIGHT, WINDOW_WIDTH


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("BrickCar")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        # Cria um frame principal que ocupará toda a janela
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill='both', expand=True)

        Game(self.main_frame , on_game_over=self.show_start_modal)

        # Mostra a tela inicial via StartModal
        self.show_start_modal()

    def show_start_modal(self):
        self.start_modal = StartModal(self.root, on_start=self.start_game)


    def start_game(self):
        self.clear_frame()
        game = Game(self.main_frame, self.on_game_over)
        game.start()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def on_game_over(self):
        self.show_start_modal()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

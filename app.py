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

        # Mostra a tela inicial via StartModal
        self.show_start_modal()

    def show_start_modal(self):
        self.clear_frame()
        # Cria o StartModal no main_frame, com callback para start_game
        self.start_modal = StartModal(self.main_frame, on_start=self.start_game)

    def start_game(self):
        self.clear_frame()
        game = Game(self.main_frame, on_game_over=self.show_start_modal)
        game.start()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

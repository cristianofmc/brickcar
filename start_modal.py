from tkinter import Frame, Label, Button
from config import SECOND_COLOR, FIRST_COLOR, BUTTON_COLOR, BUTTON_TEXT_COLOR


class StartModal:
    def __init__(self, root, on_start):
        self.root = root
        self.on_start = on_start

        self.frame = Frame(root, bg=SECOND_COLOR)
        self.frame.pack(expand=True, fill="both")

        Label(
            self.frame,
            text="Click to start the game",
            font=("Arial", 14, "bold"),
            bg=SECOND_COLOR,
            fg=FIRST_COLOR
        ).pack(pady=20)

        Button(
            self.frame,
            text="Start the Game",
            command=self.start,
            highlightbackground=BUTTON_COLOR,
            highlightcolor=BUTTON_COLOR,
            highlightthickness=1,
            fg=BUTTON_TEXT_COLOR
        ).pack()

        self.frame.bind("<Left>", self.start)
        self.frame.bind("<Right>", self.start)

    def start(self, event=None):
        self.frame.destroy()
        self.on_start()

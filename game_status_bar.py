from tkinter import Frame, Label, Button, StringVar, font
from config import (
    SECOND_COLOR, FIRST_COLOR, 
    BUTTON_COLOR, BUTTON_TEXT_COLOR, BUTTON_ACTIVE_TEXT_COLOR
)


class GameStatusBar:
    def __init__(self, parent_frame, on_ai_toggle):
        self.frame = Frame(parent_frame, bg=SECOND_COLOR)
        self.frame.grid(row=0, column=0, columnspan=3, sticky='EW')

        self.level_var = StringVar()
        self.score_var = StringVar()

        self.level_label = Label(
            self.frame, textvariable=self.level_var,
            font=("Helvetica", 10, "bold"),
            bg=SECOND_COLOR,
            fg=FIRST_COLOR
        )
        self.level_label.grid(row=0, column=0, pady=5, padx=10, sticky='EW')

        self.score_label = Label(
            self.frame, textvariable=self.score_var,
            font=("Helvetica", 10, "bold"),
            bg=SECOND_COLOR,
            fg=FIRST_COLOR
        )
        self.score_label.grid(row=0, column=1, pady=5, padx=10, sticky='EW')

        self.ai_button = Button(
            self.frame, text='AI',
            highlightbackground=BUTTON_COLOR, highlightcolor=BUTTON_COLOR,
            highlightthickness=1,
            fg=BUTTON_TEXT_COLOR,
            command=on_ai_toggle
        )
        self.ai_button.grid(row=0, column=2, pady=5, padx=10, sticky='EW')

        # Salvar fonte padrão
        self.default_font = font.nametofont(self.ai_button.cget("font"))
        self.bold_font = self.default_font.copy()
        self.bold_font.configure(weight="bold")

        # Estado atual do AI (para manter a cor correta no hover)
        self.ai_activated = False

        self.ai_button.bind("<Enter>", self.on_enter)
        self.ai_button.bind("<Leave>", self.on_leave)

    def on_enter(self, event):
        self.ai_button.configure(
            font=self.bold_font,
            fg=BUTTON_ACTIVE_TEXT_COLOR if self.ai_activated else BUTTON_TEXT_COLOR
        )

    def on_leave(self, event):
        self.ai_button.configure(
            font=self.default_font,
            fg=BUTTON_ACTIVE_TEXT_COLOR if self.ai_activated else BUTTON_TEXT_COLOR
        )

    def set_level(self, level):
        self.level_var.set(f"Level: {level}")

    def set_score(self, score):
        self.score_var.set(f"Score: {score}")

    def set_ai_status(self, activated):
        self.ai_activated = activated
        self.ai_button.configure(
            fg=BUTTON_ACTIVE_TEXT_COLOR if activated else BUTTON_TEXT_COLOR
        )

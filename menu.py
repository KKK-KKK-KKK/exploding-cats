import pygame
from button import Button

class Menu:
    visibility = False
    choice = 0

    def __init__(self):
        print("Initializing Menu")
        self.start_button = Button("./resources/images/start.png", (175, 700))
        self.end_button = Button("./resources/images/exit.png", (425, 700))
        self.visibility = True

    def execute_choice(self):
        if self.choice == 0:
            pass
        elif self.choice == 1:
            self.hide()
            return 1
        elif self.choice == 2:
            print("Exiting game, thank you for playing!")
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return None
        else:
            try:
                raise Exception("Incorrect menu self.choice value", "Exiting game")
            except Exception as error:
                print(error.args)
                pygame.event.post(pygame.event.Event(pygame.QUIT))

    def draw(self, surface):
        if not self.visibility:
            return
        self.start_button.draw_button(surface)
        self.end_button.draw_button(surface)

    def hide(self):
        if not self.visibility:
            return
        print("Hiding menu")
        self.visibility = False
        self.start_button.hide()
        self.end_button.hide()

    def reveal(self):
        if self.visibility:
            return
        print("Revealing menu")
        self.visibility = True
        self.start_button.reveal()
        self.end_button.reveal()

    def update(self):
        start_pressed = self.start_button.update()
        end_pressed = self.end_button.update()

        if start_pressed:
            self.choice = 1
        elif end_pressed:
            self.choice = 2

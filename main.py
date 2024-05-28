import pygame
import sys



class Button:
    keydown = False
    outside_rect_keypress = False

    def __init__(self, image_path, center_coords):
        print(f"Creating button with image: {image_path} at: {center_coords}")
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = center_coords

    def draw_button(self, surface):
        print("Drawing button")
        surface.blit(self.image, self.rect) 

    def draw_hover_animation(self):
        pass

    def draw_click_animation(self):
        #Function should execute only after a sucessful click
        pass
        

    def update(self):
        #Function written to create a correct 'click' mechanism 
        #Returns True on successful click and False on failure
        mouse_pos = pygame.mouse.get_pos()
        mouse_inside_rect = self.rect.collidepoint(mouse_pos)
        pressed_mouse = pygame.mouse.get_pressed()
        self.mouse_inside_rect_previous = mouse_inside_rect
        
        if mouse_inside_rect == False and pressed_mouse[0]:
            self.keydown = False
            self.outside_rect_keypress = True
            return False

        if self.outside_rect_keypress and pressed_mouse[0] == False:
            self.keydown = False
            self.outside_rect_keypress = False
            return False
    
        if self.outside_rect_keypress == True:
            return False

        if mouse_inside_rect and pressed_mouse[0]:
            self.keydown = True
            return False

        if self.mouse_inside_rect_previous == False:
            self.keydown = False
            return False

        if self.keydown and mouse_inside_rect and pressed_mouse[0] == False:
            print("Button clicked!")
            self.keydown = False
            return True
        else:
            # print("false")
            self.keydown = False

        return False


class Menu:
    visibility = False
    choice = 0 #0 - none, 1 - start, 2 - exit

    def __init__(self):
        print("Initializing Menu")
        self.start_button = Button("./resources/images/start.png", (300, 360))
        self.end_button = Button("./resources/images/exit.png", (300, 540))
        #Dodać jakiś ładny border menu?
        self.visibility = True

    def execute_choice(self):
        if self.choice == 0:
            pass
        elif self.choice == 1:
            self.visibility = False
            return 1
        elif self.choice == 2:
            print("Exiting game, thank you for playing!")
            pygame.event.post(pygame.event.Event(pygame.QUIT))
            return None

    def draw(self, surface):
        if self.visibility:
            self.start_button.draw_button(surface)
            self.end_button.draw_button(surface)
        else:
            pass #Dodaj funkcje które usuną przyciski etc

    def update(self):
        start_pressed = self.start_button.update()
        end_pressed = self.end_button.update()

        if start_pressed == True:
            self.choice = 1
        elif end_pressed == True:
            self.choice = 2

class Game:

    def __init__(self, mode):
        self.mode = mode



class Player:
    score = 0
    def __init__(self, nickname):
        self.nickname = nickname

class Deck:
    cards = []

    def __init__(self, player_id):
        self.player_id = player_id

class Card:
    stack_number = 0
    in_deck = False

    def __init__(self, name):
        self.name = name


    # def draw():



BACKGROUND_COLOR = (237, 204, 139)

def main():

    pygame.init()
    pygame.display.set_caption("Wybuchające koty")
    screen = pygame.display.set_mode((600, 800))
    screen.fill(BACKGROUND_COLOR)
    FPS = pygame.time.Clock()
    FPS.tick(60)

    menu = Menu()
    menu.draw(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
                
        menu.update()
        menu_choice = menu.execute_choice()
        if menu_choice == 1:
            game = Game(1)
        pygame.display.update()
        
        




if __name__=="__main__":
    main()
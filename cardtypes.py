import pygame

class Card:
    stack_position = (150, 385)
    obverse_image_path = "./resources/images/cards/image-023.jpg"

    def __init__(self):
        self.stack_number = 0
        self.in_deck = False
        self.visibility = False
        self.obverse = False
        self.image_scale = (110, 160)
        self.center_coords = None
        self.card_used = False
        print("Creating card")

    def load_image(self, center_coords):
        if self.center_coords == None:
            self.center_coords = center_coords
            print(f"Creating card at: {center_coords}")

        
        self.image = None
        if self.obverse == False:
            self.image = pygame.image.load(self.obverse_image_path)
        else:    
            self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, self.image_scale)
        self.rect = self.image.get_rect()
        self.rect.center = self.center_coords
        self.visibility = True

    def place_card(self, center_coords):
        if self.card_used == False:
            self.center_coords = center_coords

    def draw(self, surface):
        if not self.visibility:
            return
        surface.blit(self.image, self.rect)

    def use_card(self):
        self.card_used = True
        self.center_coords = self.stack_position


    def update(self, width_offset):
        if not self.visibility:
            return False
        self.rect.update(self.rect.x, self.rect.y, self.rect.width-width_offset, self.rect.height)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_inside_rect = self.rect.collidepoint(mouse_pos)
        pressed_mouse = pygame.mouse.get_pressed()

        if mouse_inside_rect:
            self.image_scale = (220, 320)
        elif mouse_inside_rect == False:
            self.image_scale = (110, 160)

        if mouse_inside_rect and pressed_mouse[0]:
            self.use_card()
            return True

        return False


class ExplodingCat(Card):
    image_path = "./resources/images/cards/image-023.jpg"
    card_type = 0

    def __init__(self, center_coords):
        super().__init__()
        self.load_image(center_coords)
        print("ExplodingCat card created")

class Defuse(Card):
    image_path = "./resources/images/cards/image-000.jpg"
    card_type = 1

    def __init__(self, center_coords):
        super().__init__()
        self.load_image(center_coords)
        print("Defuse card created")

class Defuse_1(Defuse):
    image_path =  "./resources/images/cards/image-001.jpg"

class Defuse_2(Defuse):
    image_path =  "./resources/images/cards/image-002.jpg"

class TacoCat(Card):
    image_path = "./resources/images/cards/image-003.jpg"
    card_type = 2

    def __init__(self, center_coords):
        super().__init__()
        self.load_image(center_coords)
        print("TacoCat card created")

class RainbowCat(Card):
    image_path = "./resources/images/cards/image-004.jpg"
    card_type = 3

    def __init__(self, center_coords):
        super().__init__()
        self.load_image(center_coords)
        print("RainbowCat card created")

class BeardCat(Card):
    image_path = "./resources/images/cards/image-005.jpg"
    card_type = 4

    def __init__(self, center_coords):
        super().__init__()
        self.load_image(center_coords)
        print("BeardCat card created")


class Favor(Card):
    image_path = "./resources/images/cards/image-006.jpg"
    card_type = 5

    def __init__(self, center_coords):
        super().__init__()
        self.load_image(center_coords)
        print("Favor card created")

class Favor_1(Favor):
    image_path =  "./resources/images/cards/image-007.jpg"

class Favor_2(Favor):
    image_path =  "./resources/images/cards/image-008.jpg"
import pygame
import time
import itertools

class Card:
    stack_position = (150, 385)
    reverse_image_path = "./resources/images/cards/image-023.jpg"
    reverse_image = None
    id_iter = itertools.count()

    def __init__(self):
        self.id = next(self.id_iter)
        self.stack_number = 0
        self.in_deck = False
        self.visibility = False
        self.obverse = False
        self.image_scale = (110, 160)
        self.center_coords = None
        self.card_used = False
        self.reverse_image = pygame.image.load(self.reverse_image_path).convert_alpha()
        print("Creating card")

    def __repr__(self):
        return f"id: {self.id}"

    def load_image(self, center_coords):
        if self.center_coords == None:
            self.center_coords = center_coords
            print(f"Creating card at: {center_coords}")

        
        self.image = None
        if self.obverse == False:
            self.image = self.reverse_image
        else:    
            self.image = self.card_image
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
        self.obverse = True

    def reveal_card(self, position):
        self.obverse = True
        self.image = self.card_image
        self.center_coords = position
        self.rect.update((position), (self.rect.width, self.rect.height))


    def update(self, width_offset, ai_turn=False):
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

        if ai_turn:
            self.use_card()
            return True

        if mouse_inside_rect and pressed_mouse[0]:
            self.use_card()
            time.sleep(0.1)
            return True

        return False


class ExplodingCat(Card):
    image_path = "./resources/images/cards/image-015.jpg"
    card_type = 0

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("ExplodingCat card created")

    def __repr__(self):
        return "Exploding Cat" + super().__repr__()

class Defuse(Card):
    image_path = "./resources/images/cards/image-000.jpg"
    card_type = 1

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("Defuse card created")

    def __repr__(self):
        return "Defuse " + super().__repr__()

class Defuse_1(Defuse):
    image_path =  "./resources/images/cards/image-001.jpg"

class Defuse_2(Defuse):
    image_path =  "./resources/images/cards/image-002.jpg"

class TacoCat(Card):
    image_path = "./resources/images/cards/image-003.jpg"
    card_type = 2

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("TacoCat card created")

    def __repr__(self):
        return "Taco Cat " + super().__repr__()

class RainbowCat(Card):
    image_path = "./resources/images/cards/image-004.jpg"
    card_type = 3

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("RainbowCat card created")

    def __repr__(self):
        return "Rainbow Cat " + super().__repr__()

class BeardCat(Card):
    image_path = "./resources/images/cards/image-005.jpg"
    card_type = 4

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("BeardCat card created")

    def __repr__(self):
        return "Beard Cat " + super().__repr__()


class Favor(Card):
    image_path = "./resources/images/cards/image-006.jpg"
    card_type = 5

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("Favor card created")

    def __repr__(self):
        return "Favor " + super().__repr__()

class Favor_1(Favor):
    image_path =  "./resources/images/cards/image-007.jpg"

class Favor_2(Favor):
    image_path =  "./resources/images/cards/image-008.jpg"

class Skip(Card):
    image_path = "./resources/images/cards/image-009.jpg"
    card_type = 6

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("Skip card created")

    def __repr__(self):
        return "Skip " + super().__repr__()

class Skip_1(Skip):
    image_path =  "./resources/images/cards/image-010.jpg"

class Skip_2(Skip):
    image_path =  "./resources/images/cards/image-011.jpg"

class Reveal(Card):
    image_path = "./resources/images/cards/image-012.jpg"
    card_type = 7

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("Reveal card created")

    def __repr__(self):
        return "Reveal " + super().__repr__()

class Reveal_1(Reveal):
    image_path =  "./resources/images/cards/image-013.jpg"

class Reveal_2(Reveal):
    image_path =  "./resources/images/cards/image-014.jpg"


class Attack(Card):
    image_path = "./resources/images/cards/image-016.jpg"
    card_type = 8

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("Attack card created")

    def __repr__(self):
        return "Attack " + super().__repr__()

class Attack_1(Attack):
    image_path =  "./resources/images/cards/image-017.jpg"

class Shuffle(Card):
    image_path = "./resources/images/cards/image-018.jpg"
    card_type = 9

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("Shuffle card created")

    def __repr__(self):
        return "Shuffle " + super().__repr__()

class Shuffle_1(Shuffle):
    image_path =  "./resources/images/cards/image-019.jpg"

class Nope(Card):
    image_path = "./resources/images/cards/image-020.jpg"
    card_type = 10

    def __init__(self, center_coords):
        super().__init__()
        self.card_image = pygame.image.load(self.image_path).convert_alpha()
        self.load_image(center_coords)
        print("Nope card created")

    def __repr__(self):
        return "Nope " + super().__repr__()

class Nope_1(Nope):
    image_path = "./resources/images/cards/image-021.jpg"

class Nope_2(Nope):
    image_path = "./resources/images/cards/image-022.jpg"

import pygame

class Card:
    def __init__(self):
        self.stack_number = 0
        self.in_deck = False
        self.visibility = False
        print("Creating card")

    def load_image(self, center_coords):
        print(f"Creating card at: {center_coords}")
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale_by(self.image, 0.10)
        self.rect = self.image.get_rect()
        self.rect.center = center_coords
        self.visibility = True

    def draw(self, surface):
        if not self.visibility:
            return
        surface.blit(self.image, self.rect)

    def update(self):
        pass


class ExplodingCat(Card):
    image_path = "./resources/images/cards/image-002.jpg"
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
    image_path =  "./resources/images/cards/image-001.jpg"

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

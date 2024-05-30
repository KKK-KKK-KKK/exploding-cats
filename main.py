import pygame
import sys
import random
from menu import Menu
from cardtypes import *

class Game:
    visibility = False
    player_one = None
    player_two = None
    deck = None
    dealt_hands = False
    card_debug = False

    def __init__(self, mode):
        self.mode = mode
        self.background_image = pygame.image.load("./resources/images/background.jpg")

    def set_players(self, nickname_first, nickname_second):
        if self.player_one is None and self.player_two is None:
            self.player_one = Player(nickname_first)
            self.player_two = Player(nickname_second)

    def remove_players(self):
        self.player_one = None
        self.player_two = None

    def prepare_deck(self, amount):
        if self.deck is None:
            self.deck = Deck()
            self.deck.fill_deck(amount)

    def prepare_hands(self, draw_amount):
        if self.dealt_hands:
            return
        print("Preparing starting hands")
        for i in range(draw_amount):
            print(f"Preparing starting hands, iteration: {i}")
            self.player_one.hand.draw_from_deck_start(self.deck)
            self.player_two.hand.draw_from_deck_start(self.deck)
        print(f"Preparing starting hands, drawing defuse")
        self.player_one.hand.draw_from_deck_defuse(self.deck)
        self.player_two.hand.draw_from_deck_defuse(self.deck)
        print(f"Preparing starting hands finished")
        self.player_one.hand.print_hand()
        self.player_two.hand.print_hand()
        self.dealt_hands = True

    def create_card_debug(self, surface):
        if not self.card_debug:
            card = Defuse((80, 650))
            card.draw(surface)
            card = Defuse((80, 130))
            card.draw(surface)
            self.card_debug = True

    def hide(self):
        if not self.visibility:
            return
        print("Hiding game")
        self.visibility = False

    def reveal(self):
        if self.visibility:
            return
        print("Revealing game")
        self.visibility = True

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))  # Rysowanie tła jako pierwsze
        if self.deck:
            self.deck.draw(screen)
        if self.player_one and self.player_two:
            self.player_one.hand.draw(screen, "top")
            self.player_two.hand.draw(screen, "bottom")

    def update(self):
        pass



class Deck:
    card_types = [0, 1, 2, 3, 4]  # always add enum when a new card is added to deck
    __MAX_EXPLOSIVE = 4
    __MAX_DEFUSE = 6

    def __init__(self):
        self.cards = []
        self.already_filled = False
        self.visibility = False
        print("Deck created")

    def fill_deck(self, amount):
        def get_card_type(card_type, center_coords):
            card_version = random.choice([0, 1, 2])

            if card_type == 0:
                return ExplodingCat(center_coords)
            elif card_type == 1:
                if card_version == 0:
                    return Defuse(center_coords)
                if card_version == 1:
                    return Defuse_1(center_coords)
                if card_version == 2:
                    return Defuse_2(center_coords)
            elif card_type == 2:
                return TacoCat(center_coords)
            elif card_type == 3:
                return RainbowCat(center_coords)
            elif card_type == 4:
                return BeardCat(center_coords)
            else:
                try:
                    raise Exception("Incorrect card type selected in deck", "Exiting game")
                except Exception as error:
                    print(error.args)
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if self.already_filled:
            return

        print("Filling deck with cards")
        card_types_deep_copy = self.card_types.copy()

        def skip_max_card_type(card_types_deep_copy, card_type_id, max):
            type_cats_cards = list(filter(lambda x: (x.card_type == card_type_id), self.cards))
            if len(type_cats_cards) == max:
                try:
                    idx = card_types_deep_copy.index(card_type_id)
                    card_types_deep_copy.pop(idx)
                except:
                    pass
            return card_types_deep_copy

        for i in range(amount):
            card = random.choice(card_types_deep_copy)
            self.cards.append(get_card_type(card, (300, 300)))

            # if max amount of card reached, then remove from card_types_deep_copy
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 0, self.__MAX_EXPLOSIVE)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 1, self.__MAX_DEFUSE)

        self.already_filled = True

    def draw_card(self):
        return self.cards.pop()

    def draw_card_no_explosion_no_defuse(self):
        viable_card = self.__pop_viable_card(self.__check_type_no_explosion_no_defuse)
        return viable_card

    def draw_card_defuse(self):
        viable_card = self.__pop_viable_card(self.__check_type_defuse)
        return viable_card

    def draw(self, surface):
        for i in range(len(self.cards)):
            self.cards[i].load_image((300, 400))
            self.cards[i].draw(surface)
        self.visibility = True

    def __check_type_no_explosion_no_defuse(self, card):
        if card.card_type == 0 or card.card_type == 1:
            return False
        return True

    def __check_type_defuse(self, card):
        if card.card_type == 1:
            return True
        return False

    def __pop_viable_card(self, check_type):
        viable_card = next(filter(check_type, self.cards), None)
        card_index = self.cards.index(viable_card)
        viable_card = self.cards.pop(card_index)  # remove the card from deck
        try:
            if not check_type(viable_card):
                raise Exception("Incorrect card type was chosen while drawing viable card",
                                f"type: {viable_card.card_type} at index: {card_index}")
        except Exception as error:
            print(error.args)
            pygame.event.post(pygame.event.Event(pygame.QUIT))

        return viable_card


class Player:
    def __init__(self, nickname):
        self.score = 0
        self.nickname = nickname
        self.hand = Hand()

    def update(self):
        pass

class Hand:
    def __init__(self):
        self.cards = []
        self.amount = 0
        print("Hand created")

    def draw_from_deck(self, deck):
        self.cards.append(deck.draw_card())
        self.amount = len(self.cards)

    def draw_from_deck_start(self, deck):
        self.cards.append(deck.draw_card_no_explosion_no_defuse())
        print(self.cards)
        self.amount = len(self.cards)

    def draw_from_deck_defuse(self, deck):
        self.cards.append(deck.draw_card_defuse())
        self.amount = len(self.cards)

    def print_hand(self):
        cards = [card.card_type for card in self.cards]
        print(cards)

    def draw(self, surface, side):
        offset_y = 650 if side == "top" else 130
        for i in range(len(self.cards)):
            self.cards[i].load_image((60 + i * 50, offset_y))
            self.cards[i].draw(surface)







    

def main():
    pygame.init()
    pygame.display.set_caption("Wybuchające koty")
    screen = pygame.display.set_mode((600, 800))
    background_menu_image = pygame.image.load("./resources/images/background_menu.jpg")
    FPS = pygame.time.Clock()
    FPS.tick(60)

    menu = Menu()
    game = Game(1)
    show_menu = True

    DRAW_AMOUNT = 7
    DECK_SIZE = 32

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if show_menu:
            screen.blit(background_menu_image, (0, 0))
            menu.draw(screen)
            menu.update()
            menu_choice = menu.execute_choice()
            if menu_choice == 1:
                show_menu = False
                menu.hide()
                game.reveal()
                game.prepare_deck(DECK_SIZE)
                game.set_players("Player1", "Player2")
                game.prepare_hands(DRAW_AMOUNT)
        else:
            game.draw(screen)

        pygame.display.update()

if __name__ == "__main__":
    main()

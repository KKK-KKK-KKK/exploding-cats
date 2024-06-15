import pygame
import sys
import random
import time
from menu import Menu
from button import Button
from cardtypes import *


class Sound:
    cat_sounds_path = "./resources/cat-sounds/"
    meow_sounds = []
    music = None

    def __init__(self):
        self.meow_sounds = [
                    pygame.mixer.Sound(self.cat_sounds_path + "angry-kitty.wav"),
                    pygame.mixer.Sound(self.cat_sounds_path + "angry-roar.wav"),
                    pygame.mixer.Sound(self.cat_sounds_path + "little-cat-pain.wav"),
                    pygame.mixer.Sound(self.cat_sounds_path + "little-meow-attention.wav"),
                    pygame.mixer.Sound(self.cat_sounds_path + "little-meow.wav"),
                    pygame.mixer.Sound(self.cat_sounds_path + "sweet-meow.wav"),
                ] 
        self.music = pygame.mixer.Sound(self.cat_sounds_path + "battle-theme.mp3")

    def play_meow(self):
        rdn = random.randrange(len(self.meow_sounds))
        self.meow_sounds[rdn].play()

    def play_music(self):
        self.music.play(loops=-1)

    def stop_music(self):
        self.music.stop()


class Game:
    visibility = False
    player_one = None
    player_two = None
    deck = None
    dealt_hands = False
    card_debug = False
    pass_image_path = "./resources/images/pass.png"
    player_two_pass_button = None
    winner = 0
    sounds = None
    

    def __init__(self, mode):
        self.mode = mode
        self.background_image = pygame.image.load("./resources/images/background.jpg")
        self.sounds = Sound()
        

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

    def create_stack(self):
        self.stack = Stack()

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

    def start_music(self):
        self.sounds.play_music()
    
    def stop_music(self):
        self.sounds.stop_music()

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

    def reveal_player_two_cards(self):
        self.player_two.hand.reveal_hand()

    def draw_player_two_pass_button(self, surface):
        if self.player_two_pass_button is None:
            self.player_two_pass_button = Button(self.pass_image_path, (500,500))
        self.player_two_pass_button.draw_button(surface)

    def draw_end(self, screen):
        winner_path = ""
        if self.winner == 1:
            winner_path = "winner1.png"
        elif self.winner == 2:
            winner_path = "winner2.png"
        else:
            raise Exception("Wrong value of winner in draw_end", "Exiting game")
        end_image = pygame.image.load(f"./resources/images/{winner_path}")
        screen.blit(end_image, (0, 0))

    def draw(self, screen):
        screen.blit(self.background_image, (0, 0))
        if self.deck:
            self.deck.draw(screen)
        if self.player_one and self.player_two:
            self.player_one.hand.draw(screen, "top")
            self.player_two.hand.draw(screen, "bottom")
            self.draw_player_two_pass_button(screen)
            self.stack.draw(screen)

    def update(self):
        def do_card_action(player_user, player_target, card_type):
            if card_type == 0:
                print("ExplosiveCat action executing")
                #check for defuse
                #end game if not present
            elif card_type == 1:
                pass #Defuse
            elif card_type == 2: 
                print("TacoCat action executing")
                if len(self.stack.cards) > 1 and self.stack.cards[-2].card_type == 2:
                    print("Stealing card")
                    stolen_card = player_target.hand.pop_from_hand()
                    player_user.hand.push_to_hand(stolen_card)
            elif card_type == 3:
                print("RainbowCat action executing")
                if len(self.stack.cards) > 1 and self.stack.cards[-2].card_type == 3:
                    print("Stealing card")
                    stolen_card = player_target.hand.pop_from_hand()
                    player_user.hand.push_to_hand(stolen_card)
            elif card_type == 4:
                print("BeardCat action executing")
                if len(self.stack.cards) > 1 and self.stack.cards[-2].card_type == 4:
                    print("Stealing card")
                    stolen_card = player_target.hand.pop_from_hand()
                    player_user.hand.push_to_hand(stolen_card)
            elif card_type == 5:
                print("Favor action executing")
                stolen_card = player_target.hand.pop_from_hand()
                player_user.hand.push_to_hand(stolen_card) 
            elif card_type == 6:
                print("Skip action executing")
                player_user.skip = True
            elif card_type == 7:
                print("Reveal action executing")
                self.deck.cards[-1].reveal_card((350,300))
                if len(self.deck.cards) > 1:
                    self.deck.cards[-2].reveal_card((420,300))
                if len(self.deck.cards) > 2:
                    self.deck.cards[-3].reveal_card((490,300))
            elif card_type == 8:
                print("Attack action executing")
                player_user.skip = True
                player_target.double_throw = True
                #Skip turn. Enemy player has to play cards twice.
                return 8
            elif card_type == 9:
                print("Shuffle action executing")
                print(self.deck.cards)
                random.shuffle(self.deck.cards)
                print(self.deck.cards)
                pass
            # elif card_type == 10:
            #     print("Nope action executing")
            #     pass

            return False
        


        #Hotseat version
        # popped_card = self.player_one.hand.update()
        # if popped_card is not None:
        #     self.stack.update(popped_card)
        #     do_card_action(self.player_one, self.player_two, popped_card.card_type) #act upon the type of the card
           
        popped_card = self.player_two.hand.update()
        card_action = None
        if popped_card is not None:
            self.stack.update(popped_card)
            card_action = do_card_action(self.player_two, self.player_one, popped_card.card_type) #act upon the type of the card
            self.sounds.play_meow()
            self.player_two.hand.reveal_hand()
            self.player_one.hand.hide_hand()
        passed = self.player_two_pass_button.update()
        if passed:
            if self.player_two.skip == False:
                avoid_death = self.player_two.hand.pass_turn(self.deck)
                if avoid_death == 3:
                    return 1
                elif avoid_death == 2:
                    print("asd")
                    pass
                elif avoid_death.card_type == 0:
                    print("asd2")
                    self.deck.insert_card(avoid_death)
                
            self.player_two.hand.reveal_hand()
            #AI player turn
            popped_card = self.player_one.AI_turn()
            if popped_card is not None:
                self.stack.update(popped_card)
                do_card_action(self.player_one, self.player_two, popped_card.card_type)
                if self.player_one.double_throw == True:
                    popped_card = self.player_one.AI_turn()
                    self.stack.update(popped_card)
                    do_card_action(self.player_one, self.player_two, popped_card.card_type)

            if self.player_one.skip == False:
                avoid_death = self.player_one.hand.pass_turn(self.deck)
                if avoid_death == 3:
                    return 2
                elif avoid_death == 2:
                    print("asd")
                    pass
                elif avoid_death.card_type == 0:
                    print("asd2")
                    self.deck.insert_card(avoid_death)
               
            self.player_one.skip = False
            self.player_one.double_throw = False
            self.player_two.skip = False
            self.player_two.double_throw = False
            self.player_one.hand.hide_hand()
        return 0


class Deck:
    card_types = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # always add enum when a new card is added to deck
    __MAX_EXPLOSIVE = 1
    __MAX_DEFUSE = 3
    __MAX_TACOCAT = 4
    __MAX_RAINBOWCAT = 4
    __MAX_BEARDCAT = 4
    __MAX_FAVOR = 3
    __MAX_SKIP = 3
    __MAX_REVEAL = 3
    # __MAX_NOPE = 3
    __MAX_SHUFFLE = 2
    __MAX_ATTACK = 2

    def __init__(self):
        self.cards = []
        self.already_filled = False
        self.visibility = False
        print("Deck created")

    def fill_deck(self, amount):
        def get_card_type(card_type, center_coords):
            card_version = random.choice([0, 1, 2])
            card_version_lesser = random.choice([0,1])

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
            elif card_type == 5:
                if card_version == 0:
                    return Favor(center_coords)
                if card_version == 1:
                    return Favor_1(center_coords)
                if card_version == 2:
                    return Favor_2(center_coords)
            elif card_type == 6:
                if card_version == 0:
                    return Skip(center_coords)
                if card_version == 1:
                    return Skip_1(center_coords)
                if card_version == 2:
                    return Skip_2(center_coords)
            elif card_type == 7:
                if card_version == 0:
                    return Reveal(center_coords)
                if card_version == 1:
                    return Reveal_1(center_coords)
                if card_version == 2:
                    return Reveal_2(center_coords)
            elif card_type == 8:
                if card_version_lesser == 0:
                    return Attack(center_coords)
                if card_version_lesser == 1:
                    return Attack_1(center_coords)
            elif card_type == 9:
                if card_version_lesser == 0:
                    return Shuffle(center_coords)
                if card_version_lesser == 1:
                    return Shuffle_1(center_coords)
            # elif card_type == 10:
            #     if card_version == 0:
            #         return Nope(center_coords)
            #     if card_version == 1:
            #         return Nope_1(center_coords)
            #     if card_version == 2:
            #         return Nope_2(center_coords)
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
            self.cards.append(get_card_type(card, (350, 300)))

            # if max amount of card reached, then remove from card_types_deep_copy
            #TODO: refactor it into a loop and a function
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 0, self.__MAX_EXPLOSIVE)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 1, self.__MAX_DEFUSE)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 2, self.__MAX_TACOCAT)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 3, self.__MAX_RAINBOWCAT)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 4, self.__MAX_BEARDCAT)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 5, self.__MAX_FAVOR)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 6, self.__MAX_SKIP)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 7, self.__MAX_REVEAL)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 8, self.__MAX_ATTACK)
            card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 9, self.__MAX_SHUFFLE)
            # card_types_deep_copy = skip_max_card_type(card_types_deep_copy, 10, self.__MAX_NOPE)

        self.already_filled = True

    def insert_card(self, card):
        random_index = 0
        if len(self.cards) < 1:
            random_index = 0
        else:
            try:
                random_index = random.randrange(0, len(self.cards)-1)
            except Exception as e:
                top_index = 0
        self.cards.insert(random_index, card)
        for i in range(0, len(self.cards)):
            self.cards[i].update(0)

    def draw_card(self):
        return self.cards.pop()

    def draw_card_no_explosion_no_defuse(self):
        viable_card = self.__pop_viable_card(self.__check_type_no_explosion_no_defuse)
        return viable_card

    def draw_card_defuse(self):
        viable_card = self.__pop_viable_card(self.__check_type_defuse)
        return viable_card

    def draw(self, surface):
        last_cards = []
        if len(self.cards) > 2:
            last_cards = [self.cards[-1], self.cards[-2], self.cards[-3]]
        elif len(self.cards) == 2:
            last_cards = [self.cards[-1], self.cards[-2]]
        elif len(self.cards) == 1:
            last_cards = [self.cards[-1]]

        for i in range(0, len(last_cards)):
            last_cards[i].load_image((300, 400))
            last_cards[i].draw(surface)
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

class Stack:
    stack_position = (150, 385) #this variable doesn't dictate location during game loop, look at Card class instead

    def __init__(self):
        self.cards = []
        self.already_filled = False
        self.visibility = False
        print("Stack created")

    def draw(self, surface):
        stack_cards_size = len(self.cards) 
        if stack_cards_size > 0:
            self.cards[stack_cards_size-1].load_image(self.stack_position)
            self.cards[stack_cards_size-1].place_card(self.stack_position)
            self.cards[stack_cards_size-1].draw(surface)

    def update(self, popped_card):
        if popped_card == None:
            return

        self.cards.append(popped_card)
        for i in range(0, len(self.cards)):
            self.cards[i].update(0)


class Player:
    def __init__(self, nickname):
        self.score = 0
        self.nickname = nickname
        self.double_throw = False
        self.skip = False
        self.hand = Hand()

    def AI_turn(self):
        time.sleep(0.4)
        popped_card = self.hand.update(True) #could be changed to "cards" and accept array
        return popped_card

    def update(self):
        pass

class Hand:
    width_offset = 55

    def __init__(self):
        self.cards = []
        self.amount = 0
        print("Hand created")

    def has_defuse(self):
        for i in range(0, len(self.cards)):
            if self.cards[i].card_type == 1:
                return i
        return -1

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

    def pop_from_hand(self):
        if len(self.cards) > 0:
            card = self.cards.pop()
        else:
            card = None
        return card 

    def push_to_hand(self, card):
        self.cards.append(card)

    def pass_turn(self, deck):
        drawn_card = deck.draw_card()
        if drawn_card.card_type == 0:
            avoid_death = self.has_defuse()
            if avoid_death == -1:
                return 3
            else:
                return drawn_card


        self.cards.append(drawn_card)
        return 2

    def reveal_hand(self):
        for i in range(0, len(self.cards)):
            self.cards[i].obverse = True

    def hide_hand(self):
        for i in range(0, len(self.cards)):
            self.cards[i].obverse = False

    def print_hand(self):
        cards = [card.card_type for card in self.cards]
        print(cards)

    def draw(self, surface, side):
        if side == "top":
            offset_y = 130
        elif side == "bottom":
            offset_y = 650
        for i in range(len(self.cards)): #TODO: popraw ułożenie kart
            if i == 10 and side == "bottom":
                offset_y += 30
            if i == 10 and side == "top":
                offset_y -= 30
            self.cards[i].load_image((60, 130))
            self.cards[i].place_card((60 + i * self.width_offset, offset_y))
            self.cards[i].draw(surface)

    
    def update(self, ai_turn=False):
        top_index = -1
        if ai_turn:
            if len(self.cards) < 1:
                return None
            try:
                top_index = random.randrange(len(self.cards)-1)
            except Exception as e:
                top_index = 0
            self.cards[top_index].update(self.width_offset, True)
            print(self.cards)
            print(f"Hand cards length: {len(self.cards)-1}")
            print(f"top_index: {top_index}")
            return self.cards.pop(top_index)

        for i in range(0, len(self.cards)):
            put_card_on_stack = self.cards[i].update(self.width_offset)
            if put_card_on_stack:
                top_index = i

        if top_index != -1:
            print(self.cards)
            print(f"Hand cards length: {len(self.cards)-1}")
            print(f"top_index: {top_index}")
            return self.cards.pop(top_index)
        
        return None
            








    

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
    show_game = False
    show_end = False

    DRAW_AMOUNT = 7
    # DECK_SIZE = 32
    DECK_SIZE = 29 #No Nope cards
    pygame.event.set_allowed([pygame.QUIT]) #remember to add events if needed

    while(1):
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
                show_game = True
                menu.hide()
                game.reveal()
                game.prepare_deck(DECK_SIZE)
                game.set_players("Player1", "Player2")
                game.prepare_hands(DRAW_AMOUNT)
                game.create_stack()
                game.reveal_player_two_cards()
                game.start_music()
                
        elif show_game:
            game.draw(screen)
            winner = game.update()
            game.winner = winner
            if winner != 0:
                show_game = False
                show_end = True
        elif show_end:
            game.draw_end(screen)
            game.stop_music()
        pygame.display.update()

if __name__ == "__main__":
    main()

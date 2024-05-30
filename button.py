import pygame


class Button:
    keydown = False
    outside_rect_keypress = False
    visibility = False

    def __init__(self, image_path, center_coords):
        print(f"Creating button with image: {image_path} at: {center_coords}")
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.center = center_coords
        self.visibility = True

    def draw_button(self, surface):
        if not self.visibility:
            return
        surface.blit(self.image, self.rect)

    def draw_hover_animation(self):
        pass

    def draw_click_animation(self):
        pass

    def hide(self):
        if not self.visibility:
            return
        print("Hiding button")
        self.visibility = False

    def reveal(self):
        if self.visibility:
            return
        print("Revealing button")
        self.visibility = True

    def update(self):
        if not self.visibility:
            return False
        mouse_pos = pygame.mouse.get_pos()
        mouse_inside_rect = self.rect.collidepoint(mouse_pos)
        pressed_mouse = pygame.mouse.get_pressed()
        self.mouse_inside_rect_previous = mouse_inside_rect

        if not mouse_inside_rect and pressed_mouse[0]:
            self.keydown = False
            self.outside_rect_keypress = True
            return False

        if self.outside_rect_keypress and not pressed_mouse[0]:
            self.keydown = False
            self.outside_rect_keypress = False
            return False

        if self.outside_rect_keypress:
            return False

        if mouse_inside_rect and pressed_mouse[0]:
            self.keydown = True
            return False

        if not self.mouse_inside_rect_previous:
            self.keydown = False
            return False

        if self.keydown and mouse_inside_rect and not pressed_mouse[0]:
            print("Button clicked!")
            self.keydown = False
            return True
        else:
            self.keydown = False

        return False



import pygame
import pygame.freetype
from pygame.sprite import Sprite 
from pygame.rect import Rect 
from enum import Enum
from pygame.sprite import RenderUpdates

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
	""" Returns surface with text written on """
	font = pygame.freetype.SysFont("Times New Roman", font_size, bold=True)
	surface, st = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
	return surface.convert_alpha()

class Player:

	def __init__(self, score=0, lives=3, current_level = 1):
		self.score = score
		self.lives = lives 
		self.current_level = current_level

class UIElement(Sprite):

	def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
		
		self.mouse_over = False
		default_image = create_surface_with_text(text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb)
		highlighted_image = create_surface_with_text(text=text, font_size=font_size * 2, text_rgb=text_rgb, bg_rgb=bg_rgb)

		self.images = [default_image, highlighted_image]
		self.rects = [
			  default_image.get_rect(center=center_position),
			  highlighted_image.get_rect(center=center_position)
		]

		super().__init__()

		self.action = action

	def image(self):
		return self.images[1] if self.mouse_over else self.images[0]

	def rect(self):
		return self.rects[1] if self.mouse_over else self.rects[0]

	def update(self, mouse_pos, mouse_up):
		if self.rect().collidepoint(mouse_pos):
			self.mouse_over = True
			if mouse_up:
				return self.action
		else:
			self.mouse_over = False

	def draw(self, surface):
		surface.blit(self.image(), self.rect())

class GameState(Enum):
	QUIT = -1
	TITLE = 0
	NEWGAME = 1
	NEXT_LEVEL = 2


def game_loop(screen, buttons):

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)
    			
        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()


def play_level(screen, player):

    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Next level ({player.current_level + 1})",
        action=GameState.NEXT_LEVEL,
    )


    buttons = RenderUpdates(return_btn, nextlevel_btn)

    return game_loop(screen, buttons)


def title_screen(screen):

    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(start_btn, quit_btn)

    return game_loop(screen, buttons)

def main():
	pygame.init()

	screen = pygame.display.set_mode((800, 600))
	game_state = GameState.TITLE

	while True:
		if game_state == GameState.TITLE:
			game_state = title_screen(screen)

		if game_state == GameState.NEWGAME:
			player = Player()
			game_state = play_level(screen, player)

		if game_state == GameState.NEXT_LEVEL:
			player.current_level += 1
			game_state = play_level(screen, player)

		if game_state == GameState.QUIT:
			pygame.quit()
			return

if __name__ == "__main__":
	main()
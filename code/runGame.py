import pygame
import sys
import numpy as np
from game import *
import nashpy as nash

BACKGROUND_COLOR = (200,200,200);
BOARD_COLOR = (255,255,255);

square_size = 84;
square_spacing = 96;

font_size = 32


class GameRunner:
    def __init__(self) -> None:
        pygame.init();

        self.WIDTH, self.HEIGHT = 1280, 720;

        # Create the Pygame screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT));
        pygame.display.set_caption("Village Game");
    
        self.font = pygame.font.Font(None, font_size)

    def run(self):
        village_game = Game(0.1, 0.8, 2, 0.1, 0.2, 100, 100);

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();

            (game, resources) = village_game.get_round();

            utilities = [game.payoff_matrices[0], game.payoff_matrices[1]];
            # Fill the background color
            self.screen.fill(BACKGROUND_COLOR);

            self.__plot_matchup__(utilities, resources);

            pygame.display.flip();

            pygame.time.Clock().tick(10);

            village_game.run(game);

    def __plot_matchup__(self, utilities: list[np.ndarray], resources: np.ndarray):

        board0_corner = np.array([64,64]);
        board1_corner = np.array([square_spacing*6 + 64,64]);

        self.__draw_board__(board0_corner, utilities[0]);
        self.__draw_board__(board1_corner, utilities[1]);
    
        number_text = self.font.render('Resources: '+str(resources[0]), True, (0, 0, 0));
        number_rect = number_text.get_rect(center=board0_corner + np.array([64, -32]));
        self.screen.blit(number_text, number_rect);
    
        number_text = self.font.render('Resources: '+str(resources[1]), True, (0, 0, 0));
        number_rect = number_text.get_rect(center=board1_corner + np.array([64, -32]));
        self.screen.blit(number_text, number_rect);
    def __draw_board__(self, origin: np.ndarray, utilities: np.ndarray):
        for i in range(3):
            for j in range(3):
                rect = pygame.draw.rect(self.screen, BOARD_COLOR, (origin[0]+square_spacing*i, origin[1]+square_spacing*j, square_size, square_size));

                number_text = self.font.render(str(utilities[i,j]), True, (0, 0, 0));
                number_rect = number_text.get_rect(center=rect.center);
                self.screen.blit(number_text, number_rect);

if __name__ == "__main__":
    game = GameRunner();
    game.run();
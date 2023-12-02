import pygame
import sys
import numpy as np
from game import *

BACKGROUND_COLOR = (200,200,200);
BOARD_COLOR = (255,255,255);

RAID_COLOR = (255,0,0);
HARVEST_COLOR = (0,255,0);
TRADE_COLOR = (0,0,255);

square_size = 84;
square_spacing = 96;

font_size = 32

game_tick = 0.5;
fps = 60;


class GameRunner:
    def __init__(self) -> None:
        pygame.init();

        self.WIDTH, self.HEIGHT = 1280, 720;

        # Create the Pygame screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT));
        pygame.display.set_caption("Village Game");
    
        self.font = pygame.font.Font(None, font_size)

    def run(self):
        village_game = Game(0.4, 0.8, 2, 0.2, 0.6, 100, 100);
        update_game_timer = game_tick;

        (game, resources) = village_game.get_round();
        prev_action = village_game.run(game);

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();

            utilities = [game.payoff_matrices[0], game.payoff_matrices[1]];

            self.screen.fill(BACKGROUND_COLOR);
            self.__plot_matchup__(utilities, resources, prev_action);

            pygame.display.flip();

            pygame.time.Clock().tick(fps);
            update_game_timer -= 1/fps;

            if update_game_timer <= 0:
                (game, resources) = village_game.get_round();
                prev_action = village_game.run(game);
                update_game_timer = game_tick;

    def __plot_matchup__(self, utilities: list[np.ndarray], resources: np.ndarray, action: list[np.ndarray]):

        board0_corner = np.array([128,128]);
        board1_corner = np.array([square_spacing*6 + 128,128]);

        self.__draw_board__(board0_corner, utilities[0], action);
        self.__draw_board__(board1_corner, utilities[1], action);
    

        #draw player resources
        number_text = self.font.render('Resources: '+str(resources[0]), True, (0, 0, 0));
        number_rect = number_text.get_rect(center=board0_corner + np.array([64, -64]));
        self.screen.blit(number_text, number_rect);
    
        number_text = self.font.render('Resources: '+str(resources[1]), True, (0, 0, 0));
        number_rect = number_text.get_rect(center=board1_corner + np.array([64, -64]));
        self.screen.blit(number_text, number_rect);
    

        #draw action names

        # player 1
        #columns
        action_text = self.font.render(('Harvest'), True, HARVEST_COLOR);
        action_rect = action_text.get_rect(center=board0_corner + np.array([40, -24]));
        self.screen.blit(action_text, action_rect);
    
        action_text = self.font.render(('Raid'), True, RAID_COLOR);
        action_rect = action_text.get_rect(center=board0_corner + np.array([40 + square_spacing, -24]));
        self.screen.blit(action_text, action_rect);

        action_text = self.font.render(('Trade'), True, TRADE_COLOR);
        action_rect = action_text.get_rect(center=board0_corner + np.array([40 + square_spacing*2, -24]));
        self.screen.blit(action_text, action_rect);
    
        #rows
        action_text = self.font.render(('Harvest'), True, HARVEST_COLOR);
        action_rect = action_text.get_rect(center=board0_corner + np.array([-64, square_spacing/2]));
        self.screen.blit(action_text, action_rect);
    
        action_text = self.font.render(('Raid'), True, RAID_COLOR);
        action_rect = action_text.get_rect(center=board0_corner + np.array([-64, square_spacing/2 + square_spacing]));
        self.screen.blit(action_text, action_rect);

        action_text = self.font.render(('Trade'), True, TRADE_COLOR);
        action_rect = action_text.get_rect(center=board0_corner + np.array([-64, square_spacing/2 + square_spacing*2]));
        self.screen.blit(action_text, action_rect);

        # player 2
        #columns
        action_text = self.font.render(('Harvest'), True, HARVEST_COLOR);
        action_rect = action_text.get_rect(center=board1_corner + np.array([40, -24]));
        self.screen.blit(action_text, action_rect);
    
        action_text = self.font.render(('Raid'), True, RAID_COLOR);
        action_rect = action_text.get_rect(center=board1_corner + np.array([40 + square_spacing, -24]));
        self.screen.blit(action_text, action_rect);

        action_text = self.font.render(('Trade'), True, TRADE_COLOR);
        action_rect = action_text.get_rect(center=board1_corner + np.array([40 + square_spacing*2, -24]));
        self.screen.blit(action_text, action_rect);
    
        #rows
        action_text = self.font.render(('Harvest'), True, HARVEST_COLOR);
        action_rect = action_text.get_rect(center=board1_corner + np.array([-64, square_spacing/2]));
        self.screen.blit(action_text, action_rect);
    
        action_text = self.font.render(('Raid'), True, RAID_COLOR);
        action_rect = action_text.get_rect(center=board1_corner + np.array([-64, square_spacing/2 + square_spacing]));
        self.screen.blit(action_text, action_rect);

        action_text = self.font.render(('Trade'), True, TRADE_COLOR);
        action_rect = action_text.get_rect(center=board1_corner + np.array([-64, square_spacing/2 + square_spacing*2]));
        self.screen.blit(action_text, action_rect);


    def __draw_board__(self, origin: np.ndarray, utilities: np.ndarray, action: list[np.ndarray]):
        for i in range(3):
            for j in range(3):
                
                color = BOARD_COLOR;

                rect = pygame.draw.rect(self.screen, color, (origin[0]+square_spacing*i, origin[1]+square_spacing*j, square_size, square_size));

                rect_corner = np.array([origin[0]+square_spacing*i, origin[1]+square_spacing*j]);

                triangle1 = [
                    (rect_corner[0], rect_corner[1]),
                    (rect_corner[0], rect_corner[1] + square_size),
                    (rect_corner[0] + square_size, rect_corner[1] + square_size),
                ]
                triangle2 = [
                    (rect_corner[0], rect_corner[1]),
                    (rect_corner[0] + square_size, rect_corner[1]),
                    (rect_corner[0] + square_size, rect_corner[1] + square_size),
                ]

                # Draw actions
                color1 = (0,0,0);
                color2 = (0,0,0);
                if action[0] == 0:
                    color1 = HARVEST_COLOR;
                if action[0] == 1:
                    color1 = RAID_COLOR;
                if action[0] == 2:
                    color1 = TRADE_COLOR;

                if action[1] == 0:
                    color2 = HARVEST_COLOR;
                if action[1] == 1:
                    color2 = RAID_COLOR;
                if action[1] == 2:
                    color2 = TRADE_COLOR;

                if j == action[0] and i == action[1]:
                    pygame.draw.polygon(self.screen, color1, triangle1)
                    pygame.draw.polygon(self.screen, color2, triangle2)

                number_text = self.font.render(str(utilities[j,i]), True, (0, 0, 0));
                number_rect = number_text.get_rect(center=rect.center);
                self.screen.blit(number_text, number_rect);

if __name__ == "__main__":
    game = GameRunner();
    game.run();
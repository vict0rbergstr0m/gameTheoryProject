import pygame
import sys
import numpy as np
from game import *

BACKGROUND_COLOR = (3,15,19);
BOARD_COLOR = (79,109,122);


RAID_COLOR = (144,50,61);
HARVEST_COLOR = (194,128,52);
TRADE_COLOR = (217,202,179);
NASH_COLOR = (0, 160, 30);
square_size = 84;
square_spacing = 96;

font_size = 32

game_tick = 0.1;
fps = 60;


class GameAnalyzer:
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
        right_arrow_pressed = False;
        active_input = False;
        input_string = '';
        input_font = pygame.font.Font(None, font_size);
        text_color = (255, 255, 255);
        input_rect = pygame.Rect(10, self.HEIGHT - 40, 140, 32);
        player_index = 0;
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();

            # Check for keydown events
                if event.type == pygame.KEYDOWN and not active_input:
                # Check if the right arrow key is pressed
                    if event.key == pygame.K_RIGHT:
                        right_arrow_pressed = True
                    # Check if the '1' key is pressed
                    elif event.key == pygame.K_1:
                        # Ask the user for a new value to set for resources[0]
                        #new_resource_value = int(input("Enter the new value for resources[0]: "))
                        #village_game.resources[0] = new_resource_value
                        active_input = not active_input
                        player_index = 0;
                    elif event.key == pygame.K_2:
                        # Ask the user for a new value to set for resources[0]
                        #new_resource_value = int(input("Enter the new value for resources[0]: "))
                        #village_game.resources[0] = new_resource_value
                        active_input = not active_input;
                        player_index = 1;    
                

                # Handle text input events
                if event.type == pygame.KEYDOWN and active_input:
                    if event.key == pygame.K_RETURN:
                        try:
                            # Update resources[0] with the entered value
                            village_game.resources[player_index] = int(input_string)
                        except ValueError:
                            pass  # Handle invalid input (non-integer)
                        active_input = False
                        self.screen.fill(BACKGROUND_COLOR);
                        utilities = [game.payoff_matrices[0], game.payoff_matrices[1]];
                        self.__plot_matchup__(utilities, resources, prev_action);

                        input_string = ''
                    elif event.key == pygame.K_BACKSPACE:
                        input_string = input_string[:-1]
                        pygame.draw.rect(self.screen, (150+player_index*100, 150, 150), input_rect)
                        text_surface = self.font.render(input_string, True, text_color)
                        self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
                    else:
                        input_string += event.unicode
                        pygame.draw.rect(self.screen, (150+player_index*100, 150, 150), input_rect)
                        text_surface = self.font.render(input_string, True, text_color)
                        self.screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
                                # Check for keyup events
                    pygame.display.flip();
                    
                if event.type == pygame.KEYUP:
                    # Check if the right arrow key is released
                    if event.key == pygame.K_RIGHT:
                        right_arrow_pressed = False
                        
                        
                        
            if right_arrow_pressed:
                    
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
        number_text = self.font.render('Resources: '+str(resources[0]), True, (255, 255, 255));
        number_rect = number_text.get_rect(center=board0_corner + np.array([64, -64]));
        self.screen.blit(number_text, number_rect);
    
        number_text = self.font.render('Resources: '+str(resources[1]), True, (255, 255, 255));
        number_rect = number_text.get_rect(center=board1_corner + np.array([64, -64]));
        self.screen.blit(number_text, number_rect);
    
        #Draw Nash
        
        game = nash.Game(utilities[0],utilities[1])
        print(game)
        equilibria = game.support_enumeration();
        for count,eq in enumerate(equilibria):
            print(eq)
            if any(eq[0]==1): # type: ignore
                i = eq[0].tolist().index(1); # type: ignore
                j = eq[1].tolist().index(1); # type: ignore
                circ_pos1= (board0_corner[0]+square_size/2 + square_spacing*(i), board0_corner[1]+square_size/2+square_spacing*(j));
                pygame.draw.circle(self.screen, NASH_COLOR,circ_pos1,square_size*2/(3*np.sqrt(2)),4)
                circ_pos2= (board1_corner[0]+square_size/2 + square_spacing*(i), board1_corner[1]+square_size/2+square_spacing*(j));
                pygame.draw.circle(self.screen, NASH_COLOR,circ_pos2,square_size*2/(3*np.sqrt(2)),4)
                eq_text = self.font.render('Nash: ' + str(eq),True,(255, 255, 255));
                eq_rect = eq_text.get_rect(center=board0_corner+square_spacing*7/2+np.array([0, 30])*count);
                self.screen.blit(eq_text, eq_rect);
            else:
                eq_text = self.font.render('Nash: ' + str(eq),True,(255, 255, 255));
                eq_rect = eq_text.get_rect(center=board0_corner+square_spacing*7/2+np.array([0, 30])*count);
                self.screen.blit(eq_text, eq_rect);

        
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
    game = GameAnalyzer();
    game.run();
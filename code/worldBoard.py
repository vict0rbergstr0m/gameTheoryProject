import numpy as np
import pygame
import sys
from strategies import *

BACKGROUND_COLOR = (3,15,19);
PLAYER_COLOR = (79,109,122);


RAID_COLOR = (144,50,61);
HARVEST_COLOR = (194,128,52);
TRADE_COLOR = (217,202,179);

font_size = 32

game_tick = 0.1;
fps = 60;

class Player:
    def __init__(self, color, resources, position, strategy) -> None:
        self.color = color
        self.resources = resources
        self.position = position
        self.strategy = strategy

class WorldGame:
    """
    keep track of all players, their resources, and locations.
    """
    def __init__(self, n_players, min_resources, max_resources) -> None:
        pygame.init();

        self.WIDTH, self.HEIGHT = 1280, 720;

        # Create the Pygame screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT));
        pygame.display.set_caption("Village Game");
    
        self.font = pygame.font.Font(None, font_size);
    
        self.players = [];
        for i in range(n_players):
            position = (np.random.randint(0, self.WIDTH), np.random.randint(0, self.HEIGHT));
            self.players.append(Player(PLAYER_COLOR, np.random.randint(min_resources, max_resources), position, NashStrategy()));

    def run(self):
        update_game_timer = game_tick;
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit();

            self.screen.fill(BACKGROUND_COLOR);
            self.__draw_players__(self.players);

            pygame.display.flip();

            pygame.time.Clock().tick(fps);
            update_game_timer -= 1/fps;

            if update_game_timer <= 0:



                update_game_timer = game_tick;

    def __draw_players__(self, players: list[Player]):
        for player in players:
            self.__draw_player__(player)


    def __draw_player__(self, player: Player):
        pygame.draw.circle(self.screen, player.color, (player.position[0], player.position[1]), np.sqrt(player.resources)/2);

if __name__ == "__main__":
    game = WorldGame(50, 250, 1000);
    game.run()
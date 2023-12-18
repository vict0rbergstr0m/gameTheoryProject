import numpy as np
import pygame
import sys
from strategies import *
from game import *

harvest_factor = 0.4;
raid_factor = 0.8;
max_raid_value = 2;
raid_cost = 0.2;
trade_factor = 0.6;

BACKGROUND_COLOR = (6,30,38);
PLAYER_COLOR = (79,109,122);

RAID_COLOR = (144,50,61);
HARVEST_COLOR = (194,128,52);
TRADE_COLOR = (217,202,179);

dead_value = 5;

font_size = 16

game_tick = 0.1;
fps = 60;

class Player:
    def __init__(self, color, resources, position: tuple[float,float], strategy) -> None:
        self.color = color;
        self.resources = resources;
        self.position = position;
        self.strategy = strategy;
        self.neighbors = [];
        self.dead = False;
        self.splits = 1;

    def dead_check(self) -> bool:
        if self.resources <= dead_value:
            self.dead = True;
            self.color = (0,0,0);
        return self.dead;

class WorldGame:
    """
    keep track of all players, their resources, and locations.
    """
    def __init__(self, n_players, min_resources, max_resources, always_neighbors_distance = 200, split_at_resources = 5000) -> None:
        self.always_neighbors_distance = always_neighbors_distance;

        pygame.init();

        self.WIDTH, self.HEIGHT = 1280, 720;

        # Create the Pygame screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT));
        pygame.display.set_caption("Village Game");
    
        self.font = pygame.font.Font(None, font_size);
    
        self.players: list[Player] = [];

        possible_strategies = [HarvestStrategy, RaidStrategy, TradeStrategy, NashStrategy, PacifistStrategy, GreedyStrategy];
        # possible_strategies = [HarvestStrategy, NashStrategy, PacifistStrategy];
        #possible_strategies = [HarvestStrategy];

        for i in range(n_players):
            position = (np.random.randint(0, self.WIDTH), np.random.randint(0, self.HEIGHT));
            strat = possible_strategies[np.random.randint(0, len(possible_strategies))];
            self.players.append(Player(PLAYER_COLOR, np.random.randint(min_resources, max_resources), position, strat()));
    
        self.__build_neighbors__(self.players);
        self.update_edges = False;
        self.split_at_resources = split_at_resources;

    def __build_neighbors__(self, players: list[Player]):
        """
        finds players closer than always_neighbors_distance and adds them as neighbors

        if no neighbors are found:
            finds the closest player to a player and adds them as neighbors
        """
        for player in players:
            player.neighbors = [];

        for player1 in players:
            if player1.dead:
                continue;

            closest_neighbor: tuple[float, Player] = (np.inf, players[0]);
            for player2 in players:
                if player1.position == player2.position or player1.neighbors.__contains__(player2) or player2.dead:
                    continue;

                if self.__get_distance__(player1, player2) <= self.always_neighbors_distance:
                    player1.neighbors.append(player2);
                    player2.neighbors.append(player1);
            
                if len(player1.neighbors) == 0:
                    dist = self.__get_distance__(player1, player2);
                    if dist < closest_neighbor[0]:
                        closest_neighbor = (dist, player2);

                
            if len(player1.neighbors) == 0:
                player1.neighbors.append(closest_neighbor[1]);
                closest_neighbor[1].neighbors.append(player1);
    
            for neighbor in player1.neighbors:#UGH WHY DOES IT KEEP ADDING ITSELF!???
                if neighbor.position == player1.position:
                    player1.neighbors.remove(neighbor);

    def __get_distance__(self, player1: Player, player2: Player):
        return np.sqrt((player1.position[0] - player2.position[0])**2 + (player1.position[1] - player2.position[1])**2)

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

                alive_count = 0;
                for player in self.players:
                    if not player.dead:
                        alive_count += 1;

                if alive_count <= 1:
                    update_game_timer = 99;
                    print("Game Over!");
                    # break;
                else:
                    #loop trough a list of players (sorted in order of resources descending)
                    self.players = sorted(self.players, key=lambda player: player.resources, reverse=True);
                    #the players will each get one turn to play a round against (one or all) neighbors?
                    for player in self.players:
                        if player.dead_check():
                            continue;

                        #set up a single round game
                        player.neighbors = sorted(player.neighbors, key=lambda neighbor: neighbor.resources, reverse=True);
                        opponent = player.neighbors[np.random.randint(0, len(player.neighbors))];
                        if opponent.dead:
                            for neighbor in player.neighbors:
                                if not neighbor.dead:
                                    opponent = neighbor;
                                    break;

                        game = Game(harvest_factor, raid_factor, max_raid_value, raid_cost, trade_factor, player.resources, opponent.resources, [player.strategy, opponent.strategy]);
                        (game_round, _) = game.get_round();
                        actions = game.run(game_round);

                        player.resources = game.resources[0];
                        opponent.resources = game.resources[1];

                        self.__set_color_from_action__(player, actions[0]);
                        self.__set_color_from_action__(opponent, actions[1]);

                        if player.dead_check() or opponent.dead_check():
                            self.update_edges = True;
                
                        if self.split_at_resources > 0 and player.resources >= self.split_at_resources and player.splits > 0:#spawn new player if resources are high enough
                            random_offset = (np.random.randint(-100, 100), np.random.randint(-100, 100));
                            pos = (player.position[0] + random_offset[0], player.position[1] + random_offset[1]);
                            player.resources *= 0.125; #reduce resources to 12.5% as cost for splitting
                            self.players.append(Player(player.color, player.resources, pos, player.strategy)); #spawn new player and add to player list
                            self.__build_neighbors__(self.players); #rebuild neighbors
                            self.update_edges = True;
                            player.splits -= 1; #update slipt count for player


                if self.update_edges:
                    self.__build_neighbors__(self.players);
                update_game_timer = game_tick;

    def __set_color_from_action__(self, player: Player, action: np.ndarray):
        if action == 0:
            player.color = HARVEST_COLOR
        elif action == 1:
            player.color = RAID_COLOR
        elif action == 2:
            player.color = TRADE_COLOR

    def __draw_players__(self, players: list[Player]):
        for player in players:
            self.__draw_paths__(player)

        for player in players:
            self.__draw_player__(player)

    def __draw_player__(self, player: Player):
        size = player.resources/(10000+player.resources)*50 + 4;
        pygame.draw.circle(self.screen, player.color, (player.position[0], player.position[1]), size);
        text_color = (255,255,255);
        if player.dead:
            text_color = (0,0,0);

        text = self.font.render(player.strategy.__class__.__name__, True, text_color); # Render the text
        text_rect = text.get_rect(center=(player.position[0], player.position[1] - 20));  # Set the position of the text
        self.screen.blit(text, text_rect);  # Draw the text on the screen

    def __draw_paths__(self, player: Player):
        start_pos = player.position;
        for neighbor in player.neighbors:
            end_pos = neighbor.position;
            pygame.draw.line(self.screen, TRADE_COLOR, start_pos, end_pos, 5);

if __name__ == "__main__":
    game = WorldGame(10, 250, 1000, 200, 50000);
    game.run()
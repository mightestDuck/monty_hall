import numpy as np
import random


class Player:
    def __init__(self, strategy):
        self.strategy = strategy

    def choose(self, init_choice: int, host_choice: int, doors: np.array) -> int:
        if self.strategy == 'donkey':
            return init_choice
        elif self.strategy == 'switcher':
            options = [n for n in range(len(doors)) if n != host_choice and n != init_choice]
            return options[random.randint(0, len(options) - 1)]


class Host:
    def __init__(self, strategy):
        self.strategy = strategy

    def choose(self, player_choice: int, doors: np.array) -> int:
        options = []
        if self.strategy == 'random':
            options = [n for n in range(len(doors)) if n != player_choice]
        elif self.strategy == 'knows-it-all':
            options = [n for n in range(len(doors)) if n != player_choice and doors[n] == 0]
        return options[random.randint(0, len(options) - 1)]


def play_game(player: Player, host: Host, n_doors: int, k_rewards: int) -> int:
    doors = np.zeros(n_doors)
    lucky_doors = random.sample(range(n_doors), k_rewards)
    for door in lucky_doors:
        doors[door] = 1

    init_choice = random.randint(0, n_doors - 1)
    host_choice = host.choose(init_choice, doors)
    player_choice = player.choose(init_choice, host_choice, doors)
    return doors[player_choice]


if __name__ == '__main__':
    i_GAMES = 100000
    n_DOORS = 3
    k_REWARDS = 1

    players = [Player(strategy='donkey'), Player(strategy='switcher')]
    hosts = [Host(strategy='knows-it-all'), Host(strategy='random')]
    for player in players:
        for host in hosts:
            successes = 0
            for _ in range(i_GAMES):
                successes += play_game(player, host, n_DOORS, k_REWARDS)
            print(f'player={player.strategy:<10} host={host.strategy:<13} wins={100 * successes/i_GAMES:.2f}%')

import numpy as np

from game import Action
from game import Game


class LearningEnvironment(object):
    def __init__(self):
        self.game = Game(select_random_snake_and_food_positions=True)
        self.steps_without_scoring = 0

    def reset(self):
        self.game = Game(select_random_snake_and_food_positions=True)
        self.steps_without_scoring = 0
        return self.build_observation(self.game)

    def step(self, action):
        score_before = self.game.get_score()
        self.game.make_action(action)
        score_after = self.game.get_score()

        observation = self.build_observation(self.game)
        reward = score_after - score_before
        done = self.game.is_finished()

        if reward == 0:
            self.steps_without_scoring += 1
        else:
            self.steps_without_scoring = 0

        if self.steps_without_scoring == 300:
            done = True

        return (observation, reward, done)

    def cur_obs(self):
        return self.build_observation(self.game)

    def build_observation(self, g):
        observation = np.zeros((Game.HEIGHT + 2, Game.WIDTH + 2, 2))

        # border
        for i in range(Game.HEIGHT+2):
            observation[i, 0, 0] = 1.0
            observation[i, Game.WIDTH + 1, 0] = 1.0
        for i in range(Game.WIDTH+2):
            observation[0, i, 0] = 1.0
            observation[Game.HEIGHT + 1, i, 0] = 1.0

        # snake's head
        observation[g.snake[0][0]+1, g.snake[0][1]+1, 1] = 1.0
        # snake's tail
        for (r, c) in g.snake[1:]:
            observation[r+1, c+1, 0] = 1.0

        # food
        observation[g.food_at[0]+1, g.food_at[1]+1, 0] = -1.0

        return observation

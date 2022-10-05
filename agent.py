from snake_game import SnakeGame
import numpy as np
from action import Action
from existance import Existance

class Agent:
    def __init__(self, alpha = 0.95, gamma = 0.9, animate_learning = False):

        self.animate_learning = animate_learning
        self.game = SnakeGame(animate = self.animate_learning)
        self.alpha = alpha
        self.gamma = gamma
        # first question: what are states for our agent and what shall we put in q table:
        # 1. are there any obstacles (including own body) in front, 
        # if turn right or if turn left: so three states with 2 possible values (2, 2, 2)
        # 2. distance to food increases/decreases (2)
        # 3. food left, right, above, below head (2, 2, 2, 2)
        # 4. actions: turn right, turn left, go forward (3)

        self.obstacles_infront = np.array([0, 1]) # 0 if dont exis, 1 if does
        self.obstacles_left = np.array([0, 1]) # 0 if dont exis, 1 if does
        self.obstacles_right = np.array([0, 1]) # 0 if dont exis, 1 if does
        self.dist_to_food = np.array([0, 1])  # 0 if decrreses, 1 if increases
        self.food_left = np.array([0, 1]) # 0 if is left, 1 if isn't
        self.food_right = np.array([0, 1]) # 0 if is left, 1 if isn't
        self.food_above = np.array([0, 1]) # 0 if is left, 1 if isn't
        self.food_below = np.array([0, 1]) # 0 if is left, 1 if isn't
        self.actions = np.array([Action.RIGHT, Action.LEFT, Action.FORWARD])
        self.q_table = np.zeros(shape = (2, 2, 2, 2, 2, 2, 2, 2, 3))
        
    def get_action(self, epsilon, optimal_action):
        """ Chooses an action according to epsilon greedy policy.

        Args:
            epsilon (float): Probability that random action is choosen
            optimal_action (int): Optimal action

        Returns:
            action, action_ind: Action agent is taking and it's index.
        """
        c = np.random.choice([0, 1], p = [epsilon, 1 - epsilon])

        if c == 0:
            action_ind = np.random.choice(range(len(self.actions))) # choose random action
        else:
            action_ind = optimal_action

        action = self.actions[action_ind] 
        return action, action_ind

    def play_episode(self, epsilon):
        self.game = SnakeGame(animate = self.animate_learning)
        game_over = False
        while not game_over:
            obs_infront, obs_left, obs_right, dist_to_food, food_left, food_right, food_above, food_below = self.game.get_states()
            optimal_action = int(np.argmax(self.q_table[obs_infront, obs_left, obs_right, dist_to_food, food_left, food_right, food_above, food_below, :]))

            action, action_ind = self.get_action(epsilon, optimal_action)
            
            game_over = self.game.play_step(action)  
            newobs_infront, newobs_left, newobs_right, newdist_to_food, newfood_left, newfood_right, newfood_above, newfood_below = self.game.get_states()

            reward = self.game.get_reward()

            self.q_table += self.alpha*(
                    reward + self.gamma * max(self.q_table[newobs_infront, newobs_left, newobs_right, newdist_to_food, newfood_left, newfood_right, newfood_above, newfood_below , :]) - 
                    self.q_table[obs_infront, obs_left, obs_right, dist_to_food, food_left, food_right, food_above, food_below, action_ind])

    def learn(self, num_of_episodes = 200, epsilon_start = 0.25, epsilon_stop = 0.01):
        epsilon_step = (epsilon_start - epsilon_stop)/num_of_episodes
        epsilon = epsilon_start
        for episode in range(1, num_of_episodes):

            self.play_episode(epsilon = epsilon)
            epsilon -= epsilon_step
            if episode % 100 == 0:
                print(f"Episode {episode} finished.")


    def control(self):
        game = SnakeGame(animate = True)
        game_over = False
        while not game_over:

            obs_infront, obs_left, obs_right, dist_to_food, food_left, food_right, food_above, food_below = game.get_states()
            optimal_action = int(np.argmax(self.q_table[obs_infront, obs_left, obs_right, dist_to_food, food_left, food_right, food_above, food_below, :]))
            
            game_over = game.play_step(self.actions[optimal_action])  



    
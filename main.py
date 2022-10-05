from agent import Agent



if __name__ == '__main__':
    a = Agent()

    a.learn(num_of_episodes=1200, epsilon_start=0.5, epsilon_stop=0.1)
    a.control()

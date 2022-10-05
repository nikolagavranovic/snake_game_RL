from agent import Agent



if __name__ == '__main__':
    a = Agent()

    a.learn(num_of_episodes=5000, epsilon_start=0.8, epsilon_stop=0.1)
    a.control()
    a.control()

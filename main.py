from agent import Agent



if __name__ == '__main__':
    a = Agent()

    # learning from zero
    # a.learn(num_of_episodes=50000, epsilon_start=0.8, epsilon_stop=0.1)
    # a.save_agent_params()

    # loading existing model and controling snake
    a.load_agent_params()
    a.control()

    # loading existing model and training
    # a.load_agent_params()
    # a.learn(num_of_episodes=10000, epsilon_start=0.8, epsilon_stop=0.1)
    # a.save_agent_params()
   

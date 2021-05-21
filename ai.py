import numpy as np


class Ai:
    def __init__(self):
        # Class to Ai, with training and decisions make

        # states is the number of sides in the Cartesian plane of the game.
        # This is directly the number of ways or positions the car can run on.
        self.states = 2
        self.actions = ['right', 'left']
        self.q_values = np.zeros((self.states, self.states, len(self.actions)))
        self.rewards = np.full((self.states, self.states), -100.)

        # define the start location, the start position on the matrix
        self.current_row_index = self.current_column_index = 0
        self.current_row_index = self.current_column_index = 0

        # define training parameters
        self.epsilon = 0.9  # the percentage of time when we should take the best action
        self.discount_factor = 0.9  # discount factor for future rewards
        self.learning_rate = 0.9  # the rate at which the AI agent should learn

    def set_rewards(self, left: None, right: None):
        # function that set the values for rewards matrix to hold the rewards for each state.
        self.rewards[0][0] = left
        self.rewards[0][1] = right

    def set_starting_location(self):
        # choose a random point to start the episode
        self.current_row_index = np.random.randint(self.states)
        self.current_column_index = np.random.randint(self.states)

    def get_next_action(self):
        # it's choose in an random way a value between 0 and 1 and make a comparison with the epsilon.
        # after that, it's choose the q_values for this state.
        if np.random.random() < self.epsilon:
            return np.argmax(self.q_values[self.current_row_index, self.current_column_index])
        else:
            # choose a random action
            return np.random.randint(2)

    def get_next_location(self, action_index):
        # method that get new row and colon based on the chosen action
        new_row_index = self.current_row_index
        new_column_index = self.current_column_index

        if self.actions[action_index] == 'right' and self.current_column_index < self.states - 1:
            new_column_index += 1
        elif self.actions[action_index] == 'left' and self.current_column_index > 0:
            new_column_index -= 1
        return new_row_index, new_column_index

    def get_shortest_path(self, start_row_index, start_column_index):
        #  That method will get the shortest path between any location and the place with the best reward

        self.current_row_index, self.current_column_index = start_row_index, start_column_index
        shortest_path = [[self.current_row_index, self.current_column_index]]

        # get best action
        self.epsilon = 1.
        action_index = self.get_next_action()

        # update the location and add to list
        current_row_index, current_column_index = self.get_next_location(action_index)
        shortest_path.append([current_row_index, current_column_index])
        return shortest_path

    def training(self, log=False):

        # run in 1000 episodes
        for episode in range(1000):
            # get the starting location for this episode
            self.set_starting_location()

            # choose which action to take
            self.epsilon = 0.9
            action_index = self.get_next_action()

            # do the index transition
            old_row_index, old_column_index = self.current_row_index, self.current_column_index
            row_index, column_index = self.get_next_location(action_index)

            # receive the reward for moving to the new state, and calculate the temporal difference
            reward = self.rewards[row_index, column_index]
            # print(old_row_index, old_column_index, action_index)
            old_q_value = self.q_values[old_row_index, old_column_index, action_index]
            temporal_difference = reward + (self.discount_factor * np.max(self.q_values[row_index,
                                                                                        column_index])) - old_q_value

            # update the Q-value for the previous state and action pair
            new_q_value = old_q_value + (self.learning_rate * temporal_difference)
            self.q_values[old_row_index, old_column_index, action_index] = new_q_value
        if log:
            print("training completed")


# aa = Ai()
# lst = [8, 6]
# aa.set_rewards(lst[0], lst[1])
# aa.training()
# print(aa.get_shortest_path(0, 0)[1][1])



from typing import Tuple
import numpy as np
import time

import os


import numpy as np


class RobotPolicy(object):

    def __init__(self, N_rows = 20, N_cols = 20, max_episodes_steps = 1000):
        self.N_rows = N_rows
        self.N_cols = N_cols
        self.num_states = N_rows * N_cols
        self.gamma = 0.99
        self.max_episodes_steps = max_episodes_steps
        self.actions = {
                0: (-1, 0),  # left
                1: (1, 0),   # right
                2: (0, 1),   # up
                3: (0, -1),  # down
                4: (0, 0)    # stay
            }
        self.num_actions = 5


    def reward_function(self, cube_center, i, j, sigma = .1, action = None):

        # we first need to define a function whihc translates the coordinates (i, j) into coordinates (x, y), assuming that they are equidistant and in the range [0, 1]
        def _coord_to_xy(i, j):
            x = i / (self.N_rows - 1)
            y = j / (self.N_cols - 1)
            return x, y
        x_point, y_point = _coord_to_xy(i, j)

        # 2D Gaussian formula
        gaussian = np.exp(-((x_point - cube_center[0])**2 + (y_point - cube_center[1])**2) / (2 * sigma**2))

        # Normalize so the sum is 1 (optional, depends on use case)
        # gaussian /= np.sum(gaussian)


        return gaussian

    def coord_to_state(self, i, j):
        return i * self.N_cols + j

    def state_to_coord(self, index): 
        return divmod(index, self.N_cols)

    def cube_center_to_coord(self):
        # convert the cube center to coordinates (i, j)
        i = self.cube_center[0] * (self.N_rows - 1)
        j = self.cube_center[1] * (self.N_cols - 1)
        return i, j

    def compute_transition_probabilities(self):
    # Costruzione della matrice
        P = np.zeros((self.num_states, self.num_states, self.num_actions), dtype=np.float32)

        for s in range(self.num_states):
            r, c = self.state_to_coord(s)
            for a in range(self.num_actions):
                dr, dc = self.actions[a]
                new_r, new_c = r + dr, c + dc

                # Se nuova posizione è valida, aggiorna lo stato
                if 0 <= new_r < self.N_rows and 0 <= new_c < self.N_cols:
                    s_prime = self.coord_to_state(new_r, new_c)
                else:
                    s_prime = s  # rimane nello stesso stato

                P[s, s_prime, a] = 1.0

        return P


    def compute_optimal_solution(self, cube_center: Tuple[float, float]) -> np.ndarray:
        # definition of the transition matrixes
        # transition probabilities when the action selected is a=0
        P = self.compute_transition_probabilities()
            

        # definition of the reward
        rew = np.zeros((self.num_states, ))
        
        beta = 1
        for i in range(self.N_rows):
            for j in range(self.N_cols):
                index=self.coord_to_state(i, j)
                rew[index] = self.reward_function(cube_center, i, j, action=0)
                

        # value iteration algorithm
        mu_=np.zeros((self.num_states, ))                  
        v_estimate= np.zeros((self.num_states, ))
        old_v_estimate = np.zeros((self.num_states, ))

        if self.gamma > 0:
            epsilon = 1*(1-self.gamma)/(2*self.gamma)
        else: 
            epsilon = 0.1
        diff = 0
        n_iterations = 1000
        for n_iter in range(n_iterations):  
            for i in range(self.N_rows):
                for j in range(self.N_cols):
                    index = self.coord_to_state(i, j)
                    future_values = [rew[index] + self.gamma * np.dot(P[index,:, action], old_v_estimate) for action in range(self.num_actions)]
                    # future_values =  [ rew[index] + self.gamma * np.dot(P[index,:, 0], old_v_estimate),  rew[index] + self.gamma * np.dot(P[index,:, 1], old_v_estimate), rew[index] + self.gamma * np.dot(P[index,:, 2], old_v_estimate), rew[index] + self.gamma * np.dot(P[index,:, 3], old_v_estimate)]     
                    v_estimate[index] = max(future_values)
                    mu_[index] = np.argmax(future_values)
            diff = max(abs(v_estimate - old_v_estimate))
            if diff < epsilon:
                break
            for index in range(self.num_states):
                old_v_estimate[index] = v_estimate[index]

        # generate the solution in an easier format to plot 
        policy=np.zeros((self.N_rows, self.N_cols), dtype=int)
        for i in range(self.N_rows):
            for j in range(self.N_cols):
                index=self.coord_to_state(i,j)
                policy[i,j] = mu_[index]

        value_function = np.zeros((self.N_rows, self.N_cols))
        for i in range(self.N_rows):
            for j in range(self.N_cols):
                index = self.coord_to_state(i, j)
                value_function[i, j] = v_estimate[index]
        
        return policy, self.actions
                


import torch
import random
import numpy as np
from collections import deque
from model import Linear_QNet, QTrainer
from game import Game
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(9, 256, 9)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, board):
        matrix = np.array(board)
        state = matrix.flatten()
        for idx in range(9):
            if state[idx]=='x':
                state[idx]=1
            elif state[idx]=='o':
                state[idx]=2
            elif state[idx]=='':
                state[idx]=0
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def possible_moves(self,state):
        poss=[]
        for idx in range(9):
            if state[idx]==0:
                poss.append(idx)
        return poss

    def get_action(self,state):
        # random moves: tradeoff exploration / exploitation
        poss=self.possible_moves(state)
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0,0,0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            print('Random Action')
            move = random.choice(poss)
            final_move[move] = 1
        else:
            print('Torch Action')
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            #TODO fix the torch action on the board , it makes illegal moves
        return final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game=Game(1)
    print('entry to agent')
    while True:
        game.checkExit()
        game.render()
        a,b,c=game.play_step(game.get_action(game.game_state()),'x',game.agent_turn)
        game.CheckWin()
        # get old state
        state_old = agent.get_state(game.board)
        # get move
        if game.start==True:
            final_move = agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = game.play_step(final_move,'o',game.ai_turn)
            state_new = agent.get_state(game.board)

            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

        game.CheckWin()
        game.Refresh()

        if game.start==False:
            # train long memory, plot result
            game.reset()
            if done:
                agent.n_games += 1
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)

if __name__ == '__main__':
    train()
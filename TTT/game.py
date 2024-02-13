import pygame
from tile import Tile
from TAI import TAI
import time
import numpy as np
import random

class Game:
    def __init__(self,player) :
        pygame.init()
        self.player_turn=player
        self.agent_turn=player
        self.ai_turn=(player-1)**2
        self.start=True
        self.turn=1
        self.entry=0
        self.glscore=0
        self.ai=TAI(self.ai_turn)
        self.size=600
        self.board = [	['', '', ''],
                    ['', '', ''],
                    ['', '', '']
                ]
        self.x=pygame.transform.scale(pygame.image.load('./piece/x.png'), (190, 190))
        self.o=pygame.transform.scale(pygame.image.load('./piece/o.png'), (190, 190))
        self.restart=Tile(240,440 , 100, 50)
        self.font = pygame.font.Font(None, 36)
        self.tiles_list=self.g_tiles(self.board)
        self.clock=pygame.time.Clock()
        window_size = (self.size, self.size)
        self.screen = pygame.display.set_mode(window_size)
        pygame.display.set_caption("Tic-Tac-Toe")
        for tile in self.tiles_list:
            tile.state=False
        #---------------------game start------------------------#
        while True:	
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        #new_value(results)
                        pygame.quit()
                        exit()
            if self.start:
                # if self.ai_action():
                #     self.turn=(self.turn-1)**2
                if self.player_action() and self.start==True:
                    self.turn=self.ai_turn
                    print(self.turn)
                if self.winner()=='x':
                    self.start=self.win('the winner is X')
                    ending='x'
                    save=True
                if self.winner()=='o':
                    self.start=self.win('the winner is O')
                    ending='o'
                    save=True
                if self.winner()=='draw':
                    self.start=self.win('Its a Draw')
                    ending='draw'
                    save=True
                if self.ai_turn==self.turn and self.start==True:
                    if self.ai_turn==0:
                        a,b,c=self.play_step(self.get_action(self.game_state()),'x',self.agent_turn)
                    else:
                        a,b,c=self.play_step(self.get_action(self.game_state()),'o',self.agent_turn)
            else:
                if save==True:
                    #results.append((board,ending))
                    #print(entry)
                    save=False
                #if pygame.mouse.get_pressed()[0]:
                self.reset()
                self.start=True
                time.sleep(0.3)
                for tile in self.tiles_list:
                    tile.state=False
                self.screen.fill((0,0,0))
                
            pygame.display.update()
            self.clock.tick(30)
    def checkExit(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #new_value(results)
                    pygame.quit()
                    exit()

    def Refresh(self):
        pygame.display.update()
        self.clock.tick(30)

    def g_tiles(self,config):
        output = []
        row=len(config)
        column=len(config[0])
        for x in range(row):
            for y in range(column):
                output.append(
                    Tile(x,  y, self.size/3 , self.size/3)
                    )
        return output

    def CheckWin(self):
        if self.winner()=='x':
            self.start=self.win('the winner is X')
        if self.winner()=='o':
            self.start=self.win('the winner is O')
        if self.winner()=='draw':
            self.start=self.win('Its a Draw')
    
    def winner(self):
        count=0
        if self.board[0][0] == self.board[1][1] and self.board[0][0] == self.board[2][2]and self.board[0][0] != '':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] and self.board[0][2] == self.board[2][0]and self.board[0][2] != '':
            return self.board[0][2] 
        for i in range(3):
            if self.board[i][0]==self.board[i][1] and self.board[i][2]==self.board[i][1] and self.board[i][0] != '':
                return self.board[i][0]
            if self.board[0][i]==self.board[1][i] and self.board[2][i]==self.board[1][i]and self.board[0][i] != '':
                return self.board[0][i]
            for j in range(3):
                if self.board[i][j]!='':
                    count=count+1
        if count==9:
            return 'draw'   
    
    def win(self,mark):
        pygame.draw.rect(self.screen, 'white', (0,0 , self.size, self.size))
        text_surface = self.font.render(mark, True, 'black')
        self.screen.blit(text_surface, (200, 250))
        self.restart.simdraw(self.screen)
        res = self.font.render('click anywhere to restart', True, 'black')
        self.screen.blit(res, (150, 450))
        return False
    #--------------agent functions to work with-------------#
    def game_state(self):
        matrix = np.array(self.board)
        state = matrix.flatten()
        for idx in range(9):
            if state[idx]=='x':
                state[idx]=2
            elif state[idx]=='o':
                state[idx]=1
            elif state[idx]=='':
                state[idx]=0
        return np.array(state, dtype=int)

    def possible_moves(self,state):
        poss=[]
        for idx in range(9):
            if state[idx]==0:
                poss.append(idx)
        return poss
        
    def get_action(self,state):
        final_move = [0,0,0,0,0,0,0,0,0]
        poss=self.possible_moves(state)
        if len(poss)!= 0:
            move=random.choice(poss)
            final_move[move] = 1
        return final_move

    def play_step(self,action,pick,next_turn):
        for idx in range(9):
            if action[idx]==1:
                pos=idx
        x=int(pos/3)
        y=pos-3*x
        self.board[x][y]=pick
        self.turn=next_turn
        self.tiles_list[pos].state=True
        self.tiles_list[pos].draw(self.screen,self.x,self.o,self.board[x][y])
        time.sleep(0.1)
        return self.evaluate()

    def evaluate(self):
        reward=0
        done=False
        score=self.glscore
        if self.winner()=='x':
            reward=-10
            done=True
            score =reward + self.glscore
        if self.winner()=='o':
            reward=10
            done=False
            score =reward + self.glscore
        if self.winner()=='draw':
            reward=-5
            done=False
            score =reward + self.glscore
        return reward,done,score

    def reset(self):
        self.board , self.turn , self.glscore
        a,done,score=self.evaluate()
        self.board = [	['', '', ''],
                ['', '', ''],
                ['', '', '']
                ]
        self.turn=1
        print('the current score is : '+str(score))
        self.glscore=score
        if done==True:
            print('the finale score is : '+str(score))
            self.glscore=0
        for tile in self.tiles_list:
            tile.state=False
        time.sleep(0.5)
        self.screen.fill((0,0,0))
        self.start=True
    
    def render(self):
        for tile in self.tiles_list:
            tile.draw(self.screen,self.x,self.o,self.board[tile.x][tile.y])
    #------------player and bot actions and turns-------------# 

    def player_action(self):
        for tile in self.tiles_list:
            tile.draw(self.screen,self.x,self.o,self.board[tile.x][tile.y])
            if self.player_turn==self.turn:
                if tile.det_click() and tile.state==False:
                    if self.player_turn==0 and tile.state==False:
                        self.board[tile.x][tile.y]='x'
                    if self.player_turn==1 and tile.state==False:
                        self.board[tile.x][tile.y]='o'
                    tile.state=True
                    tile.draw(self.screen,self.x,self.o,self.board[tile.x][tile.y])
                    return True

    def ai_action(self):
        for tile in self.tiles_list:
            tile.draw(self.screen,self.x,self.o,self.board[tile.x][tile.y])
        if self.player_turn==self.turn:
            a,b,c=self.play_step(self.get_action(self.game_state()),'x')
            time.sleep(0.1)
            return True 
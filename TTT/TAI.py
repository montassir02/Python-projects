import random
class TAI:
    def __init__(self,turn) :
        self.turn=turn   
    def get_empty(self,board):
        output = []
        row=len(board)
        column=len(board[0])
        for x in range(row):
            for y in range(column):
                if board[x][y]=='':
                    output.append(3*x+y)
        if output==[]:
            return output,False
        else:
            return output,True
    
    def rndv(self,table):
        return random.choice(table)
    
    def getP(self,value):
        x=int(value/3)
        y=value-3*x
        return x,y
    
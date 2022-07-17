import pandas as pd
import numpy as np
import random

class Die:
    
    def __init__(self, arr):
        self.faces = np.array(arr)
        if self.faces.dtype =='int64' or self.faces.dtype == '<U1': #could be done with isinstance()
            self._df = pd.DataFrame({'Faces': self.faces,
                                  'Weights': np.ones(self.faces.size)})
    
    def change(self, face, w_val):
        if face in list(self._df['Faces']):
            if (isinstance(w_val, int) or isinstance(w_val, float)):
                self._df.loc[self._df['Faces']==face,'Weights'] = float(w_val)
            else:
                raise TypeError("Weight has to be an integer or a float.")
        else:
            raise ValueError("Face value is not on the die")
            
    def roll(self, num = 1):
        v = []
        if num==1:
            outcomes = random.choices(self._df['Faces'], weights=(self._df['Weights']))
            return outcomes
        else:
            for i in range(num):
                outcomes = random.choices(self._df['Faces'], weights=(self._df['Weights']))
                v.append(outcomes)
        return v
    
    def show(self):
        return self._df
    

    
    

class Game:
    
    def __init__(self, l):
        self.l = np.array(l)
        self._result = pd.DataFrame()
    
    
    def play(self, n):
        
        self._result = pd.DataFrame()
        
        for i in range(self.l.size):
            res = pd.DataFrame(self.l[i].roll(n))
            res.index = [str(m+1) for m in range(n)]
            res.index.name = 'Roll Number'
            res.columns = [i+1]
            res.columns.name = 'Die Number'
            self._result = pd.concat([self._result, res], axis=1)
            
    def show(self, form = 'wide'):
        if form == 'wide':
            return self._result
        if form == 'narrow':
            return self._result.stack()
        else:
            raise ValueError("Can only accept values 'narrow' or 'wide'")
        
    

class Analyzer:
    
    def __init__(self, game):
        if isinstance(game, Game):
            self.game = game
        else:
            raise TypeError("Cannot accept values that are not objects of Game type")
        self.type = game.show().dtypes
        
        
        self._result = self.game.show()
        
        self.jackpots = pd.DataFrame()
        
        self.combinations = pd.DataFrame()
        self.face_counts = pd.DataFrame()
    
    def jackpot(self):
        num = 0
        df = self.game.show()
        nf = df.to_numpy()
        jackpot_dict = {"Roll Number": [], "is_jackpot": []}
        for i in range(len(nf)):
            res = len(set(nf[i])) <= 1
            if res:
                num += 1
            jackpot_dict["Roll Number"].append(i+1)
            jackpot_dict["is_jackpot"].append(res)
            
        self.jackpots = pd.DataFrame(jackpot_dict)
        self.jackpots.set_index('Roll Number', inplace = True)
        return num
    
    
    def combo(self):
        return self._result.apply(lambda x: pd.Series(sorted(x)), 1).value_counts().to_frame('n')
        
        
    def face_counts_per_roll(self):
        lfaces = self.game.l[0].faces
        rolls = self.game.show()
        
        self.face_counts = pd.DataFrame(columns=lfaces)
        
        for r,m in rolls.iterrows():
            temp = m.value_counts()
            self.face_counts.loc[r,np.array(temp.index)] = temp.values
        self.face_counts.fillna(0,inplace = True)
        self.face_counts.index.name = 'Roll Number'
        self.face_counts.columns.name = 'Face Values'
        return self.face_counts
        
        
        
    
    
    
    
    
    
    
    
    
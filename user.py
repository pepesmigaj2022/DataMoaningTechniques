import pandas as pd

class User:
    def __init__(self, uid, df):
       
        self.id = uid
        self.df = df

        self.data_history = df[df['id']==self.id]
        self.mood_history = self.data_history[self.data_history['record_type']=='mood']
        self.usage_history = self.data_history[self.data_history['record_type']!='mood']

        
    def __repr__(self):
        return (f"User(id={self.id}, df_shape={self.df.shape}, "
                f"data_history={len(self.data_history)}, "
                f"nood_history={len(self.mood_history)}, "
                f"usage_history={len(self.usage_history)}, "
                )
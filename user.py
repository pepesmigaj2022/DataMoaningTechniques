import pandas as pd

class User:
    def __init__(self, uid, df):
       

        self.id = uid
        self.df = df
       
        # Should we include 'time' as an input?
        # Because to predict the mood of a User at a time,
        # We can only use data up to the day (not time) before

        # What are we trying to p[redict?
        #   - Avg mood for the next day
        #   - Mood for the next hour

        self.data_history = df[df['id']==self.id]
        self.mood_history = self.data_history[self.data_history['record_type']=='mood']
        self.usage_history = self.data_history[self.data_history['record_type']!='mood']

        # Mean daily mood
        # Aggregated (additive) daily usage
        # 7day_ma_mood
        # 7day_ma_usage
        
    def __repr__(self):
        return (f"User(id={self.id}, df_shape={self.df.shape}, "
                f"data_history={len(self.data_history)}, "
                f"nood_history={len(self.mood_history)}, "
                f"usage_history={len(self.usage_history)}, "
                )
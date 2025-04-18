import pandas as pd
import numpy as np
import os


def clean_features_df(df, file_name):
    df = df.dropna(subset=['feature_avg_mood', 'feature_var_mood'])

    for col in ['feature_avg_arousal', 'feature_var_arousal', 'feature_avg_valence', 'feature_var_valence']:
        df[col] = df[col].fillna(df[col].mean())

    for col in ['feature_screen_time', 'feature_social_contact', 'feature_gaming','feature_office_app',
                 'feature_travel_app', 'feature_entertainment_app', 'feature_communication_app', 'feature_social_app']:
        df[col] = df[col].fillna(0)

    df.to_csv(f'clean_features/clean_{file_name}')

    
if __name__ == '__main__':
    folder = 'features'
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        df = pd.read_csv(file_path)

        clean_features_df(df, file)



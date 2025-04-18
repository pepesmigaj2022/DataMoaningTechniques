import pandas as pd
import matplotlib.pyplot as plt
import glob

file_paths = glob.glob('clean_features/clean_output*.csv')
dfs = [pd.read_csv(file) for file in file_paths]
combined_df = pd.concat(dfs, ignore_index=True)

non_features = ['date', 'Unnamed: 0']
feature_cols = [col for col in combined_df.columns if col not in non_features and col != 'feature_avg_mood']

for feature in feature_cols[1:]:
    plt.figure()
    plt.scatter(combined_df[feature], combined_df['feature_avg_mood'], alpha=0.6)
    plt.xlabel(feature)
    plt.ylabel('feature_avg_mood')
    plt.title(f'{feature} vs. feature_avg_mood')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
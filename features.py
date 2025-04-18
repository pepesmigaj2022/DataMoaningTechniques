import pandas as pd
import numpy as np


####################################################################################
# FEATURES                                                                         #
####################################################################################


def feature_general_op(id, record_type, op, df, record_detail = None):
    ''' 
    works when the operation of the values can be one function stored in op such as
    np.mean, np.sum... Variable record_type is a string from the column dataset_clean.csv
    It gives 2 vectors: one containing the dates (days) and the other the corresponding 
    values per day per id.
    '''
    if record_detail is None:
        filtered_df = df[(df['record_type'] == record_type)& (df['id'] == id)]
    else:
        filtered_df = df[(df['record_type'] == record_type) & (df['id'] == id) & (df['record_detail'] == record_detail)]

    if filtered_df.empty:
        print(f"No data for id {id} with record_type {record_type} and record_detail {record_detail}")
        return [[], []]  # Return empty lists if no data is found

    vals = [filtered_df['date'].values, filtered_df['value'].values]
    result_vals = []
    same_day = []
    dates = []
    date_helper = vals[0][0][:10]
    for i in range(len(vals[0])):
        current_date = vals[0][i][:10]
        if date_helper != current_date:
            dates.append(date_helper)
            date_helper = current_date
            result_vals.append(op(same_day))
        else:
           same_day.append(vals[1][i])
    return [dates, result_vals]

def feature_avg_mood(id, df):
    record_type = 'mood'
    op = np.mean
    return feature_general_op(id, record_type, op, df)

def feature_var_mood(id, df):
    record_type = 'mood'
    op = np.var
    return feature_general_op(id, record_type, op, df)
    
def feature_apps_time(id, df):
    record_type = 'app'
    op = np.sum
    return feature_general_op(id, record_type, op, df)

def feature_screen_time(id, df):
    record_type = 'screen'
    op = np.sum
    return feature_general_op(id, record_type, op, df)

def feature_social_contact(id,df): # only sms and calls, not comunication apps
    sms = feature_general_op(id, 'sms', np.sum, df)
    df_sms = pd.DataFrame({
        'date' : sms[0],
        'sms_vals' : sms[1]
    })
    calls = feature_general_op(id, 'call', np.sum, df)
    df_calls = pd.DataFrame({
        'date' : calls[0],
        'call_vals' : calls[1]
    })
    merged_df = pd.merge(df_calls, df_sms, on='date', how='outer')
    merged_df['call_vals'] = merged_df['call_vals'].fillna(0)
    merged_df['sms_vals'] = merged_df['sms_vals'].fillna(0)
    merged_df['total_vals'] = merged_df['call_vals'] + merged_df['sms_vals']
    return [merged_df['date'].values, merged_df['total_vals'].values]

def feature_avg_arousal(id, df):
    record_type = 'sensor'
    record_detail = 'arousal'
    op = np.mean
    return feature_general_op(id, record_type, op, df, record_detail=record_detail)

def feature_var_arousal(id, df):
    record_type = 'sensor'
    record_detail = 'arousal'
    op = np.var
    return feature_general_op(id, record_type, op, df, record_detail=record_detail)

def feature_gaming(id, df):
    record_type = 'app'
    record_detail = 'game'
    op = np.sum
    return feature_general_op(id, record_type, op, df, record_detail=record_detail)


####################################################################################
# DATAFRAME PER PERSON PER DAY                                                     #
####################################################################################

def create_df(id, df):
    # have to update when creating more features
    features = [feature_avg_mood, feature_var_mood, feature_screen_time, feature_apps_time, 
                feature_avg_arousal, feature_var_arousal, feature_social_contact, feature_gaming]
    feature0 = features[0]
    dfs = pd.DataFrame({
        'date' : feature0(id, df)[0],
        f'{feature0}'.split()[1] : feature0(id, df)[1]
    })

    for feature in features[1:]:
        df_new = pd.DataFrame({
            'date' : feature(id, df)[0],
            f'{feature}'.split()[1] : feature(id, df)[1]
        })
        dfs = pd.merge(dfs, df_new, on='date', how='outer')
        if dfs.empty:
            return
        dfs.to_csv(f'features/output{id}.csv')


####################################################################################
####################################################################################


file = "dataset_clean.csv"
dataset_clean = pd.read_csv(file)
num_people = max(dataset_clean['id'])

for i in range(num_people+1):
    create_df(i+1, dataset_clean)



import pandas as pd
import re

def preprocess(data, time_format):
    if time_format == "12-hour":
        pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s[ap]m - '  # Matches date and time
        date_format = '%d/%m/%y, %I:%M %p - '
    else:  # 24-hour format
        pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2} - '  # Matches date and time
        date_format = '%d/%m/%y, %H:%M - '
    
    messages = re.split(pattern, data)[1:]  # Split data into messages
    dates = re.findall(pattern, data)  # Find all dates and times

    df = pd.DataFrame({'date_time': dates, 'message': messages})
    df['date_time'] = pd.to_datetime(df['date_time'], format=date_format)
    df.rename(columns={'date_time': 'date'}, inplace=True)

    users = []
    msgs = []
    for message in df['message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            msgs.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['user'] = users
    df['message'] = msgs
    df.drop(columns=['message'], inplace=False)  # Ensure 'message' column is not dropped

    # Extracting additional columns for analysis
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['only_date'] = df['date'].dt.date
    
    return df

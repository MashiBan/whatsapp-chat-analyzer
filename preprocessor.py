import re
import pandas as pd
def preprocess(data):
    pattern = r'\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s(?:AM|PM)\s-\s'

    messages = re.split(pattern, data)
    dates = re.findall(pattern, data)

    print(len(messages))
    print(len(dates))

    # If they have different lengths, identify the discrepancy
    if len(messages) != len(dates):
        # Adjust either messages or dates so that they have the same length
        # For example, you can truncate the longer list or add placeholder values
        min_length = min(len(messages), len(dates))
        messages = messages[:min_length]
        dates = dates[:min_length]

    # Create the DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert the 'message_date' column to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M:%S %p - ')

    # Rename the column 'message_date' to 'date'
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:  # Correctly reference the 'user_message' column
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)  # Drop the original 'user_message' column

    df['year'] = df['date'].dt.year
    df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df